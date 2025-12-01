"""
Persistent session storage using SQLite.
"""
import sqlite3
import json
import time
import uuid
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class PersistentSessionService:
    """Session service with SQLite persistence."""

    def __init__(self, db_path: str = "data/sessions.db"):
        self.db_path = db_path
        self._init_db()
        logger.info(f"Initialized persistent session storage at {db_path}")

    def _init_db(self):
        """Initialize database schema."""
        import os
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                created_at REAL NOT NULL,
                last_accessed REAL NOT NULL,
                context TEXT
            )
        """)

        # User profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                platforms TEXT,
                total_activities INTEGER DEFAULT 0,
                skill_level TEXT,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def create(self, user_id: str) -> Dict:
        """Create a new session."""
        session_id = str(uuid.uuid4())
        now = time.time()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO sessions (session_id, user_id, created_at, last_accessed, context)
            VALUES (?, ?, ?, ?, ?)
        """, (session_id, user_id, now, now, json.dumps([])))

        conn.commit()
        conn.close()

        logger.info(f"Created session {session_id} for user {user_id}")
        return {"session_id": session_id}

    def get(self, session_id: str) -> Optional[Dict]:
        """Get session by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT session_id, user_id, created_at, last_accessed, context
            FROM sessions WHERE session_id = ?
        """, (session_id,))

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return {
            "session_id": row[0],
            "user_id": row[1],
            "created_at": row[2],
            "last_accessed": row[3],
            "context": json.loads(row[4])
        }

    def update_context(self, session_id: str, item: Dict) -> bool:
        """Update session context."""
        session = self.get(session_id)
        if not session:
            return False

        context = session["context"]
        context.append(item)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE sessions
            SET context = ?, last_accessed = ?
            WHERE session_id = ?
        """, (json.dumps(context), time.time(), session_id))

        conn.commit()
        conn.close()

        logger.info(f"Updated context for session {session_id}")
        return True

    def update_user_profile(self, user_id: str, profile_data: Dict):
        """Update or create user profile."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = time.time()

        cursor.execute("""
            INSERT OR REPLACE INTO user_profiles
            (user_id, platforms, total_activities, skill_level, created_at, updated_at)
            VALUES (?, ?, ?, ?, COALESCE((SELECT created_at FROM user_profiles WHERE user_id = ?), ?), ?)
        """, (
            user_id,
            json.dumps(profile_data.get('platforms', [])),
            profile_data.get('total_activities', 0),
            profile_data.get('skill_level', 'Unknown'),
            user_id,
            now,
            now
        ))

        conn.commit()
        conn.close()

        logger.info(f"Updated profile for user {user_id}")

    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Get user profile."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_id, platforms, total_activities, skill_level, created_at, updated_at
            FROM user_profiles WHERE user_id = ?
        """, (user_id,))

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return {
            "user_id": row[0],
            "platforms": json.loads(row[1]),
            "total_activities": row[2],
            "skill_level": row[3],
            "created_at": row[4],
            "updated_at": row[5]
        }
