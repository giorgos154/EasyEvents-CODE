from src.classes.user import User
from tkinter import messagebox

class Auth:
    _current_user = None  # -- Apothikeusi tou current user -- #

    @classmethod
    def login(cls, username, password, is_organizer):
        # -- Methodos gia login -- #
        role = "organizer" if is_organizer else "attendee"
        
        # -- Elegxos an einai kena ta pedia -- #
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return False
            
        # -- Elegxos an ta stoixeia einai sosta -- #
        if User.verify_credentials(username, password, role):
            # -- An einai sosta, fortonoume ton user -- #
            user = User.load_from_db(username)
            if user:
                cls._current_user = user
                return True
                
        messagebox.showerror("Error", "Invalid credentials")
        return False

    @classmethod
    def get_current_user(cls):
        # -- Epistrofi tou current user -- #
        return cls._current_user

    @classmethod
    def logout(cls):
        # -- Logout tou user -- #
        cls._current_user = None
