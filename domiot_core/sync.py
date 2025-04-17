import urllib.request
import json
import os
from typing import List, Dict

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
        
