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
    fetch_raw_users()
    return {"status": "ok", "message": "Sync started"}

@app.get("/users")
def list_users():
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    users = []
    for row in rows:
        user = User(
            username=row[1],
            name=row[2],
            is_owner=row[3],
            is_active=row[4],
            local_only=row[5],
            domiot_role=row[6]
        )
        users.append(user)
    return users



@app.get("/users/{username}")
def get_user(username: str):

    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    if row is None:
        return {"status": "error", "message": "User not found"}
    user = User(
        username=row[1],
        name=row[2],
        is_owner=row[3],
        is_active=row[4],
        local_only=row[5],
        domiot_role=row[6]
    )
    return user