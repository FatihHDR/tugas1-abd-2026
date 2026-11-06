# Alur pengerjaan Tugas 1. Jalankan `make setup` sekali, lalu `make all`.
#
#   make setup      buat virtualenv dan pasang dependency
#   make data       unduh dataset NASA POWER ke data/raw/
#   make profiling  eksekusi notebooks/01_data_profiling.ipynb
#   make cleaning   eksekusi notebooks/02_data_cleaning.ipynb
#   make eda        eksekusi notebooks/03_eda_and_insights.ipynb
#   make all        data -> profiling -> cleaning -> eda

PY := .venv/bin/python
JUPYTER := .venv/bin/jupyter

.PHONY: setup data profiling cleaning eda all clean

setup:
	python3 -m venv .venv
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -r requirements.txt

data:
	$(PY) src/download_data.py

profiling:
	$(JUPYTER) nbconvert --to notebook --execute --inplace notebooks/01_data_profiling.ipynb

cleaning:
	$(JUPYTER) nbconvert --to notebook --execute --inplace notebooks/02_data_cleaning.ipynb

eda:
	$(JUPYTER) nbconvert --to notebook --execute --inplace notebooks/03_eda_and_insights.ipynb

all: data profiling cleaning eda

clean:
	rm -f data/raw/*.parquet data/processed/*.parquet output/figures/*.html
	rm -rf notebooks/.ipynb_checkpoints
