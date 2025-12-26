from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class ReportProcessor:
    @staticmethod
    def extract_unique_phones(report_data: Dict[str, Any]) -> List[str]:
        logger.info("Extracting unique phone numbers")
        phones = {
            item['msisdn']
            for item in report_data.get('data', {}).get('result', [])
        }
        logger.info(f"Found {len(phones)} unique phone numbers")
        return sorted(phones)
