# src/classes/event.py
from src.db_connection import get_db_connection
import pymysql
from datetime import datetime

class Event:
    """
    Event Class: Αντιπροσωπεύει μια εκδήλωση στο σύστημα.
    Περιλαμβάνει μεθόδους για διαχείριση δεδομένων εκδήλωσης στη βάση.
    """
    def __init__(self, event_id, organizer_id, title, description, category, event_date, venue,
                 is_public=True, max_participants=None, is_paid=False, cost=0.00,
                 payment_method=None, status='scheduled'):

        self.event_id = event_id
        self.organizer_id = organizer_id
        self.title = title
        self.description = description
        self.category = category
        if isinstance(event_date, str):
            try:
                self.event_date = datetime.strptime(event_date, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                self.event_date = event_date 
        else:
            self.event_date = event_date 
        self.venue = venue
        self.is_public = is_public
        self.max_participants = max_participants
        self.is_paid = is_paid
        self.cost = cost
        self.payment_method = payment_method
        self.status = status

    @classmethod
    def find_by_id(cls, event_id):
        """
        Βρίσκει μια εκδήλωση στη βάση δεδομένων με βάση το ID της.
        """
        conn = get_db_connection()
        event = None
        if not conn:
            return None  # Δεν έγινε σύνδεση με τη βάση

        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = """
                    SELECT event_id, 
                           organizer_id, 
                           title, 
                           description, 
                           category, 
                           event_date, 
                           venue,
                           is_public, 
                           max_participants, 
                           is_paid, 
                           cost, 
                           status
                    FROM events
                    WHERE event_id = %s
                    """
            cursor.execute(query, (event_id,))
            result = cursor.fetchone()
            if result:
                event = cls(**result)
        except pymysql.MySQLError as e:
            print(f"Database Error in Event.find_by_id: {e}")
        finally:
            cursor.close()
            conn.close()
        return event

    def get_current_participant_count(self):
        """
        Μετρά τους ενεργούς συμμετέχοντες για αυτή την εκδήλωση.
        """
        conn = get_db_connection()
        count = None
        if not conn:
            return None

        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = """
                SELECT COUNT(*) as count FROM event_participations
                WHERE event_id = %s AND status IN ('registered', 'checkedIn')
            """
            cursor.execute(query, (self.event_id,))
            result = cursor.fetchone()
            if result:
                count = result['count']
        except pymysql.Error as e:
            print(f"Database Error in Event.get_current_participant_count: {e}")
        finally:
            cursor.close()
            conn.close()
        return count

    def check_availability(self):
        """
        Ελέγχει αν υπάρχει διαθέσιμος χώρος για νέα συμμετοχή.
        """
        if self.max_participants is None or self.max_participants <= 0:
            return True  # Δεν υπάρχει όριο, πάντα υπάρχει διαθέσιμος χώρος

        current_count = self.get_current_participant_count()

        if current_count is None:
            print("Error getting participant count. Assuming unavailable.")
            return False

        return current_count < self.max_participants

    @classmethod
    def find_all_events(cls):
        """
        Επιστρέφει όλες τις εκδηλώσεις από τη βάση.
        """
        conn = get_db_connection()
        events = []
        if not conn:
            print("No database connection")
            return events

        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT * FROM events WHERE DATE(event_date) >= CURDATE() ORDER BY event_date ASC"
            cursor.execute(query)
            results = cursor.fetchall()
            for event_data in results:
                event = cls(**event_data)
                events.append(event)
        except pymysql.Error as e:
            print(f"Database Error in Event.find_all_events: {e}")
        finally:
            cursor.close()
            conn.close()
        return events

    @classmethod
    def find_organizer_events(cls, organizer_id):
        """
        Επιστρέφει όλες τις εκδηλώσεις που δημιούργησε ο συγκεκριμένος διοργανωτής.
        """
        conn = get_db_connection()
        events = []
        if not conn:
            print("No database connection")
            return events

        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = """
                SELECT * FROM events 
                WHERE organizer_id = %s 
                AND DATE(event_date) >= CURDATE()
                ORDER BY event_date ASC
            """
            cursor.execute(query, (organizer_id,))
            results = cursor.fetchall()
            for event_data in results:
                event = cls(**event_data)
                events.append(event)
        except pymysql.Error as e:
            print(f"Database Error in Event.find_organizer_events: {e}")
        finally:
            cursor.close()
            conn.close()
        return events

    @classmethod
    def is_title_duplicate(cls, title, ignore_id=None):
        all_events = cls.find_all_events()
        for event in all_events:
            if event.title == title and event.event_id != ignore_id:
                return True
        return False

    def update_event(self):
        """
        Ενημερώνει τα στοιχεία της εκδήλωσης στη βάση.
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

    @classmethod
    def find_user_events(cls, user_id):
        """
        Επιστρέφει όλα τα events στα οποία συμμετέχει ο χρήστης.
        """
        conn = get_db_connection()
        events = []
        if not conn:
            print("No database connection")
            return events

        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = """
                SELECT e.*
                FROM events e
                JOIN event_participations ep ON e.event_id = ep.event_id
                WHERE ep.user_id = %s AND ep.status != 'withdrawn'
                AND DATE(e.event_date) >= CURDATE()
                ORDER BY e.event_date ASC
            """
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()
            for event_data in results:
                event = cls(**event_data)
                events.append(event)
        except pymysql.Error as e:
            print(f"Database Error in Event.find_user_events: {e}")
        finally:
            cursor.close()
            conn.close()
        return events
