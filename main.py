import logging

from config import Config
from services.api_client import APIClient
from services.notifier import EmailNotifier, TelegramNotifier
from services.report import ReportProcessor
from utils.excel import ExcelManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("script.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class ReportPipeline:
    def __init__(self, config: Config):
        self.config = config
        self.api_client = APIClient(config.api_url, config.api_key)
        self.telegram = TelegramNotifier(
            config.telegram_api_url,
            config.telegram_token,
            config.telegram_chat_id
        )
        self.email = EmailNotifier(
            config.smtp_server,
            config.smtp_port,
            config.email_sender,
            config.email_password,
            config.email_recipient,
        )
        self.processor = ReportProcessor()

    def execute(self) -> None:
        self.telegram.send("Script started")
        logger.info("Pipeline execution started")

        try:
            report = self.api_client.fetch_report()
            phones = self.processor.extract_unique_phones(report)
            print(f"unique phones: {phones}")
            with ExcelManager.temporary_excel(
                phones, self.config.excel_filename
            ) as excel_file:
                self.email.send_with_attachment(excel_file)

            logger.info("Pipeline completed successfully")
            self.telegram.send("Script completed successfully")

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            self.telegram.send(error_msg)
            raise


def main() -> None:
    config = Config.from_env()
    pipeline = ReportPipeline(config)
    pipeline.execute()


if __name__ == "__main__":
    main()
