from __future__ import annotations

import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import duckdb
import polars as pl
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PARTS_DIR = RAW_DIR / "_parts"
OUTPUT_PATH = RAW_DIR / "cuaca_indonesia.parquet"

BASE_URL = "https://power.larc.nasa.gov/api/temporal/hourly/point"
COMMUNITY = "RE"
PARAMETERS = [
    "T2M",                # Suhu udara 2 m (degC)
    "T2MDEW",             # Titik embun 2 m (degC)
    "RH2M",               # Kelembapan relatif 2 m (%)
    "QV2M",               # Kelembapan spesifik 2 m (g/kg)
    "PRECTOTCORR",        # Presipitasi terkoreksi (mm/jam)
    "PS",                 # Tekanan permukaan (kPa)
    "WS10M",              # Kecepatan angin 10 m (m/s)
    "WD10M",              # Arah angin 10 m (derajat)
    "ALLSKY_SFC_SW_DWN",  # Radiasi matahari gelombang pendek (W/m^2)
    "CLOUD_AMT",          # Tutupan awan (%)
]

START_YEAR = 2001
END_YEAR = 2024
CHUNK_YEARS = 3
MAX_WORKERS = 8
FILL_VALUE = -900.0  # NASA POWER memakai -999.0 untuk data hilang

# API POWER mengembalikan timestamp dalam Local Standard Time (LST) masing-masing
# lokasi ("time_standard": "LST"), bukan UTC. Kolom waktu karena itu dinamai
# "waktu_lokal" dan zona waktu tiap kota disimpan pada kolom "zona_waktu".

# (kota, provinsi, latitude, longitude, zona_waktu, utc_offset_hours)
CITIES: list[tuple[str, str, float, float, str, int]] = [
    ("Banda Aceh", "Aceh", 5.5483, 95.3238, "WIB", 7),
    ("Medan", "Sumatera Utara", 3.5952, 98.6722, "WIB", 7),
    ("Padang", "Sumatera Barat", -0.9471, 100.4172, "WIB", 7),
    ("Pekanbaru", "Riau", 0.5071, 101.4478, "WIB", 7),
    ("Tanjung Pinang", "Kepulauan Riau", 0.9186, 104.4665, "WIB", 7),
    ("Jambi", "Jambi", -1.6101, 103.6131, "WIB", 7),
    ("Palembang", "Sumatera Selatan", -2.9761, 104.7754, "WIB", 7),
    ("Pangkal Pinang", "Kepulauan Bangka Belitung", -2.1316, 106.1169, "WIB", 7),
    ("Bengkulu", "Bengkulu", -3.8004, 102.2655, "WIB", 7),
    ("Bandar Lampung", "Lampung", -5.3971, 105.2668, "WIB", 7),
    ("Serang", "Banten", -6.1104, 106.1503, "WIB", 7),
    ("Jakarta", "DKI Jakarta", -6.2088, 106.8456, "WIB", 7),
    ("Bandung", "Jawa Barat", -6.9175, 107.6191, "WIB", 7),
    ("Semarang", "Jawa Tengah", -6.9932, 110.4203, "WIB", 7),
    ("Yogyakarta", "DI Yogyakarta", -7.7956, 110.3695, "WIB", 7),
    ("Surabaya", "Jawa Timur", -7.2575, 112.7521, "WIB", 7),
    ("Malang", "Jawa Timur", -7.9666, 112.6326, "WIB", 7),
    ("Denpasar", "Bali", -8.6705, 115.2126, "WITA", 8),
    ("Mataram", "Nusa Tenggara Barat", -8.5833, 116.1167, "WITA", 8),
    ("Kupang", "Nusa Tenggara Timur", -10.1772, 123.6070, "WITA", 8),
    ("Pontianak", "Kalimantan Barat", -0.0263, 109.3425, "WIB", 7),
    ("Palangka Raya", "Kalimantan Tengah", -2.2080, 113.9165, "WIB", 7),
    ("Banjarmasin", "Kalimantan Selatan", -3.3186, 114.5944, "WITA", 8),
    ("Samarinda", "Kalimantan Timur", -0.5017, 117.1536, "WITA", 8),
    ("Balikpapan", "Kalimantan Timur", -1.2379, 116.8529, "WITA", 8),
    ("Tanjung Selor", "Kalimantan Utara", 2.8375, 117.3660, "WITA", 8),
    ("Manado", "Sulawesi Utara", 1.4748, 124.8421, "WITA", 8),
    ("Palu", "Sulawesi Tengah", -0.8917, 119.8707, "WITA", 8),
    ("Makassar", "Sulawesi Selatan", -5.1477, 119.4327, "WITA", 8),
    ("Kendari", "Sulawesi Tenggara", -3.9450, 122.4989, "WITA", 8),
    ("Gorontalo", "Gorontalo", 0.5435, 123.0568, "WITA", 8),
    ("Mamuju", "Sulawesi Barat", -2.6748, 118.8885, "WITA", 8),
    ("Ambon", "Maluku", -3.6954, 128.1814, "WIT", 9),
    ("Sofifi", "Maluku Utara", 0.7347, 127.5586, "WIT", 9),
    ("Jayapura", "Papua", -2.5916, 140.6690, "WIT", 9),
    ("Manokwari", "Papua Barat", -0.8615, 134.0620, "WIT", 9),
    ("Sorong", "Papua Barat Daya", -0.8762, 131.2558, "WIT", 9),
    ("Merauke", "Papua Selatan", -8.4932, 140.4018, "WIT", 9),
    ("Nabire", "Papua Tengah", -3.3500, 135.4833, "WIT", 9),
    ("Wamena", "Papua Pegunungan", -4.0996, 138.9445, "WIT", 9),
]


def slug(name: str) -> str:
    """Ubah nama kota menjadi nama file yang aman."""
    return name.lower().replace(" ", "_")


def year_chunks(start_year: int, end_year: int) -> list[tuple[int, int]]:
    """Bagi rentang tahun menjadi potongan <= CHUNK_YEARS tahun."""
    chunks: list[tuple[int, int]] = []
    start = start_year
    while start <= end_year:
        end = min(start + CHUNK_YEARS - 1, end_year)
        chunks.append((start, end))
        start = end + 1
    return chunks


def request_payload(lat: float, lon: float, start_year: int, end_year: int) -> dict:
    """Kirim permintaan ke POWER dan kembalikan JSON-nya."""
    params = {
        "parameters": ",".join(PARAMETERS),
        "community": COMMUNITY,
        "longitude": lon,
        "latitude": lat,
        "start": f"{start_year}0101",
        "end": f"{end_year}1231",
        "format": "JSON",
    }
    response = requests.get(BASE_URL, params=params, timeout=300)
    response.raise_for_status()
    return response.json()


def fetch_chunk(
    lat: float, lon: float, start_year: int, end_year: int
) -> pl.DataFrame:
    """Ambil satu potongan tahun; jika rentangnya ditolak, pecah menjadi lebih kecil."""
    try:
        payload = request_payload(lat, lon, start_year, end_year)
    except requests.HTTPError as error:
        if error.response is not None and error.response.status_code == 422 and start_year < end_year:
            mid = (start_year + end_year) // 2
            return pl.concat(
                [
                    fetch_chunk(lat, lon, start_year, mid),
                    fetch_chunk(lat, lon, mid + 1, end_year),
                ],
                how="vertical",
            )
        raise

    parameter_data = payload["properties"]["parameter"]
    timestamps = list(parameter_data[PARAMETERS[0]].keys())

    return pl.DataFrame(
        {
            "waktu_lokal": timestamps,
            **{name: list(parameter_data[name].values()) for name in PARAMETERS},
        }
    ).with_columns(
        (pl.col("waktu_lokal") + "00").str.strptime(pl.Datetime("us"), "%Y%m%d%H%M").alias("waktu_lokal"),
        *[
            pl.when(pl.col(name) <= FILL_VALUE)
            .then(None)
            .otherwise(pl.col(name))
            .alias(name)
            for name in PARAMETERS
        ],
    )


def download_city(city: tuple[str, str, float, float, str, int]) -> str:
    """Unduh seluruh rentang tahun untuk satu kota dan simpan sebagai bagian Parquet."""
    kota, provinsi, lat, lon, zona, offset = city
    part_path = PARTS_DIR / f"{slug(kota)}.parquet"
    if part_path.exists():
        return f"{kota}: sudah ada, dilewati"

    frames = [fetch_chunk(lat, lon, s, e) for s, e in year_chunks(START_YEAR, END_YEAR)]
    combined = pl.concat(frames, how="vertical").sort("waktu_lokal").with_columns(
        pl.lit(kota).alias("kota"),
        pl.lit(provinsi).alias("provinsi"),
        pl.lit(lat, dtype=pl.Float64).alias("latitude"),
        pl.lit(lon, dtype=pl.Float64).alias("longitude"),
        pl.lit(zona).alias("zona_waktu"),
        pl.lit(offset, dtype=pl.Int8).alias("utc_offset_jam"),
    )
    combined.write_parquet(part_path)
    return f"{kota}: {combined.height:,} baris tersimpan"


def combine_parts() -> None:
    """Gabungkan seluruh file per kota menjadi satu Parquet via DuckDB (streaming)."""
    connection = duckdb.connect()
    connection.execute(
        f"""
        COPY (
            SELECT * FROM read_parquet('{PARTS_DIR}/*.parquet')
        ) TO '{OUTPUT_PATH}' (FORMAT PARQUET, COMPRESSION SNAPPY)
        """
    )
    connection.close()


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PARTS_DIR.mkdir(parents=True, exist_ok=True)

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(download_city, city): city for city in CITIES}
        for index, future in enumerate(as_completed(futures), start=1):
            print(f"[{index}/{len(CITIES)}] {future.result()}")

    print("Menggabungkan seluruh bagian menjadi satu file Parquet ...")
    combine_parts()

    connection = duckdb.connect()
    total_rows = connection.execute(
        f"SELECT COUNT(*) FROM read_parquet('{OUTPUT_PATH}')"
    ).fetchone()[0]
    connection.close()

    shutil.rmtree(PARTS_DIR, ignore_errors=True)

    size_mb = OUTPUT_PATH.stat().st_size / 1_000_000
    print(
        f"Selesai dalam {time.time() - start_time:.0f}s: {total_rows:,} baris, "
        f"{size_mb:.1f} MB -> {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()
