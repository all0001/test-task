import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    api_url: str
    api_key: str
    smtp_server: str
    smtp_port: int
    email_sender: str
    email_password: str
    email_recipient: str
    telegram_token: str
    telegram_chat_id: str
    telegram_api_url: str = "https://api.telegram.org"
    excel_filename: str = "phones.xlsx"

    @classmethod
    @lru_cache(maxsize=1)
    def from_env(cls) -> "Config":
        return cls(
            api_url=os.getenv("API_URL", ""),
            api_key=os.getenv("API_KEY", ""),
            smtp_server=os.getenv("SMTP_SERVER", ""),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            email_sender=os.getenv("EMAIL_SENDER", ""),
            email_password=os.getenv("EMAIL_PASSWORD", ""),
            email_recipient=os.getenv("EMAIL_RECIPIENT", ""),
            telegram_token=os.getenv("TELEGRAM_TOKEN", ""),
            telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
            telegram_api_url=os.getenv("TELEGRAM_API_URL", "https://api.telegram.org"),
        )


config = Config.from_env()
