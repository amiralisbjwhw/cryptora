import os

class Config:
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "amir-secret-key")
    DATABASE_PATH = os.path.join(os.getcwd(), "database.db")
import os

class Config:
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "amir-secret-key")
    DATABASE_PATH = os.path.join(os.getcwd(), "database.db")
    PORT = int(os.getenv("PORT", 10000))
    LOGGING_ENABLED = True
    ALLOWED_HOSTS = ["*"]  # برای آینده اگه خواستی محدود کنی
