from fastapi import FastAPI, Request
import os
import sqlite3
from database import init_db, User, UserRole
from sync import fetch_users
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse



init_db()

con = sqlite3.connect("/data/db.sqlite3", check_same_thread=False)
cur = con.cursor()

app = FastAPI()
app.mount('/static', StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
@app.post("/")
async def hello(request: Request):
    if request.method == "POST":
        form = await request.form()
        for key, new_role in form.items():
            if "__" in key:
                username, _ = key.rsplit("__", 1)
                cur.execute("SELECT * FROM users WHERE username=?", (username,))
                row = cur.fetchone()
                if row is None:
                    raise ValueError(f"User {username} not found")
                
                user = User(
                    username=row[1],
                    name=row[2],
                    is_owner=row[3],
                    is_active=row[4],
                    local_only=row[5],
                    domiot_role=row[6]
                )
                if new_role not in UserRole.list():
                    raise ValueError(f"Invalid role {new_role}")

                # Update the user role
                user.domiot_role = UserRole(new_role)

                print(f"Updating user {user.username} to role {user.domiot_role}")
                cur.execute('''
                    UPDATE users
                    SET domiot_role=?
                    WHERE username=?
                ''', (user.domiot_role, user.username))
                
                con.commit()



            else:
                raise ValueError(f"Invalid form")
    
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
        "domiot_roles": UserRole, 
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