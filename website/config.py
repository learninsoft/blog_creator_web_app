import os

BASE_DIR = os.getcwd()

class Config:
    DB_TYPE = "sqlite"
    DB_NAME = os.path.join(BASE_DIR,"database.db")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///" + DB_NAME
    LOGFILE = os.path.join(BASE_DIR, "application_logs.log")
