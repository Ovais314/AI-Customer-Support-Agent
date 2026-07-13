import sqlite3
import logging
from datetime import datetime

from services.n8n_service import N8NService

logger = logging.getLogger(__name__)

DB_PATH = "database/chat_history.db"


class TicketService:

    @staticmethod
    def initialize():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            session_id TEXT,

            issue TEXT,

            status TEXT,

            priority TEXT,

            created_at TEXT

        )
        """)

        conn.commit()
        conn.close()


    @staticmethod
    def get_existing_open_ticket(session_id: str, issue: str):

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM tickets
            WHERE session_id = ?
            AND issue = ?
            AND status = 'OPEN'
            ORDER BY id DESC
            LIMIT 1
        """, (
            session_id,
            issue
        ))

        row = cursor.fetchone()

        conn.close()

        if row:
            return row[0]

        return None


    @staticmethod
    def create_ticket(session_id: str, issue: str):

        
        existing_ticket = TicketService.get_existing_open_ticket(
            session_id=session_id,
            issue=issue
        )

        if existing_ticket:
            logger.info(
                "Reusing existing open ticket #%s",
                existing_ticket
            )

            return {
                "ticket_id": existing_ticket,
                "created": False
            }


        created_at = datetime.now().isoformat()

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO tickets (
            session_id,
            issue,
            status,
            priority,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            session_id,
            issue,
            "OPEN",
            "NORMAL",
            created_at
        ))

        conn.commit()

        ticket_id = cursor.lastrowid

        conn.close()

        # Send ticket to n8n
        n8n_result = N8NService.create_ticket({
            "ticket_id": ticket_id,
            "session_id": session_id,
            "question": issue,
            "issue": issue,
            "status": "OPEN",
            "priority": "NORMAL",
            "created_at": created_at
        })

        if not n8n_result.get("success", False):
            logger.warning(
                "Ticket #%s was saved locally but failed to sync with n8n. Error: %s",
                ticket_id,
                n8n_result.get("error")
            )
        else:
            logger.info(
                "Ticket #%s synced successfully with n8n.",
                ticket_id
            )

        return {
            "ticket_id": ticket_id,
            "created": True
        }