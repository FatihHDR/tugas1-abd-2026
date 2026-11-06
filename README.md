# Tugas 1: Eksplorasi dan Analisis Dataset Besar Indonesia

**Nama:** Fatahillah Al-Fatih
**NIM:** 202310370311132
**Username GitHub:** FatihHDR
**Mata Kuliah:** Analisis Big Data

Analisis big data atas **cuaca per jam untuk 40 kota di 38 provinsi Indonesia** (2001-2024) bersumber dari **NASA POWER** (reanalisis MERRA-2). Proyek mencakup pengunduhan data, profiling, cleaning dan validasi, analisis temporal-spasial, enam visualisasi interaktif, serta lima insight analitik. Seluruh proses dapat dijalankan ulang dari nol dan direproduksi lewat Docker.

## Ringkasan Cepat

| Item | Nilai |
|---|---|
| Dataset | Cuaca per jam 40 kota Indonesia (NASA POWER / MERRA-2) |
| Ukuran | **8.415.360 baris x 17 kolom** (memenuhi kriteria > 1 juta baris) |
| Periode | 1 Januari 2001 - 31 Desember 2024 (waktu lokal / LST) |
| Tools utama | Polars (lazy), DuckDB (SQL/`SUMMARIZE`), Plotly (interaktif) |
| Keluaran | 3 notebook tereksekusi, 6 visualisasi interaktif, 5 insight |

## Milestone

| Tahap | Target | Bukti yang dikumpulkan | Status |
|---|---|---|---|
| Milestone 1 | Pertemuan 3 | Dataset >= 500 MB atau > 1 juta baris, `data/README.md`, dan `notebooks/01_data_profiling.ipynb` | Selesai |
| Milestone 2 | Pertemuan 5 | Cleaning dengan Polars dan profiling DuckDB `SUMMARIZE` | Selesai |
| Milestone 3 | Pertemuan 8 | Analisis temporal/ruang dan minimal 6 visualisasi interaktif | Selesai |
| Final | Pertemuan 10 | Minimal 5 insight, Dockerfile, dan dokumentasi akhir | Selesai |

## Dataset

| Item | Isi |
|---|---|
| Nama | Cuaca per jam kota-kota Indonesia (NASA POWER / MERRA-2) |
| Sumber | NASA POWER Project - https://power.larc.nasa.gov/ |
| Endpoint | `https://power.larc.nasa.gov/api/temporal/hourly/point` |
| Lisensi | Data terbuka NASA; bebas digunakan untuk penelitian/pendidikan dengan atribusi |
| Ukuran | 8.415.360 baris, ~190 MB (Parquet) |
| Periode | 2001-01-01 s.d. 2024-12-31, waktu lokal (LST) tiap kota |
| Unit analisis | Satu observasi cuaca per jam untuk satu kota |

Variabel per jam: `T2M`, `T2MDEW`, `RH2M`, `QV2M`, `PRECTOTCORR`, `PS`, `WS10M`, `WD10M`, `ALLSKY_SFC_SW_DWN`, `CLOUD_AMT`. Dokumentasi lengkap (skema kolom, cakupan kota, checksum, cara unduh) ada di **[`data/README.md`](data/README.md)**.

## Struktur Repository

```text
.
├── .dockerignore                 # mengecualikan data besar/.venv dari image
├── .github/workflows/lint_check.yml
├── data/
│   ├── README.md                 # dokumentasi dataset + instruksi unduh + checksum
│   ├── raw/                      # hasil unduhan (tidak di-commit)
│   └── processed/                # data bersih (tidak di-commit)
├── notebooks/
│   ├── 01_data_profiling.ipynb   # Milestone 1: Polars lazy + DuckDB SUMMARIZE
│   ├── 02_data_cleaning.ipynb    # Milestone 2: cleaning + validasi
│   └── 03_eda_and_insights.ipynb # Milestone 3: temporal/spasial + 6 visualisasi + 5 insight
├── output/figures/               # figur interaktif HTML (tidak di-commit)
├── src/
│   └── download_data.py          # skrip unduh dataset NASA POWER
├── Dockerfile
├── Makefile                      # orkestrasi pipeline (opsional)
├── requirements.txt
├── identitas.md
└── README.md
```

## Cara Menjalankan Project

### Opsi A - Docker (rekomendasi, terisolasi)

```bash
# 1. Bangun image
docker build -t tugas1-bigdata .

# 2. Jalankan container (mount folder proyek agar hasil tersimpan di host)
docker run --rm -p 8888:8888 -v "$(pwd)":/home/jovyan/work tugas1-bigdata

# 3. Buka JupyterLab di browser
#    http://localhost:8888/lab
```

Di dalam JupyterLab (menu Terminal), jalankan pipeline berurutan:

```bash
python src/download_data.py
jupyter nbconvert --to notebook --execute --inplace notebooks/01_data_profiling.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_data_cleaning.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/03_eda_and_insights.ipynb
```

> **Catatan:** Dockerfile menjalankan JupyterLab tanpa password/token untuk penggunaan lokal. Jangan pakai konfigurasi ini di server atau jaringan publik.

### Opsi B - Virtualenv lokal

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/download_data.py          # unduh dataset ke data/raw/
jupyter lab                          # lalu jalankan notebook 01 -> 02 -> 03
```

Dengan `make` (opsional):

```bash
make setup   # buat .venv + pasang dependency
make all     # data -> profiling -> cleaning -> eda
```

## Alur Pipeline

| Langkah | Perintah | Masukan | Keluaran |
|---|---|---|---|
| 1. Unduh data | `python src/download_data.py` | API NASA POWER | `data/raw/cuaca_indonesia.parquet` |
| 2. Profiling | `notebooks/01_data_profiling.ipynb` | `data/raw/*.parquet` | profil skema, baris, null, `SUMMARIZE` |
| 3. Cleaning | `notebooks/02_data_cleaning.ipynb` | `data/raw/*.parquet` | `data/processed/dataset_bersih.parquet` |
| 4. EDA & insight | `notebooks/03_eda_and_insights.ipynb` | `data/processed/*.parquet` | 6 figur di `output/figures/` + 5 insight |

Notebook dirancang **dapat dieksekusi berurutan** dan **idempoten** (mengulang tidak mengubah hasil). Notebook menulis output ke `data/processed/` dan `output/figures/`, sehingga langkah berikutnya tidak perlu mengulang langkah sebelumnya.

## Hasil dan Insight Utama

Lima insight yang didukung analisis (detail di `notebooks/03_eda_and_insights.ipynb`):

1. **Tren pemanasan.** Suhu nasional naik ~**+0,023 derajat C/tahun**; rata-rata 2001-2005 (25,70 derajat C) naik ke 2020-2024 (26,05 derajat C) = **+0,35 derajat C**. Semua 40 kota bertren positif; bulan terpanas terjadi pada 2023-2024 (El Nino).
2. **Ketimpangan spasial.** Rentang suhu antar kota ~**14,5 derajat C**: Wamena 13,43 derajat C (dataran tinggi) hingga Tanjung Pinang 27,91 derajat C (pesisir/kepulauan).
3. **Korelasi kunci.** `T2M`-`PS` +0,74, `T2M`-`RH2M` -0,64, `T2M`-solar +0,45; sebagian besar efek antar-lokasi (ketinggian) yang perlu diwaspadai sebagai *confounding*.
4. **Pola musiman dan harian.** Curah hujan Desember **8,80 mm/hari** vs Agustus **3,81 mm/hari** (2,3x); suhu puncak pukul 13.00 (28,35 derajat C) dan terendah pukul 05.00 (23,83 derajat C), rentang ~4,5 derajat C.
5. **Rekomendasi.** Kalender tanam mengikuti puncak hujan Desember-Januari; waspadai *heat stress* pukul Oktober-November; pakai laju +0,023 derajat C/tahun sebagai baseline adaptasi iklim; korelasi suhu-radiasi mendukung potensi PLTS.

Enam visualisasi interaktif (Plotly): (1) tren deret waktu + *range slider*, (2) box plot distribusi suhu per kota, (3) heatmap korelasi, (4) treemap curah hujan per provinsi, (5) heatmap siklus jam x bulan, (6) peta spasial suhu/curah hujan. Figur HTML tersimpan di `output/figures/` dan juga tertanam di notebook.

## Reproduksibilitas dan Lingkungan

- **Docker:** `Dockerfile` berbasis `quay.io/jupyter/datascience-notebook` memasang seluruh dependency dari `requirements.txt`.
- **`.dockerignore`:** mencegah data besar, `.venv`, dan `.git` ikut masuk ke image.
- **`requirements.txt`:** `duckdb`, `jupyterlab`, `numpy`, `pandas`, `plotly`, `polars[pyarrow]`, `pyarrow`.
- **`Makefile`:** menyediakan satu perintah untuk menjalankan seluruh pipeline (`make all`).
- **Data:** tidak di-commit (lihat `.gitignore`); direproduksi lewat `src/download_data.py` dari API publik NASA POWER.

## Pemeriksaan Otomatis

Workflow `.github/workflows/lint_check.yml` berjalan pada setiap push/PR dan menjalankan:

- `python -m compileall src` - memastikan skrip Python bebas error sintaks.
- Validasi JSON seluruh notebook di `notebooks/`.

## Ringkasan Penilaian

Nilai Tugas 1 berbobot 25% dari nilai akhir. Ringkasan indikator:

| Aspek | Bobot | Indikator utama |
|---|:---:|---|
| Konsistensi commit dan GitHub workflow | 20% | Commit bertahap, pesan deskriptif, struktur repository rapi, dan pemeriksaan otomatis lulus. |
| Data handling dengan Polars dan DuckDB | 25% | Pengolahan data besar efisien, memakai Polars dan DuckDB sesuai peran masing-masing. |
| Cleaning dan data quality | 15% | Profiling, validasi, serta penanganan null dan outlier terdokumentasi. |
| Visualisasi dan insight | 25% | Visualisasi interaktif informatif dan insight analitik yang didukung data. |
| Reproduktivitas dan Docker | 15% | Dockerfile, dependency, dan instruksi eksekusi memungkinkan proyek dijalankan ulang. |

## Kaitan dengan Materi Perkuliahan

| Materi | Pertemuan | Penerapan pada Tugas 1 |
|---|:---:|---|
| Polars dan lazy evaluation | 2 | Profiling dan transformasi dataset besar dengan `scan_parquet`, expressions, `group_by_dynamic`, `rolling_mean`. |
| DuckDB dan format data | 3 | Query analitik serta profiling dengan `SUMMARIZE`, kuantil, `corr`, window `OVER`, dan `regr_slope`; memakai Parquet. |
| Data quality dan cleaning | 4 | Penanganan nilai hilang, outlier, duplikasi, dan aturan validasi fisik pada notebook 02. |
| EDA dan visualisasi | 5 | Enam visualisasi interaktif Plotly dan lima insight analitik. |
| Time series | 6 | Tren jangka panjang, rata-rata bergerak, siklus musiman dan harian pada notebook 03. |
| Streamlit dan Docker | 10-11 | Environment Docker terdokumentasi (dashboard Streamlit bersifat opsional). |

## Aturan Teknis

- Gunakan Polars untuk manipulasi data dan DuckDB untuk analitik SQL.
- Dataset harus minimal 500 MB atau lebih dari 1 juta baris.
- Jangan commit file data besar; simpan instruksi unduhan dan sumber data pada `data/README.md`.
- Gunakan commit bertahap dan pesan yang jelas, misalnya `feat: add initial dataset profiling`.

## Integritas Akademik dan Penggunaan AI

- Dilarang menyalin kode, laporan, atau visualisasi mahasiswa lain maupun repository publik tanpa sitasi dan atribusi yang jelas.
- Dilarang menggunakan jasa joki atau menyerahkan pekerjaan yang tidak dapat dijelaskan sendiri.
- AI boleh digunakan untuk belajar, mencari rujukan, menjelaskan konsep, atau debugging. AI tidak menggantikan tanggung jawab mahasiswa atas kebenaran dan kualitas solusi.
- Mahasiswa wajib dapat menjelaskan setiap bagian kode, menjalankan serta memverifikasi ulang hasilnya, dan memastikan penggunaan Polars serta DuckDB sesuai standar kuliah.
- Setiap penggunaan AI harus dicantumkan pada bagian AI Disclosure Statement di bawah.
- Pelanggaran pertama bernilai 0 untuk tugas terkait; pelanggaran berikutnya dapat berakibat nilai E untuk mata kuliah sesuai ketentuan akademik.

## AI Disclosure Statement

> **Alat AI yang digunakan:** Command Code.
>
> **Bagian yang dibantu:** penyusunan skrip pengunduhan data `src/download_data.py`; penulisan dan debugging kode Polars/DuckDB pada notebook profiling dan cleaning; pembuatan visualisasi Plotly; penulisan draft dokumentasi `README.md` dan `data/README.md`; perbaikan error (mis. perubahan API `pl()` DuckDB, `min_periods` -> `min_samples` Polars, serta koreksi label waktu UTC -> LST).
>
> **Verifikasi yang dilakukan:** menjalankan ulang seluruh notebook dari nol dan memeriksa keluaran setiap cell; memverifikasi profil statistik dan rentang nilai agar sesuai batas fisis (mis. `T2MDEW <= T2M`, `0 <= RH2M <= 100`); memeriksa dokumentasi resmi NASA POWER, Polars, dan DuckDB; serta memastikan setiap temuan pada bagian insight dapat dijelaskan dan ditelusuri ke keluaran analisis.

## Atribusi Data

Data bersumber dari **NASA POWER Project** (Prediction Of Worldwide Energy Resources), yang memakai reanalisis **MERRA-2**. Sitasi yang disarankan:

> NASA Langley Research Center (LaRC). *POWER Project Data Sets*. https://power.larc.nasa.gov/
