import pymysql
import customtkinter as ctk
from src.auth import Auth


class MyProfilePage(ctk.CTkFrame):
    def __init__(self, master, dashboard):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard
        self.current_user = Auth.get_current_user()

        if not self.current_user:
            raise Exception("User not logged in.")

        self.user_id = self.current_user.user_id
        self.initialize_ui()

    def initialize_ui(self):
        """Initialize all UI components"""
        # Header
        self.header = ctk.CTkLabel(self, text="My Profile",
                                   font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)

        # Main container with two columns
        self.main_frame = ctk.CTkFrame(self, fg_color="white")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Left column: profile info
        self.left_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        # Right column: action buttons
        self.right_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Column weights (60% - 40%)
        self.main_frame.grid_columnconfigure(0, weight=3)
        self.main_frame.grid_columnconfigure(1, weight=2)

        # Profile fields
        self.personal_frame = ctk.CTkFrame(self.left_frame, fg_color="white")
        self.personal_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Get current user's data from the database
        self.user_data = self.load_user_data()
        self.create_profile_fields()
        self.create_action_buttons()

        self.edit_mode = False

    def create_profile_fields(self):
        """Create and populate profile fields"""
        self.entries = {}
        fields_order = [
            "First Name", "Last Name", "Date of Birth",
            "Phone Number", "Street Address", "City", "Postal Code"
        ]

        for i, field in enumerate(fields_order):
            label = ctk.CTkLabel(
                self.personal_frame,
                text=field,
                font=ctk.CTkFont(family="Roboto", size=16)
            )
            label.grid(row=i, column=0, sticky="w", pady=10)

            entry = ctk.CTkEntry(
                self.personal_frame,
                width=250,
                font=ctk.CTkFont(family="Roboto", size=14)
            )
            entry.insert(0, self.user_data.get(field, ""))
            entry.configure(state="disabled")
            entry.grid(row=i, column=1, pady=10, padx=(10, 0))
            self.entries[field] = entry

    def create_action_buttons(self):
        """Create all action buttons"""
        # Buttons container
        self.button_container = ctk.CTkFrame(self.right_frame, fg_color="white")
        self.button_container.pack(expand=True)

        # My Invites button
        self.invites_btn = ctk.CTkButton(
            self.button_container,
            text="My Invites →",
            fg_color="#C8A165",
            hover_color="#b38e58",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=300,
            height=40,
            corner_radius=8,
            text_color="black",
            command=lambda: self.dashboard.show_my_invites()
        )
        self.invites_btn.pack(pady=(0, 10))

        # Edit button
        self.edit_btn = ctk.CTkButton(
            self.button_container,
            text="Edit Profile →",
            fg_color="#C8A165",
            hover_color="#b38e58",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=300,
            height=40,
            corner_radius=8,
            text_color="black",
            command=self.enable_editing
        )
        self.edit_btn.pack(pady=(0, 10))

        # View Past Events button
        self.view_events_btn = ctk.CTkButton(
            self.button_container,
            text="View Past Events →",
            fg_color="#C8A165",
            hover_color="#b38e58",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=300,
            height=40,
            corner_radius=8,
            text_color="black",
            command=self.show_past_events
        )
        self.view_events_btn.pack(pady=10)

        # Save button
        self.save_btn = ctk.CTkButton(
            self.button_container,
            text="Save Changes →",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=300,
            height=40,
            corner_radius=8,
            text_color="black",
            command=self.save_changes
        )

        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            self.button_container,
            text="Cancel →",
            fg_color="#f44336",
            hover_color="#e53935",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=300,
            height=40,
            corner_radius=8,
            text_color="black",
            command=self.disable_editing
        )

    def load_user_data(self):
        """Load user data from the database"""
        try:
            with pymysql.connect(
                    host="localhost",
                    user="root",
                    password="Denistheking123!",
                    database="easyeventsdatabase",
                    charset="utf8mb4",
                    cursorclass=pymysql.cursors.DictCursor
            ) as conn:
                with conn.cursor() as cursor:
                    query = """
                            SELECT first_name, \
                                   last_name, \
                                   date_of_birth, \
                                   phone_number, \
                                   address_street, \
                                   address_city, \
                                   address_postal_code
                            FROM user_info
                            WHERE user_id = %s \
                            """
                    cursor.execute(query, (self.user_id,))
                    result = cursor.fetchone()

                    if not result:
                        raise Exception("User data not found.")

                    # Format date if it exists
                    if result["date_of_birth"]:
                        result["date_of_birth"] = result["date_of_birth"].strftime("%Y-%m-%d")

                    return {
                        "First Name": result["first_name"],
                        "Last Name": result["last_name"],
                        "Date of Birth": result["date_of_birth"],
                        "Phone Number": result["phone_number"],
                        "Street Address": result["address_street"],
                        "City": result["address_city"],
                        "Postal Code": result["address_postal_code"]
                    }

        except Exception as e:
            self.show_error_message(f"Failed to load user data: {str(e)}")
            return {
                "First Name": "",
                "Last Name": "",
                "Date of Birth": "",
                "Phone Number": "",
                "Street Address": "",
                "City": "",
                "Postal Code": ""
            }

    def enable_editing(self):
        """Enable editing of profile fields"""
        for entry in self.entries.values():
            entry.configure(state="normal")

        self.edit_btn.pack_forget()
        self.view_events_btn.pack_forget()
        self.invites_btn.pack_forget()
        self.save_btn.pack(pady=(0, 10))
        self.cancel_btn.pack(pady=10)
        self.edit_mode = True

    def disable_editing(self):
        """Disable editing of profile fields"""
        # Reload original data
        self.user_data = self.load_user_data()
        for field, entry in self.entries.items():
            entry.configure(state="disabled")
            entry.delete(0, "end")
            entry.insert(0, self.user_data.get(field, ""))

        self.save_btn.pack_forget()
        self.cancel_btn.pack_forget()
        self.invites_btn.pack(pady=(0, 10))
        self.edit_btn.pack(pady=(0, 10))
        self.view_events_btn.pack(pady=10)
        self.edit_mode = False

    def save_changes(self):
        """Save profile changes to the database"""
        try:
            with pymysql.connect(
                    host="localhost",
                    user="root",
                    password="Denistheking123!",
                    database="easyeventsdatabase",
                    charset="utf8mb4",
                    cursorclass=pymysql.cursors.DictCursor
            ) as conn:
                with conn.cursor() as cursor:
                    update_query = """
                                   UPDATE user_info
                                   SET first_name          = %s,
                                       last_name           = %s,
                                       date_of_birth       = %s,
                                       phone_number        = %s,
                                       address_street      = %s,
                                       address_city        = %s,
                                       address_postal_code = %s
                                   WHERE user_id = %s \
                                   """

                    updated_data = (
                        self.entries["First Name"].get(),
                        self.entries["Last Name"].get(),
                        self.entries["Date of Birth"].get(),
                        self.entries["Phone Number"].get(),
                        self.entries["Street Address"].get(),
                        self.entries["City"].get(),
                        self.entries["Postal Code"].get(),
                        self.user_id
                    )

                    cursor.execute(update_query, updated_data)
                    conn.commit()

                    self.show_success_message("Your profile has been updated successfully!")
                    self.disable_editing()

        except Exception as e:
            self.show_error_message(f"Failed to update profile: {str(e)}")

    def show_past_events(self):
        """Show past events dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Past Events")
        dialog.geometry("500x600")
        dialog.transient(self)
        dialog.grab_set()

        # Center dialog
        self.center_window(dialog)

        # Dialog header
        header = ctk.CTkLabel(
            dialog,
            text="Past Events",
            font=ctk.CTkFont(family="Roboto", size=20, weight="bold")
        )
        header.pack(pady=20, padx=20)

        # Scrollable frame for events
        events_frame = ctk.CTkScrollableFrame(dialog, fg_color="white")
        events_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        try:
            with pymysql.connect(
                    host="localhost",
                    user="root",
                    password="Denistheking123!",
                    database="easyeventsdatabase",
                    charset="utf8mb4",
                    cursorclass=pymysql.cursors.DictCursor
            ) as conn:
                with conn.cursor() as cursor:
                    query = """
                            SELECT e.title,
                                   e.event_date,
                                   e.venue,
                                   e.description,
                                   e.category,
                                   e.status
                            FROM events e
                                     JOIN event_participations ep ON e.event_id = ep.event_id
                            WHERE ep.user_id = %s
                              AND e.event_date < CURDATE()
                              AND e.status = 'completed'
                            ORDER BY e.event_date DESC
                            """

                    cursor.execute(query, (self.user_id,))
                    past_events = cursor.fetchall()

                    if not past_events:
                        no_events_label = ctk.CTkLabel(
                            events_frame,
                            text="No past events found.",
                            font=ctk.CTkFont(family="Roboto", size=14)
                        )
                        no_events_label.pack(pady=20)
                        return

                    # Display events
                    for event in past_events:
                        self.create_event_card(events_frame, event)

        except Exception as e:
            self.show_error_message(f"Error loading past events: {e}", parent=dialog)

    def create_event_card(self, parent, event):
        """Create a card for an event"""
        event_frame = ctk.CTkFrame(parent, fg_color="#f5f5f5", corner_radius=8)
        event_frame.pack(fill="x", pady=5, padx=5)

        # Format date
        event_date = event["event_date"].strftime("%B %d, %Y") if event["event_date"] else "Date not specified"

        # Title
        title = ctk.CTkLabel(
            event_frame,
            text=event["title"],
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold")
        )
        title.pack(anchor="w", padx=10, pady=(10, 0))

        # Date
        date = ctk.CTkLabel(
            event_frame,
            text=f"Date: {event_date}",
            font=ctk.CTkFont(family="Roboto", size=12)
        )
        date.pack(anchor="w", padx=10)

        # Venue
        venue = ctk.CTkLabel(
            event_frame,
            text=f"Venue: {event['venue']}",
            font=ctk.CTkFont(family="Roboto", size=12)
        )
        venue.pack(anchor="w", padx=10)

        # Category
        if event.get("category"):
            category = ctk.CTkLabel(
                event_frame,
                text=f"Category: {event['category']}",
                font=ctk.CTkFont(family="Roboto", size=12)
            )
            category.pack(anchor="w", padx=10)

        # Status
        status = ctk.CTkLabel(
            event_frame,
            text=f"Status: {event['status'].capitalize()}",
            font=ctk.CTkFont(family="Roboto", size=12)
        )
        status.pack(anchor="w", padx=10)

        # Description (if available)
        if event.get("description"):
            description = ctk.CTkLabel(
                event_frame,
                text=f"Description: {event['description']}",
                font=ctk.CTkFont(family="Roboto", size=12),
                wraplength=400
            )
            description.pack(anchor="w", padx=10, pady=(0, 10))

    def show_success_message(self, message):
        """Show a success message dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Success!")
        dialog.geometry("300x150")
        dialog.transient(self)
        dialog.grab_set()
        self.center_window(dialog)

        # Success message
        ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(family="Roboto", size=14)
        ).pack(expand=True)

        # OK button
        ctk.CTkButton(
            dialog,
            text="OK",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            command=dialog.destroy
        ).pack(pady=20)

    def show_error_message(self, message, parent=None):
        """Show an error message dialog"""
        parent = parent or self
        dialog = ctk.CTkToplevel(parent)
        dialog.title("Error")
        dialog.geometry("300x150")
        dialog.transient(parent)
        dialog.grab_set()
        self.center_window(dialog)

        # Error message
        ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(family="Roboto", size=14)
        ).pack(expand=True)

        # OK button
        ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy
        ).pack(pady=20)
###
    def center_window(self, window):
        """Center a window on screen"""
        window.update_idletasks()
        x = (window.winfo_screenwidth() - window.winfo_width()) // 2
        y = (window.winfo_screenheight() - window.winfo_height()) // 2
        window.geometry(f"+{x}+{y}")