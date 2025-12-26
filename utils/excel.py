from typing import List
import pandas as pd
import logging
from contextlib import contextmanager
import os

logger = logging.getLogger(__name__)


class ExcelManager:
    @staticmethod
    def create_excel(phones: List[str], filename: str) -> str:
        logger.info(f"Creating Excel file: {filename}")
        df = pd.DataFrame({'Phone Numbers': phones})
        df.to_excel(filename, index=False)
        return filename

    @staticmethod
    @contextmanager
    def temporary_excel(phones: List[str], filename: str):
        excel_file = ExcelManager.create_excel(phones, filename)

        try:
            yield excel_file
        finally:
            if os.path.exists(excel_file):
                os.remove(excel_file)
                logger.info(f"Removed tmp file: {excel_file}")
