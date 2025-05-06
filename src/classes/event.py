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
        find_by_id (Class Method): Vriskei mia ekdilwsi sti vasi dedomenwn me vasi to ID tis.
       
        """
        conn = get_db_connection()
        event = None
        if not conn:
            return None # Den egine syndesi me ti vasi

        try:
            cursor = conn.cursor()
            query = "SELECT * FROM events WHERE event_id = %s"
            cursor.execute(query, (event_id,))
            result = cursor.fetchone()
            if result:
                # Dimiourgia Event object apo ta data tis vasis
                event = cls(**result) # Xrisimopoioume **result gia na perasoume ta key-values ws arguments
        except pymysql.Error as e:
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

    def register_participant(self, user_id):
        """
        register_participant: Kataxwrei enan neo symmetexonta gia auti tin ekdilwsi.
        Prosthetai mia eggrafi ston pinaka event_participations.
        Epistrefei True an i eggrafi egine epitixws, False an oxi (px, sfalma vasis).
        """
        conn = get_db_connection()
        success = False
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO event_participations (user_id, event_id, registration_date, status)
                VALUES (%s, %s, %s, %s)
            """
            
            status = 'registered' 
            cursor.execute(query, (user_id, self.event_id, datetime.now(), status)) 
            conn.commit() # Kanoume commit tis allages sti vasi
            success = cursor.rowcount > 0 # Elegxoume an egine i eisagwgi (rowcount > 0)
            if success:
                print(f"User {user_id} registered successfully for event {self.event_id}")
            else:
                 print(f"Failed to register user {user_id} for event {self.event_id}. Rowcount: {cursor.rowcount}")

        except pymysql.Error as e:
            print(f"Database Error in Event.register_participant: {e}")
            conn.rollback() # An ginei sfalma, kanoume rollback
            success = False
        finally:
            cursor.close()
            conn.close()
        return success

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


