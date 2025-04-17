import fastapi
import sqlite3
from database import init_db, User
from sync import fetch_raw_users


init_db()

con = sqlite3.connect("db.sqlite3", check_same_thread=False)
cur = con.cursor()

app = fastapi.FastAPI()


@app.get("/")
def hello():
    return {"status": "ok"}


@app.post("/sync")
def manual_sync():
    return fetch_raw_users()

