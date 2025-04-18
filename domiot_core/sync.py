import urllib.request
import json
import os
from typing import List, Dict
from database import User
from sqlite3 import Cursor

example = '{"result":"ok","data":{"users":[{"username":"ha","name":"domiot","is_owner":true,"is_active":true,"local_only":false,"group_ids":["system-admin"]},{"username":"jbrel","name":"jbrel","is_owner":false,"is_active":true,"local_only":false,"group_ids":["system-users"]}]}}'

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
        
        return data['data']['users']
        


def fetch_users(db_cur: Cursor): 
    for user in fetch_raw_users():
        u = User(
            username=user['username'],
            name=user['name'],
            is_owner=user['is_owner'],
            is_active=user['is_active'],
            local_only=user['local_only'],
            domiot_role="zero",  # Default role for all users
        )
        
        # Create the user if it doesn't exist, update if it does
        db_cur.execute("SELECT * FROM users WHERE username=?", (u.username,))
        row = db_cur.fetchone()

        if row is None:
            db_cur.execute('''
                INSERT INTO users (username, name, is_owner, is_active, local_only, domiot_role)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (u.username, u.name, u.is_owner, u.is_active, u.local_only, u.domiot_role))
        else:
            db_cur.execute('''
                UPDATE users
                SET name=?, is_owner=?, is_active=?, local_only=?, domiot_role=?
                WHERE username=?
            ''', (u.name, u.is_owner, u.is_active, u.local_only, u.domiot_role, u.username))

    return True