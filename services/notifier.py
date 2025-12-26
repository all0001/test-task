import logging
import smtplib
from abc import ABC, abstractmethod
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass


class TelegramNotifier(Notifier):
    def __init__(self, api_url: str, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"{api_url}/bot{token}/sendMessage"

    def send(self, message: str) -> None:
        try:
            response = requests.post(
                self.base_url,
                json={"chat_id": self.chat_id, "text": message},
                timeout=10,
            )
            response.raise_for_status()
            logger.info(f"Telegram notification sent: {message[:50]}...")
        except Exception as e:
            logger.error(f"Telegram send error: {e}")


class EmailNotifier:
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        sender: str,
        password: str,
        recipient: str,
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender = sender
        self.password = password
        self.recipient = recipient

    def send_with_attachment(
        self, filename: str, subject: Optional[str] = None
    ) -> None:
        logger.info(f"Sending email with attachment: {filename}")
        subject = subject or f'Report - {datetime.now().strftime("%Y-%m-%d")}'

        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = self.recipient
        msg["Subject"] = subject

        with open(filename, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={filename}")
            msg.attach(part)

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender, self.password)
            server.send_message(msg)

        logger.info("Email sent successfully")
