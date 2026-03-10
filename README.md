# FastAPI Sample Project

This repository contains a minimal production-grade FastAPI application using SQLite as a database.  
It features:

- **SQLite database** with two tables (`customers`, `orders`) seeded with example data
- **User authentication** (simple session-based login)
- **Front-end** powered by Jinja2 templates
- **Dashboard** showing joined data with columns: `Name`, `Age`, `Country`, `Item`, `Amount`, `Shipping Status`

## Getting Started

1. **Clone the repository (if not already).**
2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate    # on Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```
4. **Open your browser** at `http://127.0.0.1:8000`.  
   Login with `admin` / `password` (created automatically on startup).

## Database

The SQLite database file (`app.db`) is created automatically in the project root.  
If you want to reset the data, simply delete `app.db` and restart the server.

## Notes
- The seed data was modelled after a Programiz example showing a customer–orders relationship. A CSV file (`data/programiz_sample.csv`) holds the same sample and is loaded on first startup.
- For production deployment you should replace the simple session middleware secret key, configure environment variables appropriately, and consider using migrations (Alembic) along with a more robust authentication system.

## Docker

A `Dockerfile` is included for containerized deployment:

```bash
# build image
docker build -t fastapi-sample .
# run container
docker run -p 8000:8000 fastapi-sample
```

---

Feel free to expand or refactor as needed.