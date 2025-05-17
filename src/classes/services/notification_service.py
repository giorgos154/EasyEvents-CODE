from datetime import datetime

class NotificationService:
    """
    NotificationService: Κλάση για την αποστολή ειδοποιήσεων.
    Οι ειδοποιήσεις προσομοιώνονται με εκτυπώσεις στο console.
    """

    @staticmethod
    def send_confirmation_email(user_email, event_title, event_date, event_venue):
        """Προσομοίωση αποστολής email επιβεβαίωσης εγγραφής σε εκδήλωση"""
        print(f"\n[EMAIL SIMULATION] Event Registration Confirmation")
        print(f"To: {user_email}")
        print(f"Subject: Successful registration for {event_title}")
        print("-" * 50)
        print(f"Thank you for registering!")
        print(f"Event: {event_title}")
        print(f"Date: {event_date}")
        print(f"Venue: {event_venue}")
        print("-" * 50)

    @staticmethod
    def notify_organizer(organizer_email, event_title, participant_username):
        """
        Προσομοίωση ειδοποίησης διοργανωτή για νέα συμμετοχή.
        """
        print("\n[EMAIL SIMULATION] Notifying Organizer")
        print("-" * 50)
        print(f"To: {organizer_email}")
        print(f"Subject: New Registration for {event_title}")
        print(f"Body:")
        print(f"Hello,")
        print(f"A new participant has registered for your event!")
        print(f"Event: {event_title}")
        print(f"Participant: {participant_username}")
        print(f"Please check your event dashboard for more details.")
        print("-" * 50)

    @staticmethod
    def notify_check_in(organizer_email, event_title, attendee_name):
        """
        Προσομοίωση ειδοποίησης διοργανωτή για check-in συμμετέχοντα.
        """
        print("\n[EMAIL SIMULATION] Check-in Notification")
        print("-" * 50)
        print(f"To: {organizer_email}")
        print(f"Subject: Check-in at {event_title}")
        print(f"Body:")
        print(f"Hello,")
        print(f"{attendee_name} has checked in to your event!")
        print(f"Event: {event_title}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)

    @staticmethod
    def notify_participants(event_title, message):
        """
        Προσομοίωση ειδοποίησης προς όλους τους συμμετέχοντες ενός event.
        """
        print("\n[NOTIFICATION SIMULATION] Notify Participants")
        print("-" * 50)
        print(f"Event: {event_title}")
        print(f"Message: {message}")
        print("All participants have been notified.")
        print("-" * 50)


    @staticmethod
    def notify_organizer_for_withdrawal(organizer_email, event_title, participant_username):
        """
        Προσομοίωση ειδοποίησης διοργανωτή για νέα συμμετοχή.
        """
        print("\n[EMAIL SIMULATION] Notifying Organizer")
        print("-" * 50)
        print(f"To: {organizer_email}")
        print(f"Subject: Withdrawal from {event_title}")
        print(f"Body:")
        print(f"Hello,")
        print(f"A participant has withdrawn from your event!")
        print(f"Event: {event_title}")
        print(f"Participant: {participant_username}")
        print(f"Please check your event dashboard for more details.")
        print("-" * 50)