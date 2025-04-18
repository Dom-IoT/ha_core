import urllib.request
import json
import os
from typing import List, Dict
from database import User
from sqlite3 import Cursor

API_URL = 'http://supervisor/auth/list'
SUPERVISOR_TOKEN = os.getenv("SUPERVISOR_TOKEN")


def fetch_raw_users() -> List[dict]:
    if not SUPERVISOR_TOKEN:
        raise ValueError("SUPERVISOR_TOKEN environment variable is not set")

    # Get the SUPERVISOR_TOKEN in the env
    r = urllib.request.Request(API_URL)
    r.add_header("Authorization", f"Bearer {SUPERVISOR_TOKEN}")
    r.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(r) as response:
        if response.status != 200:
            raise Exception(f"Failing to fetch users: {response.status}")

        data = json.loads(response.read().decode())
        if data['result'] != 'ok':
            raise Exception(f"Failing to fetch users: {data['result']}")
        

        # Debugging output
        print("Fetching users from Supervisor API")
        print(f"Total users: {len(data['data']['users'])}")
        for user in data['data']['users']:
            print("User:", user['username'])   
        return data['data']['users']


def fetch_users(db_cur: Cursor) -> bool:
    for user in fetch_raw_users():
        u = User(
            username=user['username'],
            name=user['name'],
            is_owner=user['is_owner'],
            is_active=user['is_active'],
            local_only=user['local_only'],
            group_ids=user['group_ids'],
            domiot_role="zero"  # Default role for all users
        )
        
        # Check if the user already exists in the database
        db_cur.execute("SELECT * FROM users WHERE username = ?", (user['username'],))
        existing_user = db_cur.fetchone()

        if existing_user:
            print(f"User {user['username']} already exists, updating...")
            # Update all the fields of the existing user (except the domiot_role)
            db_cur.execute(
                "UPDATE users SET name = ?, is_owner = ?, is_active = ?, local_only = ? WHERE username = ?",
                (user['name'], user['is_owner'], user['is_active'], user['local_only'], user['username'])
            )
        
        else:
            print(f"User {user['username']} does not exist, creating...")
            # Insert the new user into the database with the default domiot_role
            # Note: The domiot_role is set to "zero" by default
            db_cur.execute(
                "INSERT INTO users (username, name, is_owner, is_active, local_only,  domiot_role) VALUES (?, ?, ?, ?, ?, ?)",
                (user['username'], user['name'], user['is_owner'], user['is_active'], user['local_only'], "zero")
            )

    # Commit the changes to the database
    db_cur.connection.commit()
    return True
