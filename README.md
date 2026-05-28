# MedAgentCV
Intro to Artificial Intelligence Term Project

## Local setup

### 1) Create env file
Copy the example and fill in your OpenAI key:

```bash
copy .env.example .env
```

Then edit `.env` with your values.

### 2) Install dependencies
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

If you prefer a plain requirements install for a one-off run, use `pip install -r requirements.txt` after activating the environment.

### 3) Run the API
```bash
uvicorn app.main:app --reload
```

The API will be available at: http://127.0.0.1:8000

## Docker setup

### 1) Create env file
Copy the example and fill in your OpenAI key:

```bash
copy .env.example .env
```

Then edit `.env` with your values.

### 2) Build and run (Docker)
```bash
docker build -t medagentcv .
docker run --env-file .env -p 8000:8000 medagentcv
```

### 3) Docker Compose (optional)
```bash
docker compose up --build
```

### API usage
POST `/api/v1/analyze` (multipart/form-data):
- `image`: image file
- `disease_description`: text
