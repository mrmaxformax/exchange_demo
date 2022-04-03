import logging
import os


LOG_FORMAT_STRING = "%(asctime)s: %(levelname)s: %(message)s -- File: %(filename) s -> %(funcName) s() -> %(lineno)d"
LOG_DATE_FORMAT = "%m-%d-%Y %I:%M:%S %p"

logging.getLogger("faker").setLevel(logging.ERROR)
logging.getLogger("boto3").setLevel(logging.ERROR)

log_file_path = f"{os.getcwd()}/reports/log_report.log"
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

LOG = logging.getLogger("API Testing Framework")
LOG.setLevel(logging.DEBUG)
formatter = logging.Formatter(LOG_FORMAT_STRING)

# create file handler which logs even debug messages
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# create console handler with a higher log level
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

# add the handlers to the logger
LOG.addHandler(file_handler)
LOG.addHandler(stream_handler)
