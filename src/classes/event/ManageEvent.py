from src.db_connection import get_db_connection
import pymysql
from datetime import datetime

class ManageEvent:
    def __init__(self, current_user):
        self.current_user = current_user
        self.title = None
        self.description = None
        self.event_date = None
        self.venue = None
        self.is_public = True
        self.max_participants = None
        self.is_paid = False
        self.cost = 0.0
        self.payment_method = None
        self.status = 'scheduled'
        self.organizer_id = current_user.user_id
        self.category = "General" # Default category value

    def create_event(self):
        """
        Εισάγει τη νέα εκδήλωση στη βάση δεδομένων.
        """
        conn = get_db_connection()
        if not conn:
            return False, "Could not connect to database."

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO events (
                    organizer_id,
                    title,
                    description,
                    event_date,
                    venue,
                    is_public,
                    max_participants,
                    is_paid,
                    cost,
                    payment_method,
                    status,
                    category
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                self.organizer_id,
                self.title,
                self.description,
                self.event_date.strftime('%Y-%m-%d %H:%M:%S'),
                self.venue,
                int(self.is_public),
                self.max_participants,
                int(self.is_paid),
                self.cost,
                self.payment_method,
                self.status,
                self.category
            ))
            conn.commit()
            event_id = cursor.lastrowid  
            return True, event_id
        except Exception as e:
            return False, f"Database error: {e}"
        finally:
            cursor.close()
            conn.close()
