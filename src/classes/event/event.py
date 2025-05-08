# src/classes/event.py
from src.db_connection import get_db_connection
import pymysql
from datetime import datetime

class Event:
    """
    Event Class: Antiproswpevei mia ekdilwsi sto systima.
    Perilamvanei methodous gia diaxeirisi dedomenwn ekdilwsis sti vasi
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
        find_by_id (Class Method): Βρίσκει μια εκδήλωση στη βάση δεδομένων με βάση το ID της.
        """
        conn = get_db_connection()
        event = None
        if not conn:
            return None  # Δεν έγινε σύνδεση με τη βάση

        try:
            cursor = conn.cursor()
            query = """
                    SELECT event_id, \
                           organizer_id, \
                           title, \
                           description, \
                           category, \
                           event_date, \
                           venue,
                           is_public, \
                           max_participants, \
                           is_paid, \
                           cost, \
                           status
                    FROM events
                    WHERE event_id = %s \
                    """

            cursor.execute(query, (event_id,))
            result = cursor.fetchone()
            if result:
                # Δημιουργία Event αντικειμένου από τα δεδομένα της βάσης
                event = cls(**result)  # Χρησιμοποιούμε **result για να περάσουμε τα key-values ως arguments
        except pymysql.MySQLError as e:  # Χρησιμοποιούμε MySQLError για καλύτερη εξαίρεση
            print(f"Database Error in Event.find_by_id: {e}")
        finally:
            cursor.close()
            conn.close()
        return event

    def get_current_participant_count(self):
        """
        get_current_participant_count: Metraei tous energous symmetexontes gia auti tin ekdilwsi.
        Energos symmetexontas = status 'registered' i 'checkedIn'.
        Epistrefei ton arithmo twn symmetexontwn i None an ginei sfalma.
        """
        conn = get_db_connection()
        count = None
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            # Metrame mono tous registered kai checkedIn, oxi tous withdrawn
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
        check_availability: Elegxei an yparxei diathesimotita gia nea symmetoxi.
        Sygrinei ton trexon arithmo symmetexontwn me to max_participants (an yparxei).
        Epistrefei True an yparxei xwros, False an einai gemato i an den oristike max_participants.
        """
        if self.max_participants is None or self.max_participants <= 0:
            return True # Den yparxei orio, panta yparxei diathesimotita

        current_count = self.get_current_participant_count()

        if current_count is None:
            print("Error getting participant count. Assuming unavailable.")
            return False # An den mporesoume na vroume ton arithmo, thewroume oti den yparxei xwros

        return current_count < self.max_participants


    @classmethod
    def find_all_events(cls):
        """
        find_all_events (Class Method): Epistrefei ola ta events apo ti vasi.
        """
        conn = get_db_connection()
        events = []
        if not conn:
            print("No database connection")
            return events # Return empty list if no connection

        try:
            cursor = conn.cursor()
            query = "SELECT * FROM events ORDER BY event_date ASC"
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
        find_organizer_events (Class Method): Returns all events created by an organizer
        """
        conn = get_db_connection()
        events = []
        if not conn:
            print("No database connection")
            return events

        try:
            cursor = conn.cursor()
            query = """
                SELECT * FROM events 
                WHERE organizer_id = %s 
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
    def find_user_events(cls, user_id):
        """
        find_user_events (Class Method): Epistrefei ola ta events pou symmetexei o xristis
        """
        conn = get_db_connection()
        events = []
        if not conn:
            print("No database connection")
            return events

        try:
            cursor = conn.cursor()
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
