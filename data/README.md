# Data Tugas 1

## Dataset yang Dipilih

| Item | Isi |
|---|---|
| Nama dataset | Cuaca per Jam Kota-Kota Indonesia (NASA POWER / MERRA-2) |
| Sumber | [NASA POWER Project](https://power.larc.nasa.gov/) |
| Endpoint API | `https://power.larc.nasa.gov/api/temporal/hourly/point` |
| Lisensi/ketentuan pakai | Data terbuka NASA; bebas digunakan untuk penelitian dan pendidikan. Cantumkan atribusi kepada *NASA POWER Project* ([kebijakan penggunaan](https://power.larc.nasa.gov/docs/)). |
| Ukuran | **8.415.360 baris** (~190 MB Parquet) — memenuhi kriteria **> 1.000.000 baris** |
| Periode data | 1 Januari 2001 – 31 Desember 2024 (waktu lokal / LST tiap kota) |
| Unit analisis | Satu observasi cuaca per jam untuk satu kota |

Nilai ini jauh melampaui batas minimal tugas. Karena data cuaca per jam punya
banyak baris dengan ukuran file relatif padat, dataset memenuhi syarat melalui
kriteria jumlah baris (> 1 juta baris) alih-alih ukuran berkas.

## Deskripsi

Dataset berisi kondisi cuaca per jam untuk 40 kota yang mewakili **seluruh 38
provinsi di Indonesia**. Data berasal dari reanalisis **MERRA-2** yang
disajikan melalui NASA POWER pada grid spasial sekitar 0,5° × 0,625°. Setiap
kota direpresentasikan oleh titik koordinat pusat kota, sehingga dataset cocok
untuk analisis **temporal** (tren, musiman, siklus harian) sekaligus
**spasial** (perbandingan antar wilayah dan zona waktu).

## Cakupan Wilayah

| Kota | Provinsi | Latitude | Longitude | Zona waktu |
|---|---|--:|--:|:--:|
| Banda Aceh | Aceh | 5.5483 | 95.3238 | WIB |
| Medan | Sumatera Utara | 3.5952 | 98.6722 | WIB |
| Padang | Sumatera Barat | -0.9471 | 100.4172 | WIB |
| Pekanbaru | Riau | 0.5071 | 101.4478 | WIB |
| Tanjung Pinang | Kepulauan Riau | 0.9186 | 104.4665 | WIB |
| Jambi | Jambi | -1.6101 | 103.6131 | WIB |
| Palembang | Sumatera Selatan | -2.9761 | 104.7754 | WIB |
| Pangkal Pinang | Kepulauan Bangka Belitung | -2.1316 | 106.1169 | WIB |
| Bengkulu | Bengkulu | -3.8004 | 102.2655 | WIB |
| Bandar Lampung | Lampung | -5.3971 | 105.2668 | WIB |
| Serang | Banten | -6.1104 | 106.1503 | WIB |
| Jakarta | DKI Jakarta | -6.2088 | 106.8456 | WIB |
| Bandung | Jawa Barat | -6.9175 | 107.6191 | WIB |
| Semarang | Jawa Tengah | -6.9932 | 110.4203 | WIB |
| Yogyakarta | DI Yogyakarta | -7.7956 | 110.3695 | WIB |
| Surabaya | Jawa Timur | -7.2575 | 112.7521 | WIB |
| Malang | Jawa Timur | -7.9666 | 112.6326 | WIB |
| Denpasar | Bali | -8.6705 | 115.2126 | WITA |
| Mataram | Nusa Tenggara Barat | -8.5833 | 116.1167 | WITA |
| Kupang | Nusa Tenggara Timur | -10.1772 | 123.6070 | WITA |
| Pontianak | Kalimantan Barat | -0.0263 | 109.3425 | WIB |
| Palangka Raya | Kalimantan Tengah | -2.2080 | 113.9165 | WIB |
| Banjarmasin | Kalimantan Selatan | -3.3186 | 114.5944 | WITA |
| Samarinda | Kalimantan Timur | -0.5017 | 117.1536 | WITA |
| Balikpapan | Kalimantan Timur | -1.2379 | 116.8529 | WITA |
| Tanjung Selor | Kalimantan Utara | 2.8375 | 117.3660 | WITA |
| Manado | Sulawesi Utara | 1.4748 | 124.8421 | WITA |
| Palu | Sulawesi Tengah | -0.8917 | 119.8707 | WITA |
| Makassar | Sulawesi Selatan | -5.1477 | 119.4327 | WITA |
| Kendari | Sulawesi Tenggara | -3.9450 | 122.4989 | WITA |
| Gorontalo | Gorontalo | 0.5435 | 123.0568 | WITA |
| Mamuju | Sulawesi Barat | -2.6748 | 118.8885 | WITA |
| Ambon | Maluku | -3.6954 | 128.1814 | WIT |
| Sofifi | Maluku Utara | 0.7347 | 127.5586 | WIT |
| Jayapura | Papua | -2.5916 | 140.6690 | WIT |
| Manokwari | Papua Barat | -0.8615 | 134.0620 | WIT |
| Sorong | Papua Barat Daya | -0.8762 | 131.2558 | WIT |
| Merauke | Papua Selatan | -8.4932 | 140.4018 | WIT |
| Nabire | Papua Tengah | -3.3500 | 135.4833 | WIT |
| Wamena | Papua Pegunungan | -4.0996 | 138.9445 | WIT |

## Skema Kolom

| Kolom | Tipe | Satuan | Keterangan |
|---|---|---|---|
| `waktu_lokal` | Datetime | LST | Timestamp observasi (Local Standard Time kota tersebut) |
| `T2M` | Float64 | °C | Suhu udara pada ketinggian 2 m |
| `T2MDEW` | Float64 | °C | Titik embun pada ketinggian 2 m |
| `RH2M` | Float64 | % | Kelembapan relatif pada 2 m |
| `QV2M` | Float64 | g/kg | Kelembapan spesifik pada 2 m |
| `PRECTOTCORR` | Float64 | mm/jam | Presipitasi total terkoreksi |
| `PS` | Float64 | kPa | Tekanan permukaan |
| `WS10M` | Float64 | m/s | Kecepatan angin pada 10 m |
| `WD10M` | Float64 | derajat | Arah angin pada 10 m (0–360) |
| `ALLSKY_SFC_SW_DWN` | Float64 | W/m² | Radiasi matahari gelombang pendek di permukaan |
| `CLOUD_AMT` | Float64 | % | Tutupan awan total |
| `kota` | String | – | Nama kota |
| `provinsi` | String | – | Nama provinsi |
| `latitude` | Float64 | derajat | Latitude pusat kota |
| `longitude` | Float64 | derajat | Longitude pusat kota |
| `zona_waktu` | String | – | WIB / WITA / WIT |
| `utc_offset_jam` | Int8 | jam | Offset zona waktu terhadap UTC (7/8/9) |

## Cara Memperoleh Data

Dataset direproduksi otomatis dengan skrip `src/download_data.py`.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/download_data.py
```

Skrip tersebut:

1. Mengunduh data per jam dari API POWER untuk setiap kota pada rentang
   2001–2024. Karena API membatasi ukuran tiap permintaan, rentang waktu
   dipecah menjadi potongan 3 tahun dan diunduh secara paralel.
2. Mengubah nilai *fill value* `-999` menjadi `NULL`.
3. Menggabungkan seluruh potongan menjadi satu berkas
   `data/raw/cuaca_indonesia.parquet` (Parquet, kompresi SNAPPY).

Untuk pemeriksaan manual, contoh satu permintaan (satu kota, satu potongan):

```text
https://power.larc.nasa.gov/api/temporal/hourly/point
  ?parameters=T2M,T2MDEW,RH2M,QV2M,PRECTOTCORR,PS,WS10M,WD10M,ALLSKY_SFC_SW_DWN,CLOUD_AMT
  &community=RE
  &latitude=-6.2088&longitude=106.8456
  &start=20010101&end=20031231
  &format=JSON
```

## Checksum

```
sha256  8da9dcbd6c434e16ac6bd9c3fcc4c320434f97a6f62a4b82fbc86bd4bb60debc
```

## Catatan Kualitas Data

- Nilai penanda data hilang `-999` dari NASA POWER sudah dikonversi menjadi
  `null`; dataset bersih ini tidak mengandung nilai tersebut.
- Timestamp tersimpan dalam **Local Standard Time (LST)** masing-masing kota
  (bukan UTC); API POWER mengembalikan `"time_standard": "LST"`. Kolom
  `zona_waktu` (WIB/WITA/WIT) dan `utc_offset_jam` disertakan sebagai metadata.
  Karena Indonesia tidak memakai DST, waktu lokal ini langsung dapat dipakai
  untuk analisis siklus harian.
- Setiap kombinasi `(kota, waktu_lokal)` bersifat unik; tidak ada duplikasi.
- Titik koordinat mengikuti grid reanalisis MERRA-2, bukan stasiun
  pengamatan darat, sehingga nilai merepresentasikan rata-rata area sekitar.

## Aturan Penyimpanan

- Jangan commit dataset mentah atau hasil olahan berukuran besar ke Git
  (lihat `.gitignore`). Skrip unduh adalah sumber kebenaran untuk reproduksi.
- File pada `data/raw/` adalah data hasil unduhan dan tidak boleh diubah manual.
- Simpan hasil transformasi yang dapat direproduksi pada `data/processed/`.
