import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-super-secret")
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DB = os.environ.get("MYSQL_DB", "university_portal")
    MYSQL_CURSORCLASS = "DictCursor"
