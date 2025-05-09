import pymysql
import customtkinter as ctk
from src.auth import Auth

class MyProfilePage(ctk.CTkFrame):
    def __init__(self, master, dashboard):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard

        # Header
        self.header = ctk.CTkLabel(self, text="My Profile",
                                   font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)

        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="white")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.left_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        self.right_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.main_frame.grid_columnconfigure(0, weight=3)
        self.main_frame.grid_columnconfigure(1, weight=2)

        self.personal_frame = ctk.CTkFrame(self.left_frame, fg_color="white")
        self.personal_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Load user data
        self.user_data = self.load_user_data()

        # Create and populate fields
        self.entries = {}
        for i, (field, value) in enumerate(self.user_data.items()):
            label = ctk.CTkLabel(self.personal_frame, text=field, font=ctk.CTkFont(family="Roboto", size=16))
            label.grid(row=i, column=0, sticky="w", pady=10)

            entry = ctk.CTkEntry(self.personal_frame, width=250, font=ctk.CTkFont(family="Roboto", size=14))
            entry.insert(0, value)
            entry.configure(state="disabled")
            entry.grid(row=i, column=1, pady=10, padx=(10, 0))
            self.entries[field] = entry

        # Buttons
        self.button_container = ctk.CTkFrame(self.right_frame, fg_color="white")
        self.button_container.pack(expand=True)

        self.invites_btn = ctk.CTkButton(
            self.button_container,
            text="My Invites  →",
            fg_color="#C8A165",
            hover_color="#b38e58",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=300,
            height=40,
            corner_radius=8,
            text_color="black",
            command=self.show_my_invites
        )
        self.invites_btn.pack(pady=(0, 10))

        self.edit_btn = ctk.CTkButton(
            self.button_container,
            text="Edit Profile  →",
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

        self.view_events_btn = ctk.CTkButton(
            self.button_container,
            text="View Past Events  →",
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

        self.save_btn = ctk.CTkButton(
            self.button_container,
            text="Save Changes  →",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=300,
            height=40,
            corner_radius=8,
            text_color="black",
            command=self.save_changes
        )

        self.cancel_btn = ctk.CTkButton(
            self.button_container,
            text="Cancel  →",
            fg_color="#f44336",
            hover_color="#e53935",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=300,
            height=40,
            corner_radius=8,
            text_color="black",
            command=self.disable_editing
        )

        self.edit_mode = False

    def load_user_data(self):
        current_user = Auth.get_current_user()
        if not current_user:
            raise Exception("User not logged in.")

        user_id = current_user.user_id

        try:
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="root",
                database="τλ",
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = conn.cursor()
            query = """
                SELECT first_name, last_name, date_of_birth, phone_number,
                       address_street, address_city, address_postal_code
                FROM user_info WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            conn.close()

            if not result:
                raise Exception("User data not found.")

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
            raise Exception(f"Failed to load user data: {str(e)}")

    def update_invite_status(self, invite_id, status):
        """Ενημερώνει την κατάσταση της πρόσκλησης σε 'accepted' ή 'rejected'."""
        try:
            # Σύνδεση στη βάση δεδομένων
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="root",
                database="τλ",  # Βεβαιώσου ότι είναι το σωστό όνομα της βάσης
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = conn.cursor()

            # Ερώτημα SQL για να ενημερωθεί η κατάσταση της πρόσκλησης
            update_query = """
                UPDATE invitations
                SET status = %s
                WHERE invitation_id = %s
            """
            cursor.execute(update_query, (status, invite_id))
            conn.commit()
            conn.close()

            print(f"Η πρόσκληση {invite_id} ενημερώθηκε με κατάσταση {status}.")  # Εκτύπωση για debug

        except Exception as e:
            print(f"Σφάλμα κατά την ενημέρωση της πρόσκλησης: {str(e)}")  # Χειρισμός σφαλμάτων

    def enable_editing(self):
        for entry in self.entries.values():
            entry.configure(state="normal")

        self.edit_btn.pack_forget()
        self.view_events_btn.pack_forget()
        self.invites_btn.pack_forget()
        self.save_btn.pack(pady=(0, 10))
        self.cancel_btn.pack(pady=10)
        self.edit_mode = True

    def disable_editing(self):
        for entry in self.entries.values():
            entry.configure(state="disabled")

        self.save_btn.pack_forget()
        self.cancel_btn.pack_forget()
        self.invites_btn.pack(pady=(0, 10))
        self.edit_btn.pack(pady=(0, 10))
        self.view_events_btn.pack(pady=10)
        self.edit_mode = False

    def save_changes(self):
        for field, entry in self.entries.items():
            self.user_data[field] = entry.get()

        dialog = ctk.CTkToplevel(self)
        dialog.title("Success!")
        dialog.geometry("300x150")
        dialog.transient(self)
        dialog.grab_set()

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        message = ctk.CTkLabel(dialog, text="Your profile has been updated successfully!", font=ctk.CTkFont(size=14))
        message.pack(expand=True)

        ok_btn = ctk.CTkButton(dialog, text="OK", fg_color="#4CAF50", hover_color="#45a049",
                               font=ctk.CTkFont(size=14, weight="bold"), command=dialog.destroy)
        ok_btn.pack(pady=20)

        self.disable_editing()

    def show_my_invites(self):
        """Show user invitations dialog with Accept/Reject buttons"""
        current_user = Auth.get_current_user()
        if not current_user:
            raise Exception("User not logged in.")

        user_id = current_user.user_id

        # Create dialog window
        dialog = ctk.CTkToplevel(self)
        dialog.title("My Invitations")
        dialog.geometry("500x600")
        dialog.transient(self)
        dialog.grab_set()

        # Center dialog on screen
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        # Header
        header = ctk.CTkLabel(
            dialog,
            text="My Invitations",
            font=ctk.CTkFont(family="Roboto", size=20, weight="bold")
        )
        header.pack(pady=20, padx=20)

        # Scrollable area for invitations
        invites_frame = ctk.CTkScrollableFrame(dialog, fg_color="white")
        invites_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Load invitations from database
        try:
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="root",
                database="τλ",
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = conn.cursor()

            query = """
        SELECT i.invitation_id, e.title, e.event_date, e.venue, i.sender_message
        FROM invitations i
        JOIN events e ON i.event_id = e.event_id
        WHERE i.receipient_userid = %s
        AND i.status = 'pending'
        AND e.status = 'scheduled'
        """

            cursor.execute(query, (user_id,))
            invites = cursor.fetchall()
            conn.close()

            if not invites:
                no_invites_label = ctk.CTkLabel(
                    invites_frame,
                    text="No pending invitations.",
                    font=ctk.CTkFont(family="Roboto", size=14)
                )
                no_invites_label.pack(pady=10)
            else:
                for invite in invites:
                    invite_block = ctk.CTkFrame(invites_frame, fg_color="white")
                    invite_block.pack(pady=10, fill="x", padx=10)

                    title_label = ctk.CTkLabel(
                        invite_block,
                        text=invite["title"],
                        font=ctk.CTkFont(family="Roboto", size=16, weight="bold")
                    )
                    title_label.pack(anchor="w")

                    date_label = ctk.CTkLabel(
                        invite_block,
                        text=f"Date: {invite['event_date']}",
                        font=ctk.CTkFont(family="Roboto", size=14)
                    )
                    date_label.pack(anchor="w")

                    venue_label = ctk.CTkLabel(
                        invite_block,
                        text=f"Venue: {invite['venue']}",
                        font=ctk.CTkFont(family="Roboto", size=14)
                    )
                    venue_label.pack(anchor="w")

                    sender_msg_label = ctk.CTkLabel(
                        invite_block,
                        text=f"Message: {invite['sender_message']}",
                        font=ctk.CTkFont(family="Roboto", size=12)
                    )
                    sender_msg_label.pack(anchor="w")

                    # Accept and Reject buttons
                    accept_btn = ctk.CTkButton(
                        invite_block,
                        text="Accept",
                        fg_color="#4CAF50",
                        hover_color="#45a049",
                        font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                        command=lambda invite_id=invite["invitation_id"]: self.update_invite_status(invite_id, "accepted")
                    )
                    accept_btn.pack(side="left", padx=10)

                    reject_btn = ctk.CTkButton(
                        invite_block,
                        text="Reject",
                        fg_color="#f44336",
                        hover_color="#e53935",
                        font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                        command=lambda invite_id=invite["invitation_id"]: self.update_invite_status(invite_id, "rejected")
                    )
                    reject_btn.pack(side="left", padx=10)

        except Exception as e:
            print(f"Error loading invitations: {str(e)}")
            error_label = ctk.CTkLabel(
                invites_frame,
                text="Failed to load invitations.",
                font=ctk.CTkFont(family="Roboto", size=14)
            )
            error_label.pack(pady=10)

    def show_past_events(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Past Events")
        dialog.geometry("500x600")
        dialog.transient(self)
        dialog.grab_set()

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        header = ctk.CTkLabel(dialog, text="Past Events", font=ctk.CTkFont(family="Roboto", size=20, weight="bold"))
        header.pack(pady=20, padx=20)

        events_frame = ctk.CTkScrollableFrame(dialog, fg_color="white")
        events_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        past_events = [
            {"title": "Tech Conference 2024", "date": "March 15, 2024", "location": "Athens Convention Center"},
            {"title": "Summer Music Festival", "date": "February 20, 2024", "location": "Thessaloniki Park"},
            {"title": "Art Exhibition", "date": "January 10, 2024", "location": "National Gallery"},
            {"title": "Networking Event", "date": "December 5, 2023", "location": "Business Center"},
        ]

        for event in past_events:
            event_block = ctk.CTkFrame(events_frame, fg_color="#f5f5f5", corner_radius=10)
            event_block.pack(fill="x", pady=10, padx=10)

            title = ctk.CTkLabel(event_block, text=event["title"], font=ctk.CTkFont(size=16, weight="bold"))
            title.pack(anchor="w", padx=10, pady=(5, 0))

            date = ctk.CTkLabel(event_block, text=f"Date: {event['date']}", font=ctk.CTkFont(size=14))
            date.pack(anchor="w", padx=10)

            location = ctk.CTkLabel(event_block, text=f"Location: {event['location']}", font=ctk.CTkFont(size=14))
            location.pack(anchor="w", padx=10, pady=(0, 5))