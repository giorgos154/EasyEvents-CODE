# notification_service.py
class NotificationService:
    """
    NotificationService: Klasi gia tin apostoli eidopoiisewn. ta kanoume sto console
    """
    @staticmethod
    def send_confirmation_email(user_email, event_title, event_date, event_venue):
        """Prosomiwsi apostolis email epivevaiwsis egrafis se ekdilwsi"""
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
        Prosomiwsi eidopoiisis diorganwti gia nea symmetoxi.
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

