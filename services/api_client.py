from typing import Dict, Any
import requests
import logging

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url: str, api_key: str, timeout: int = 30):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout

    def fetch_report(self) -> Dict[str, Any]:
        logger.info("Fetching report from API")
        response = requests.get(
            self.base_url,
            headers={'X-API-Key': self.api_key},
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
