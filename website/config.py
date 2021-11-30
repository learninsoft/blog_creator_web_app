import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "application_logs")
os.makedirs(LOG_DIR, exist_ok=True)


class Config:
    DB_TYPE = "sqlite"
    DB_NAME = os.path.join(BASE_DIR, "database.db")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + DB_NAME
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    LOGFILE = os.path.join(LOG_DIR, "application_logs.log")
