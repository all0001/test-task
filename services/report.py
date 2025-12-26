import logging
from typing import Any

logger = logging.getLogger(__name__)


class ReportProcessor:
    @staticmethod
    def extract_unique_phones(report_data: dict[str, Any]) -> list[str]:
        logger.info("Extracting unique phone numbers")
        phones = {
            item["msisdn"] for item in report_data.get("data", {}).get("result", [])
        }
        logger.info(f"Found {len(phones)} unique phone numbers")
        return sorted(phones)
