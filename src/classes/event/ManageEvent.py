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
        self.organizer_id = current_user.user_id if current_user else None
        self.category = "General"  # Default category value

    def create_event(self):
        """
        Eisagei ti nea ekdilwsi sti vasi dedomenon.
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

    def edit_event(self):
        """
        Enimerwnei ta stoixeia tis ekdilwsis sti vasi.
        """
        conn = get_db_connection()
        if not conn:
            return False, "Could not connect to database."

        try:
            cursor = conn.cursor()
            query = """
                UPDATE events SET
                    title = %s,
                    description = %s,
                    category = %s,
                    event_date = %s,
                    venue = %s,
                    is_public = %s,
                    max_participants = %s,
                    is_paid = %s,
                    cost = %s,
                    status = %s
                WHERE event_id = %s
            """
            cursor.execute(query, (
                self.title,
                self.description,
                self.category,
                self.event_date.strftime('%Y-%m-%d %H:%M:%S'),
                self.venue,
                int(self.is_public),
                self.max_participants,
                int(self.is_paid),
                self.cost,
                self.status,
                self.event_id
            ))
            conn.commit()
            return True, ""
        except Exception as e:
            return False, f"Database error: {e}"
        finally:
            cursor.close()
            conn.close()

    def cancel_event(self, event_id, organizer_id):
        """
        Akyrwnei mia ekdilwsi kai diagrafei ola ta sxetika dedomena
        """
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            if connection is None:
                return "Error: Could not connect to the database."
            
            cursor = connection.cursor()

            # Elegxos an to event anikei ston organizer
            cursor.execute(
                "SELECT event_id FROM events WHERE event_id = %s AND organizer_id = %s",
                (event_id, organizer_id)
            )
            event = cursor.fetchone()
            if not event:
                return "Error: Event not found or you don't have permission to cancel it."

            # Diagrafi sxetikwn dedomenon
            cursor.execute("DELETE FROM event_participations WHERE event_id = %s", (event_id,))
            cursor.execute("DELETE FROM discussions WHERE event_id = %s", (event_id,))
            cursor.execute("DELETE FROM ratings WHERE event_id = %s", (event_id,))
            cursor.execute("DELETE FROM invitations WHERE event_id = %s", (event_id,))
            cursor.execute("DELETE FROM points WHERE event_id = %s", (event_id,))

            # Diagrafi tou event
            cursor.execute("DELETE FROM events WHERE event_id = %s", (event_id,))

            connection.commit()
            return "Event cancelled successfully."

        except Exception as e:
            return f"Database error: {e}"

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
