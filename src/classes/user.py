from src.db_connection import get_db_connection
from typing import Optional


class User:
    def __init__(self, user_id, username, role):
       
        self.user_id = user_id
        self.username = username
        self.role = role

    @staticmethod
    def load_from_db(username: str) -> Optional["User"]:
        conn = get_db_connection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT user_id, username, role "
                    "FROM users "
                    "WHERE username = %s",
                    (username,)
                )
                row = cursor.fetchone()
                if row:
                    return User(
                        user_id = row["user_id"],
                        username= row["username"],
                        role    = row["role"]
                    )
        finally:
            conn.close()

    @classmethod
    def get_name_by_id(cls, user_id: int) -> str:
        """
        Epistrefei to username enos xristi me vasi to ID tou.
        """
        conn = get_db_connection()
        if conn is None:
            return "Unknown"

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT username, first_name, last_name
                    FROM users 
                    LEFT JOIN user_info ON users.user_id = user_info.user_id
                    WHERE users.user_id = %s
                    """, 
                    (user_id,)
                )
                result = cursor.fetchone()
                if result:
                    if result.get('first_name') and result.get('last_name'):
                        return f"{result['first_name']} {result['last_name']}"
                    return result['username']
                return "Unknown"
        finally:
            conn.close()

        return None

    @staticmethod
    def verify_credentials(username: str, password: str, role: str) -> bool:
        print(f"[DEBUG] verify_credentials called -> username={username!r}, role={role!r}")
        conn = get_db_connection()
        if conn is None:
            print("[DEBUG] get_db_connection() returned None")
            return False

        try:
            with conn.cursor() as cursor:
                sql = (
                    "SELECT COUNT(*) AS cnt "
                    "FROM users "
                    "WHERE username = %s AND password = %s AND role = %s"
                )
                params = (username, password, role)
                cursor.execute(sql, params)
                row = cursor.fetchone()
                ok = bool(row and row.get("cnt", 0) > 0)
                return ok

        except Exception as e:
            print(f"[ERROR] Exception in verify_credentials: {e!r}")
            return False

        finally:
            conn.close()
