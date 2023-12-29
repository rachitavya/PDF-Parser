# PDF-Parser
A toolkit to parse PDFs for RAGs.


## Setup
Clone the repo and cd to project root.

### Environment
1. Create and activate venv. Ex:
```
python -m venv venv
.\venv\Scripts\activate
```
2. This project uses [poetry](https://python-poetry.org/docs/basic-usage/).
```
pip install poetry
poetry install
```

### Parser
**Context:** 
1. The process has two steps: PDF -> MD -> CSV
2. PDF and MD files are in input/{language} folder
3. PDF -> MD is done by external repo
4. The repo contains code for MD -> CSV conversion.

**Step 1:** `python src/markdown_parser.py`
This will convert all the md files (from input/md/ folder) to csv files (saved in output/ folder).
**Step 2:** `python src/csv_preprocessing.py`
This performs further processing on the csv files in output/ folder and saves the output there only.



### API Under development
The idea is to create a single function for both the above steps and after combining them wiht PDF -> MD conversion, we can create a celery function for the API.

Setup steps would be:
#### Step 1:
`docker run -d -p 6379:6379 --name my-redis redis`

#### Step 2:
`celery -A worker worker --loglevel=info`

#### Step 1:
`uvicorn main:app --reload`