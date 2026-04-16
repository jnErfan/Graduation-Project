import os
from urllib.parse import urlparse


def parse_database_url(url):
    parsed = urlparse(url)
    return {
        "host": parsed.hostname or "127.0.0.1",
        "user": parsed.username or "root",
        "password": parsed.password or "",
        "db": parsed.path.lstrip("/") or "university_portal",
        "port": parsed.port or 3306,
    }


db_url = os.environ.get("DATABASE_URL") or os.environ.get("PRIVATE_DATABASE_URL")
if db_url:
    db_config = parse_database_url(db_url)
    MYSQL_HOST = db_config["host"]
    MYSQL_USER = db_config["user"]
    MYSQL_PASSWORD = db_config["password"]
    MYSQL_DB = db_config["db"]
    MYSQL_PORT = db_config["port"]
else:
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DB = os.environ.get("MYSQL_DB", "university_portal")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))

MYSQL_CURSORCLASS = "DictCursor"
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")


class Config:
    SECRET_KEY = SECRET_KEY
    MYSQL_HOST = MYSQL_HOST
    MYSQL_USER = MYSQL_USER
    MYSQL_PASSWORD = MYSQL_PASSWORD
    MYSQL_DB = MYSQL_DB
    MYSQL_PORT = MYSQL_PORT
    MYSQL_CURSORCLASS = MYSQL_CURSORCLASS
