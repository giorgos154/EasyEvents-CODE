from src.db_connection import get_db_connection
from datetime import datetime
import qrcode

class EventParticipation:
    """
    EventParticipation: Handles event participation, check-ins, and tickets
    """
    def __init__(self, event_id, user_id, status='registered'):
        self.event_id = event_id
        self.user_id = user_id
        self.status = status

    def check_in(self):
        """Record check-in"""
        conn = get_db_connection()
        if not conn:
            return False, "Database connection failed"

        try:
            cursor = conn.cursor()
            query = """
                UPDATE event_participations 
                SET status = 'checkedIn'
                WHERE event_id = %s AND user_id = %s
                AND status = 'registered'
            """
            cursor.execute(query, (self.event_id, self.user_id))
            conn.commit()
            
            if cursor.rowcount > 0:
                return True, "Check-in successful"
            return False, "Could not check in. Please verify registration."
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

    def register(self):
        """Register for event"""
        conn = get_db_connection()
        if not conn:
            return False, "Database connection failed"

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO event_participations 
                (user_id, event_id, status)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (self.user_id, self.event_id, self.status))
            conn.commit()
            return True, "Successfully registered"
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def find_by_event_user(cls, event_id, user_id):
        """Find participation record"""
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = """
                SELECT * FROM event_participations
                WHERE event_id = %s AND user_id = %s
            """
            cursor.execute(query, (event_id, user_id))
            result = cursor.fetchone()
            if result:
                return cls(
                    event_id=result['event_id'],
                    user_id=result['user_id'],
                    status=result['status']
                )
            return None
        finally:
            cursor.close()
            conn.close()

    def generate_ticket(self):
        """Generate QR code ticket"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data("https://github.com/giorgos154/EasyEvents-CODE")
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white")

    def get_ticket_info(self):
        """Get ticket details"""
        from src.classes.event.event import Event
        from src.classes.member.member import Member
        
        event = Event.find_by_id(self.event_id)
        attendee = Member.get_name_by_id(self.user_id)
        return {
            'event_title': event.title,
            'event_date': event.event_date,
            'venue': event.venue,
            'attendee': attendee,
        'check_in_time': datetime.now()
        }

    def rate_event(self, event_rating, organizer_rating, comment):
        """
        Prosthiki vathmologias kai sxoliwn gia to event me validation
        """
        # Validate inputs
        if not isinstance(event_rating, int) or not isinstance(organizer_rating, int):
            return False, "Please provide a valid rating and review"
            
        if event_rating < 1 or event_rating > 5 or organizer_rating < 1 or organizer_rating > 5:
            return False, "Please provide a valid rating and review"
            
        if not comment or len(comment.strip()) == 0:
            return False, "Please provide a valid rating and review"

        conn = get_db_connection()
        if not conn:
            return False, "Database connection failed"

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ratings (event_id, user_id, organizer_rating, event_rating, comment)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    self.event_id,
                    self.user_id,
                    organizer_rating,
                    event_rating,
                    comment
                ))
                conn.commit()
                return True, "Success! Your review has been submitted"
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()
            
    @staticmethod
    def get_unrated_events(user_id):
        """
        Epistrefi ola ta events pou o xristis exei symmetasxei alla den exei vathmologisei akoma
        """
        conn = get_db_connection()
        if not conn:
            return []

        try:
            with conn.cursor() as cursor:
                query = """
                SELECT e.event_id, e.title, e.event_date, e.venue
                FROM events e
                JOIN event_participations ep ON e.event_id = ep.event_id
                WHERE ep.user_id = %s
                AND NOT EXISTS (
                    SELECT 1 FROM ratings r
                    WHERE r.event_id = e.event_id AND r.user_id = %s
                )
                ORDER BY e.event_date DESC;
                """
                cursor.execute(query, (user_id, user_id))
                return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
