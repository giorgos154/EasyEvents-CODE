from db_connection import get_connection
from mysql.connector import Error

class EventDeletion:
    def delete_event(self, event_id, organizer_id):
        try:
            connection = get_connection()
            cursor = connection.cursor()

            # Έλεγχος αν το event ανήκει στον organizer
            cursor.execute(
                "SELECT id FROM events WHERE id = %s AND organizer_id = %s",
                (event_id, organizer_id)
            )
            event = cursor.fetchone()
            if not event:
                return "Error: Event not found or you don't have permission to delete it."

            # Διαγραφή συμμετεχόντων (αν υπάρχει πίνακας event_participants)
            cursor.execute("DELETE FROM event_participants WHERE event_id = %s", (event_id,))

            # Διαγραφή του event
            cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))

            connection.commit()
            return "Event deleted successfully."

        except Error as e:
            return f"Database error: {e}"

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
