import logging
from typing import Any

import requests

from config import config

logger = logging.getLogger(__name__)


class BaseAPIService:
    host: str
    timeout: int
    headers: dict[str, str] = {}
    endpoint = ""

    def authorize(self, **kwargs) -> None:
        pass

    def prepare_request_data(self, **kwargs) -> dict[str, Any]:
        return kwargs

    def finalize_response(self, response: requests.Response) -> dict[str, Any]:
        response.raise_for_status()
        return response.json()

    def _make_request(self, method: str = "GET", **kwargs) -> requests.Response:
        self.authorize(**kwargs)
        url = self.host + self.endpoint
        print(f"url: {self.host}")
        request_data = self.prepare_request_data(**kwargs)

        logger.info(f"Making {method} request to {url}")
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            timeout=self.timeout,
            **request_data,
        )
        return response


class ReportService(BaseAPIService):
    host = config.api_url
    endpoint = "/test_report_dev/test_report"
    api_key = config.api_key
    timeout = 30

    def authorize(self, **kwargs) -> None:
        self.headers["X-API-Key"] = self.api_key

    def fetch_report(self) -> dict[str, Any]:
        logger.info("Fetching report")
        response = self._make_request(method="GET")
        return self.finalize_response(response)
