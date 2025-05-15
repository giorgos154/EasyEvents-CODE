from db_connection import get_db_connection
from mysql.connector import Error

class EventDeletion:
    def delete_event(self, event_id, organizer_id):
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            if connection is None:
                return "Error: Could not connect to the database."
            
            cursor = connection.cursor()

            # Έλεγχος αν το event ανήκει στον organizer
            cursor.execute(
                "SELECT event_id FROM events WHERE event_id = %s AND organizer_id = %s",
                (event_id, organizer_id)
            )
            event = cursor.fetchone()
            if not event:
                return "Error: Event not found or you don't have permission to delete it."

            # Διαγραφή σχετικών δεδομένων
            cursor.execute("DELETE FROM event_participations WHERE event_id = %s", (event_id,))
            cursor.execute("DELETE FROM discussions WHERE event_id = %s", (event_id,))
            cursor.execute("DELETE FROM ratings WHERE event_id = %s", (event_id,))
            cursor.execute("DELETE FROM invitations WHERE event_id = %s", (event_id,))
            cursor.execute("DELETE FROM points WHERE event_id = %s", (event_id,))

            # Διαγραφή του event
            cursor.execute("DELETE FROM events WHERE event_id = %s", (event_id,))

            connection.commit()
            return "Event deleted successfully."

        except Error as e:
            return f"Database error: {e}"

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

