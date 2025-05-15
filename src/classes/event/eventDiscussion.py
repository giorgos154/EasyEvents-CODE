from src.db_connection import get_db_connection

class EventDiscussion:
    def __init__(self, event_id):
        self.event_id = event_id
    
    def load_messages(self):
        """Load all messages for an event"""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT d.message_text, d.timestamp, u.username
                    FROM discussions d
                    JOIN users u ON d.user_id = u.user_id
                    WHERE d.event_id = %s
                    ORDER BY d.timestamp ASC
                """, (self.event_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Database Error in EventDiscussion.load_messages: {e}")
            return []
        finally:
            conn.close()

    def add_message(self, user_id, message):
        """Add a new message to the discussion"""
        if not message.strip():
            return False
            
        conn = get_db_connection()
        if not conn:
            return False

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO discussions (event_id, user_id, message_text)
                    VALUES (%s, %s, %s)
                """, (self.event_id, user_id, message.strip()))
                conn.commit()
                return True
        except Exception as e:
            print(f"Database Error in EventDiscussion.add_message: {e}")
            return False
        finally:
            conn.close()
