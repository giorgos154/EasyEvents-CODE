from src.db_connection import get_db_connection
import pymysql

class InviteFriends:
    def load_friends(self, user_id):
        conn = get_db_connection()
        if not conn:
            print("No database connection")
            return []

        try:
            with conn.cursor() as cursor:
                query = """
                        SELECT u.username, u.user_id,
                               ui.first_name, ui.last_name
                        FROM users u
                        JOIN user_info ui ON u.user_id = ui.user_id
                        JOIN friendships f ON 
                            (u.user_id = f.user1_id AND f.user2_id = %s)
                            OR (u.user_id = f.user2_id AND f.user1_id = %s)
                        WHERE u.user_id != %s
                        ORDER BY ui.first_name, ui.last_name
                        """
                cursor.execute(query, (user_id, user_id, user_id))
                friends = cursor.fetchall()
                return friends
        except pymysql.Error as e:
            print(f"Database Error in InviteFriends.load_friends: {e}")
            return []
        finally:
            conn.close()

    def send_invites(self, selected_friends, event_id, message, sender_id):
        conn = get_db_connection()
        if not conn:
            print("No database connection")
            return False

        try:
            with conn.cursor() as cursor:
                for username in selected_friends:
                    # Get user_id for the friend
                    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
                    friend = cursor.fetchone()
                    if friend:
                        # Create invitation record
                        cursor.execute("""
                            INSERT INTO invitations (event_id, sender_userid, receipient_userid, sender_message, status)
                            VALUES (%s, %s, %s, %s, 'pending')
                        """, (event_id, sender_id, friend['user_id'], message))
            
            conn.commit()
            return True
        except pymysql.Error as e:
            print(f"Database Error in InviteFriends.send_invites: {e}")
            return False
        finally:
            conn.close()

    def load_user_invites(self, user_id):
        """Get all pending invites for a user"""
        conn = get_db_connection()
        if not conn:
            print("No database connection")
            return []

        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT i.invitation_id, i.event_id, i.sender_userid,
                           u.username AS from_username,
                           CONCAT(ui.first_name, ' ', ui.last_name) AS from_name,
                           e.title AS event_title,
                           e.event_date, e.venue AS event_location,
                           i.sender_message AS message,
                           i.status
                    FROM invitations i
                    JOIN users u ON i.sender_userid = u.user_id
                    JOIN user_info ui ON u.user_id = ui.user_id
                    JOIN events e ON i.event_id = e.event_id
                    WHERE i.receipient_userid = %s
                    AND i.status = 'pending'
                    AND e.status = 'scheduled'
                """
                cursor.execute(query, (user_id,))
                return cursor.fetchall()
        except pymysql.Error as e:
            print(f"Database Error in InviteFriends.load_user_invites: {e}")
            return []
        finally:
            conn.close()

    def accept_invite(self, invitation_id):
        """Accept an invitation and return the event_id"""
        conn = get_db_connection()
        if not conn:
            print("No database connection")
            return None

        try:
            with conn.cursor() as cursor:
                # Update status
                cursor.execute(
                    "UPDATE invitations SET status = 'accepted' WHERE invitation_id = %s",
                    (invitation_id,)
                )
                # Get event_id for redirection
                cursor.execute(
                    "SELECT event_id FROM invitations WHERE invitation_id = %s",
                    (invitation_id,)
                )
                result = cursor.fetchone()
                conn.commit()
                return result['event_id'] if result else None
        except pymysql.Error as e:
            print(f"Database Error in InviteFriends.accept_invite: {e}")
            return None
        finally:
            conn.close()

    def reject_invite(self, invitation_id):
        """Reject an invitation"""
        conn = get_db_connection()
        if not conn:
            print("No database connection")
            return False

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE invitations SET status = 'rejected' WHERE invitation_id = %s",
                    (invitation_id,)
                )
                conn.commit()
                return True
        except pymysql.Error as e:
            print(f"Database Error in InviteFriends.reject_invite: {e}")
            return False
        finally:
            conn.close()
