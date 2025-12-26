import logging
import os
from contextlib import contextmanager
from typing import Generator

import pandas as pd

logger = logging.getLogger(__name__)


class ExcelManager:
    @staticmethod
    def create_excel(phones: list[str], filename: str) -> str:
        logger.info(f"Creating Excel file: {filename}")
        df = pd.DataFrame({"Phone Numbers": phones})
        df.to_excel(filename, index=False)
        return filename

    @staticmethod
    @contextmanager
    def temporary_excel(phones: list[str], filename: str) -> Generator[str, None, None]:
        excel_file = ExcelManager.create_excel(phones, filename)

        try:
            yield excel_file
        finally:
            if os.path.exists(excel_file):
                os.remove(excel_file)
                logger.info(f"Removed tmp file: {excel_file}")
