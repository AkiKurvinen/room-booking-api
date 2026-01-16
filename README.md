# Room booking API 2026

## Features
- Book a room for timespan
- Cancel a room booking
- View all bookings for single room

## Installation

**Create and Activate Virtual Environment**

A. *Windows (Git Bash)*
```bash
python -m venv .venv
source .venv/Scripts/activate
```

B. *Windows (cmd or PowerShell)*
```bash
python -m venv .venv
.venv\Scripts\activate
```


**Install Dependencies**
```bash
pip install -r requirements.txt
```

**Initilize sqlite dev databse**  
```bash
python init_database.py
```

## Run project

```bash
uvicorn app.main:app --reload
```
- See API running [http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/)
- See API docs [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Tools & Tech
- Python FastAPI
- SQLite

## Additional dev tips

### SQLite database
Explore the SQLite database using the VS Code extension **SQLite** by alexcvzz:
1. Open the Command Palette (Shift+Ctrl+P).
2. Select `SQLite > Open Database` and choose `room_booking.db`.
3. Use `Shift+Ctrl+P` again and select `SQLite: Focus on Database View` to interact with the database tables and data.

### Fix "Import could not be resolved" Pylance warnings
Select Python Interpreter in VS Code:   
1. Open the Command Palette (Ctrl+Shift+P).
2. Search for "Python: Select Interpreter".
3. Choose the interpreter located in `.venv` (e.g., `.venv\Scripts\python.exe`).
