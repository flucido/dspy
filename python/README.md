# Python Data Engineering + Analysis Project

This project is preconfigured with a modern Python stack for data engineering, analysis, notebooks, visualization, ML, cloud I/O, and Google Gemini.

## Requirements
- Python 3.12 (managed by pyenv via .python-version)
- uv package manager (already installed)

## Quick start

1) Create/refresh the environment and install all groups:

```
uv sync --all-extras
```

This creates `.venv` and installs core + extras: `de,pandas,viz,ml,notebooks,dev,cloud,genai`.

2) Activate the venv:

```
source .venv/bin/activate
```

3) Start JupyterLab:

```
jupyter lab
```

## Using extras selectively
Install only what you need, for example:

```
uv sync -E notebooks -E viz -E de -E pandas -E cloud -E genai -E ml
uv sync -E orchestration -E transform -E streaming -E go -E timeseries -E performance -E notebook_polish
# Great Expectations (vq) requires pandas<=2.1.4; this project already constrains pandas extra accordingly.
uv sync -E vq
# Altair is optional and is split to avoid conflicts with vq; install separately if you want it.
uv sync -E altair
# Airflow is heavy; if resolution fails, install with provider constraints (see below)
uv sync -E airflow
```

### Airflow install note
Airflow often requires constraints to pin providers. If the extra fails to resolve, try:

```
# Example for Python 3.12; confirm the constraints URL for your Airflow version
CONSTRAINTS_URL=https://raw.githubusercontent.com/apache/airflow/constraints-2.10.2/constraints-3.12.txt
uv pip install --constraint "$CONSTRAINTS_URL" apache-airflow==2.10.2
```

## Linting and tests

```
ruff check . --fix
black .
pytest
```

## Configure Google Gemini
1) Obtain an API key from Google AI Studio.
2) Store it as an environment variable in your shell startup or a dotenv file (do not commit secrets). You can copy `.env.example` to `.env` and fill values:

```
export GEMINI_API_KEY={{GEMINI_API_KEY}}
```

3) Minimal usage example:

```
python - <<'PY'
import os, google.generativeai as genai
api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    raise SystemExit('Set GEMINI_API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
resp = model.generate_content('Say hi from a data stack!')
print(resp.text)
PY
```

## Notes
- Core libraries: numpy, polars, pyarrow, requests
- Data engineering: duckdb, SQLAlchemy, psycopg2-binary, alembic
- Pandas stack: pandas, openpyxl
- Visualization: matplotlib, seaborn, plotly, altair
- ML: scikit-learn
- Notebooks: jupyter, jupyterlab, ipykernel, ipywidgets
- Dev: pytest, pytest-cov, black, ruff, mypy
- Cloud/BigQuery: fsspec, s3fs, gcsfs, boto3, google-cloud-*
- GenAI: google-generativeai, python-dotenv, pydantic