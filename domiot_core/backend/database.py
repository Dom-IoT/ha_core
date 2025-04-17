import os
import sqlite3
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    HEALTHCARE_STAFF = "healthcare_staff"
    TECHNICIAN = "technician"
    PATIENT = "patient"
    ZERO = "zero" # Default role for all users


class User(BaseModel):
    """
    User extended model for the Home Assistant user.
    """
    username: str
    name: str
    is_owner: bool
    is_active: bool
    local_only: bool
    group_ids: Optional[list[str]] = None
    # We extends the HomeAssistant User class with this property
    domiot_role: UserRole = UserRole.ZERO

class UserDTO(BaseModel):
    """
    User Data Transfer Object.
    """
    username: str


def init_db():
    if os.path.exists("db.sqlite3"):
        return
    open("db.sqlite3", "w").close()
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            is_owner BOOLEAN NOT NULL,
            is_active BOOLEAN NOT NULL,
            local_only BOOLEAN NOT NULL,
            domiot_role TEXT DEFAULT 'zero'
        )
    ''')
