"""Module "config"."""

import os

SERVICE_NAME = "toaster.message-handling-service"

QUEUE_BROKER_IP = "172.18.0.40"

TOKEN: str = os.getenv("TOKEN")
GROUP_ID: int = int(os.getenv("GROUPID"))
API_VERSION: str = "5.199"


MY_SQL_HOST = os.getenv("SQL_HOST")
MY_SQL_PORT = int(os.getenv("SQL_PORT"))
MY_SQL_USER = os.getenv("SQL_USER")
MY_SQL_PSWD = os.getenv("SQL_PSWD")
