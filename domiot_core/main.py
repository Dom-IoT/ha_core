from fastapi import FastAPI, Request
import sqlite3
from database import init_db, User
from sync import fetch_users
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles




init_db()

con = sqlite3.connect("db.sqlite3", check_same_thread=False)
cur = con.cursor()

app = FastAPI()
app.mount('/static', StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def hello(request: Request):
    fetch_users(cur)
    users = []
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
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
    
    context = {
        "user": request.headers.get("X-Remote-User-Display-Name"),
        "users": users
    }
    return templates.TemplateResponse(request, "index.html", context=context)

@app.post("/sync")
def manual_sync():
    fetch_users(cur)
    return {"status": "ok", "message": "Sync started"}


@app.get("/api/users/{username}")
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