# Room booking API 2026

## Features
- Book a room for timespan
- Cancel a room booking
- View all bookings for single room

## Installation

**Create and Activate Virtual Environment**

A. *Windows (Git Bash)*
```bash
cd cli
python -m venv .venv
source .venv/Scripts/activate
```

B. *Windows (cmd or PowerShell)*
```bash
cd cli
python -m venv .venv
.venv\Scripts\activate
```

**Install Dependencies**
```bash
pip install -r requirements.txt
```

## Run project

```bash
fastapi dev main.py
```

- See API running (http://127.0.0.1:8000/)[http://127.0.0.1:8000/]
- See API docs (http://127.0.0.1:8000/docs)[http://127.0.0.1:8000/docs]

## Tools & Tech
- Python FastAPI
- SQLite
