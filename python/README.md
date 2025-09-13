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
```

## Linting and tests

```
ruff check . --fix
black .
pytest
```

## Configure Google Gemini
1) Obtain an API key from Google AI Studio.
2) Store it as an environment variable in your shell startup or a dotenv file (do not commit secrets):

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