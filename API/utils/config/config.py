# config.py

import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://musictreeadmin:AxpHDxGS2BcFdaf@musictree-server.postgres.database.azure.com:5432/postgres?sslmode=require"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
