# location_service.py
class LocationService:
    """
    Service for handling location-based features.
    All methods currently return simulated responses.
    """
    @staticmethod
    def request_permission():

        print("[LOCATION] Requesting permission...")
        return True  

    @staticmethod
    def get_current_location():
        
        print("[LOCATION] Getting current location...")
        return (37.9838, 23.7275)  # Example coordinates 

    @staticmethod
    def calculate_distance(point1, point2):
        
        print("[LOCATION] Calculating distance...")
        return 50.0  # ex distance

    @staticmethod
    def verify_in_radius(user_location, venue_location, radius=100):
        """
        Check if user is within venue radius
        """
        print("[LOCATION] Verifying location...")
        print(f"User location: {user_location}")
        print(f"Venue location: {venue_location}")
        print(f"Required radius: {radius}m")
        
        # Simulate successful verification
        return True, "User is within event area"

    @staticmethod
    def get_venue_coordinates(venue_name):

        print(f"[LOCATION] Getting coordinates for {venue_name}")
        return (37.9838, 23.7275)  # Example coordinates

    @staticmethod
    def format_location(lat, lng):

        return f"Lat: {lat:.4f}, Lng: {lng:.4f}"
