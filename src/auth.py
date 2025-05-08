from classes.member.member import Member
from tkinter import messagebox

class Auth:
    _current_user = None  # -- Αποθήκευση του τρέχοντος χρήστη -- #

    @classmethod
    def login(cls, username, password, is_organizer):
        # -- Μέθοδος για σύνδεση -- #
        role = "organizer" if is_organizer else "attendee"

        # -- Έλεγχος αν είναι κενά τα πεδία -- #
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return False

        # -- Έλεγχος αν τα στοιχεία είναι σωστά -- #
        if Member.verify_credentials(username, password, role):
            # -- Αν τα στοιχεία είναι σωστά, φορτώνουμε τον χρήστη -- #
            user = Member.load_from_db(username)
            if user:
                cls._current_user = user  # Αποθηκεύουμε τον χρήστη
                return True

        messagebox.showerror("Error", "Invalid credentials")
        return False

    @classmethod
    def get_current_user(cls):
        # -- Επιστροφή του τρέχοντος χρήστη -- #
        if cls._current_user is None:
            messagebox.showerror("Error", "No user is logged in")
        return cls._current_user

    @classmethod
    def logout(cls):
        # -- Αποσύνδεση του χρήστη -- #
        cls._current_user = None
        messagebox.showinfo("Logged out", "You have been logged out successfully.")
