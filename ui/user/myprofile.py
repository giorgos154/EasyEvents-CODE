import customtkinter as ctk
from src.auth import Auth
from datetime import datetime

class MyProfilePage(ctk.CTkFrame):
    def __init__(self, master, dashboard):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard

        self.header = ctk.CTkLabel(self, text="My Profile",
                                   font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)

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

        self.current_user = Auth.get_current_user()
        self.user_info = self.current_user.load_user_info()

        self.entries = {}
        for i, (field, value) in enumerate(self.user_info.items()):
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
            entry.insert(0, value)
            entry.configure(state="disabled")
            entry.grid(row=i, column=1, pady=10, padx=(10, 0))
            self.entries[field] = entry

        # Buttons container
        self.button_container = ctk.CTkFrame(self.right_frame, fg_color="white")
        self.button_container.pack(expand=True)

        # My Invites button
        self.invites_btn = ctk.CTkButton(
            self.button_container,
            text="My Invites→",
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

        # Save and Cancel buttons (hidden by default)
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

        self.edit_mode = False

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
        for entry in self.entries.values():
            entry.configure(state="disabled")

        self.save_btn.pack_forget()
        self.cancel_btn.pack_forget()
        self.invites_btn.pack(pady=(0, 10))
        self.edit_btn.pack(pady=(0, 10))
        self.view_events_btn.pack(pady=10)
        self.edit_mode = False

    def save_changes(self):
        """Save profile changes to the database"""
        updated_data = {
            "First Name": self.entries["First Name"].get(),
            "Last Name": self.entries["Last Name"].get(),
            "Date of Birth": self.entries["Date of Birth"].get(),
            "Phone Number": self.entries["Phone Number"].get(),
            "Street Address": self.entries["Street Address"].get(),
            "City": self.entries["City"].get(),
            "Postal Code": self.entries["Postal Code"].get()
        }

        try:
            
            # Name validation - no numbers or special characters
            if not all(c.isalpha() or c.isspace() for c in updated_data["First Name"]):
                raise ValueError("\nFirst name can only contain letters")
                
            if not all(c.isalpha() or c.isspace() for c in updated_data["Last Name"]):
                raise ValueError("\nLast name can only contain letters")

            # Date of birth validation - format YYYY-MM-DD
            try:
                datetime.strptime(updated_data["Date of Birth"], '%Y-%m-%d')
            except ValueError:
                raise ValueError("\nDate of birth must be in format YYYY-MM-DD")

            # Phone number validation - only numbers allowed
            if not updated_data["Phone Number"].replace('+', '').isdigit():
                raise ValueError("\nPhone number can only contain numbers and '+' symbol")

            # Postal code validation - only numbers allowed
            if not updated_data["Postal Code"].isdigit():
                raise ValueError("\nPostal code can only contain numbers")

            # Empty fields validation
            if any(not value for value in updated_data.values()):
                raise ValueError("All fields must be filled out")
            
            success = self.current_user.update_user_info(updated_data)
            if not success:
                raise Exception("Failed to update profile\n")

            # Show success message
            dialog = ctk.CTkToplevel(self)
            dialog.title("Success!")
            dialog.geometry("300x150")
            dialog.transient(self)
            dialog.grab_set()

            # Center dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
            y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
            dialog.geometry(f"+{x}+{y}")

            # Success message
            message = ctk.CTkLabel(
                dialog,
                text="Your profile has been updated successfully!",
                font=ctk.CTkFont(family="Roboto", size=14)
            )
            message.pack(expand=True)

            # OK button
            ok_btn = ctk.CTkButton(
                dialog,
                text="OK",
                fg_color="#4CAF50",
                hover_color="#45a049",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                command=dialog.destroy
            )
            ok_btn.pack(pady=20)

            self.disable_editing()

        except Exception as e:
            # Show error message
            error_dialog = ctk.CTkToplevel(self)
            error_dialog.title("Error")
            error_dialog.geometry("300x150")
            error_dialog.transient(self)
            error_dialog.grab_set()

            message = ctk.CTkLabel(
                error_dialog,
                text=f"Failed to update profile: {str(e)}",
                font=ctk.CTkFont(family="Roboto", size=14)
            )
            message.pack(expand=True)

            ok_btn = ctk.CTkButton(
                error_dialog,
                text="OK",
                command=error_dialog.destroy
            )
            ok_btn.pack(pady=20)

    def center_window(self, window):
        """Center a window on screen"""
        window.update_idletasks()
        x = (window.winfo_screenwidth() - window.winfo_width()) // 2
        y = (window.winfo_screenheight() - window.winfo_height()) // 2
        window.geometry(f"+{x}+{y}")

    def create_event_card(self, parent, event):
        """Create a card for an event"""
        event_frame = ctk.CTkFrame(parent, fg_color="#f5f5f5", corner_radius=8)
        event_frame.pack(fill="x", pady=5, padx=5)

        event_date = event["event_date"].strftime("%B %d, %Y") if event["event_date"] else "Date not specified"

        title = ctk.CTkLabel(
            event_frame,
            text=event["title"],
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold")
        )
        title.pack(anchor="w", padx=10, pady=(10, 0))

        date = ctk.CTkLabel(
            event_frame,
            text=f"Date: {event_date}",
            font=ctk.CTkFont(family="Roboto", size=12)
        )
        date.pack(anchor="w", padx=10)

        venue = ctk.CTkLabel(
            event_frame,
            text=f"Venue: {event['venue']}",
            font=ctk.CTkFont(family="Roboto", size=12)
        )
        venue.pack(anchor="w", padx=10)

        if event.get("category"):
            category = ctk.CTkLabel(
                event_frame,
                text=f"Category: {event['category']}",
                font=ctk.CTkFont(family="Roboto", size=12)
            )
            category.pack(anchor="w", padx=10)

        status = ctk.CTkLabel(
            event_frame,
            text=f"Status: {event['status'].capitalize()}",
            font=ctk.CTkFont(family="Roboto", size=12)
        )
        status.pack(anchor="w", padx=10)

        if event.get("description"):
            description = ctk.CTkLabel(
                event_frame,
                text=f"Description: {event['description']}",
                font=ctk.CTkFont(family="Roboto", size=12),
                wraplength=400
            )
            description.pack(anchor="w", padx=10, pady=(0, 10))

    def show_error_message(self, message, parent=None):
        """Show an error message dialog"""
        parent = parent or self
        dialog = ctk.CTkToplevel(parent)
        dialog.title("Error")
        dialog.geometry("300x150")
        dialog.transient(parent)
        dialog.grab_set()
        self.center_window(dialog)

        ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(family="Roboto", size=14)
        ).pack(expand=True)

        ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy
        ).pack(pady=20)

    def show_past_events(self):
        """Show past events in a dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Past Events")
        dialog.geometry("500x600")
        dialog.transient(self)
        dialog.grab_set()
        self.center_window(dialog)

        header = ctk.CTkLabel(
            dialog,
            text="Past Events",
            font=ctk.CTkFont(family="Roboto", size=20, weight="bold")
        )
        header.pack(pady=20, padx=20)

        events_frame = ctk.CTkScrollableFrame(dialog, fg_color="white")
        events_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        try:
            past_events = self.current_user.get_past_events()
            
            if not past_events:
                no_events_label = ctk.CTkLabel(
                    events_frame,
                    text="No past events found.",
                    font=ctk.CTkFont(family="Roboto", size=14)
                )
                no_events_label.pack(pady=20)
            else:
                for event in past_events:
                    self.create_event_card(events_frame, event)

        except Exception as e:
            self.show_error_message(f"Error loading past events: {e}", parent=dialog)
