# src/db_connection.py
import os
from dotenv import load_dotenv
import pymysql

# load .env (DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
load_dotenv()

def get_db_connection():
    try:
        conn = pymysql.connect(
            host     = os.getenv("DB_HOST"),
            port     = int(os.getenv("DB_PORT", 3306)),
            user     = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            database = os.getenv("DB_NAME"),
            cursorclass = pymysql.cursors.DictCursor,
            autocommit = False
        )
        return conn
    except Exception as e:
        print(f"[db_connection] Connection error: {e}")
        return None
