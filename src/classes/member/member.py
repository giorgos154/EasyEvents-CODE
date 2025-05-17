from src.db_connection import get_db_connection
from datetime import datetime
from typing import Optional, List, Dict


class Member:
    """
    Base class for all users. Handles authentication and basic data loading.
    """
    def __init__(self, user_id: int, username: str, role: str):
        self.user_id = user_id
        self.username = username
        self.role = role

    @staticmethod
    def verify_credentials(username: str, password: str, role: str) -> bool:
        """
        Verify a user's credentials against the database.
        """
        conn = get_db_connection()
        if conn is None:
            return False

        try:
            with conn.cursor() as cursor:
                sql = (
                    "SELECT COUNT(*) AS cnt "
                    "FROM users "
                    "WHERE username = %s AND password = %s AND role = %s"
                )
                cursor.execute(sql, (username, password, role))
                row = cursor.fetchone()
                return bool(row and row.get("cnt", 0) > 0)
        except Exception as e:
            print(f"[ERROR] Exception in verify_credentials: {e!r}")
            return False
        finally:
            conn.close()

    @staticmethod
    def load_from_db(username: str) -> Optional["Member"]:
        """
        Load a Member or User instance from the database by username.
        """
        conn = get_db_connection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT user_id, username, role, email "
                    "FROM users "
                    "WHERE username = %s",
                    (username,)
                )
                row = cursor.fetchone()
                if not row:
                    return None

                if row["role"] == "attendee":
                    # Instantiate a full User subclass
                    return User(
                        user_id=row["user_id"],
                        username=row["username"],
                        email=row.get("email", ""),
                        role=row["role"]
                    )
                # Other roles remain as base Member
                return Member(
                    user_id=row["user_id"],
                    username=row["username"],
                    role=row["role"]
                )
        finally:
            conn.close()

    @classmethod
    def get_name_by_id(cls, user_id: int) -> str:
        """
        Return the display name for a user by ID
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
                    LEFT JOIN user_info USING(user_id)
                    WHERE user_id = %s
                    """,
                    (user_id,)
                )
                result = cursor.fetchone()
                if not result:
                    return "Unknown"

                first = result.get("first_name")
                last = result.get("last_name")
                if first and last:
                    return f"{first} {last}"
                return result.get("username", "Unknown")
        finally:
            conn.close()


class User(Member):
    """
    Subclass of Member with extended profile information and past events.
    """
    def __init__(self, user_id: int, username: str, email: str, role: str = 'attendee'):
        super().__init__(user_id, username, role)
        self.email = email

    def load_user_info(self) -> Optional[Dict[str, str]]:
        """
        Fetch the detailed profile information for this user.
        Returns a dict of fields or None if not found.
        """
        conn = get_db_connection()
        if conn is None:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT first_name,
                           last_name,
                           date_of_birth,
                           phone_number,
                           address_street,
                           address_city,
                           address_postal_code
                    FROM user_info
                    WHERE user_id = %s
                    """,
                    (self.user_id,)
                )
                row = cursor.fetchone()
                if not row:
                    return None

                return {
                    "First Name": row["first_name"],
                    "Last Name": row["last_name"],
                    "Date of Birth": row["date_of_birth"].strftime("%Y-%m-%d")
                                         if isinstance(row["date_of_birth"], datetime) else row["date_of_birth"],
                    "Phone Number": row["phone_number"],
                    "Street Address": row["address_street"],
                    "City": row["address_city"],
                    "Postal Code": row["address_postal_code"]
                }
        except Exception as e:
            print(f"[ERROR] Failed to load user data: {e}")
            return None
        finally:
            conn.close()

    def update_user_info(self, user_data: Dict[str, str]) -> bool:
        """
        Update this user's profile information in the database.
        """
        conn = get_db_connection()
        if conn is None:
            return False

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE user_info
                    SET first_name = %s,
                        last_name = %s,
                        date_of_birth = %s,
                        phone_number = %s,
                        address_street = %s,
                        address_city = %s,
                        address_postal_code = %s
                    WHERE user_id = %s
                    """,
                    (
                        user_data.get("First Name"),
                        user_data.get("Last Name"),
                        user_data.get("Date of Birth"),
                        user_data.get("Phone Number"),
                        user_data.get("Street Address"),
                        user_data.get("City"),
                        user_data.get("Postal Code"),
                        self.user_id
                    )
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"[ERROR] Failed to update user data: {e}")
            return False
        finally:
            conn.close()

    def get_past_events(self) -> List[Dict[str, any]]:
        """
        Retrieve events this user has participated in that are before today.
        Returns a list of event dicts.
        """
        conn = get_db_connection()
        if conn is None:
            return []

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT e.event_id,
                           e.title,
                           e.event_date,
                           e.venue,
                           e.description,
                           e.category,
                           e.status
                    FROM events e
                    JOIN event_participations ep ON e.event_id = ep.event_id
                    WHERE ep.user_id = %s
                      AND e.event_date < CURDATE()
                    ORDER BY e.event_date DESC
                    """,
                    (self.user_id,)
                )
                return cursor.fetchall() or []
        except Exception as e:
            print(f"[ERROR] Error loading past events: {e}")
            return []
        finally:
            conn.close()

class Organizer(Member):
    """
    Subclass of Member for event organizers.
    Placeholder for class diagram.
    """
    def __init__(self, user_id: int, username: str, email: str, role: str = 'organizer'):
        super().__init__(user_id, username, role)
        self.email = email