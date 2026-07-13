import logging
import requests

from config import settings

logger = logging.getLogger(__name__)


class N8NService:

    @staticmethod
    def create_ticket(ticket_data: dict):

        try:
            response = requests.post(
                settings.N8N_WEBHOOK_URL,
                json=ticket_data,
                timeout=15
            )

            response.raise_for_status()

            logger.info("Ticket sent to n8n successfully.")

            try:
                data = response.json()
            except ValueError:
                data = {
                    "message": response.text
                }

            return {
                "success": True,
                "status_code": response.status_code,
                "response": data
            }

        except requests.exceptions.RequestException as e:

            logger.exception("Failed to send ticket to n8n.")

            return {
                "success": False,
                "error": str(e)
            }