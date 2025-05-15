from datetime import datetime
import customtkinter as ctk
from src.classes.event.event import Event  
from CTkMessagebox import CTkMessagebox


class EditEventPage(ctk.CTkFrame):
    def __init__(self, master, dashboard, event_id):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard

        self.event = Event.find_by_id(event_id)  

        if not self.event:
            self.show_error("Event not found!")
            return

        self.original_values = {
            "title": self.event.title,
            "event_date": self.event.event_date.strftime('%Y-%m-%d %H:%M'),
            "venue": self.event.venue,
            "description": self.event.description,
            "visibility": "public" if self.event.is_public else "private",
            "category": self.event.category,
            "max_participants": str(self.event.max_participants),
            "cost": str(self.event.cost)
        }

        self.default_font = ctk.CTkFont(family="Roboto", size=14)

        # Header
        self.header = ctk.CTkLabel(self, text="Edit Event", 
                                   font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)

        # Scrollable frame for the form
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=600, height=500)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.form_frame = self.scrollable_frame

        # Event Title
        self.title_label = ctk.CTkLabel(self.form_frame, text="Event Title", font=self.default_font)
        self.title_label.pack(anchor="w", pady=(5, 0))

        self.title_entry = ctk.CTkEntry(self.form_frame, font=self.default_font, placeholder_text="Enter event title")
        self.title_entry.insert(0, self.event.title)  
        self.title_entry.pack(fill="x", pady=(5, 15))

        # Date & Time
        self.dt_label = ctk.CTkLabel(self.form_frame, text="Date & Time", font=self.default_font)
        self.dt_label.pack(anchor="w", pady=(5, 0))

        self.dt_entry = ctk.CTkEntry(self.form_frame, font=self.default_font, placeholder_text="Enter event date and time (YYYY-MM-DD HH:MM)")
        self.dt_entry.insert(0, self.event.event_date.strftime('%Y-%m-%d %H:%M'))  
        self.dt_entry.pack(fill="x", pady=(5, 15))

        # Location
        self.loc_label = ctk.CTkLabel(self.form_frame, text="Location", font=self.default_font)
        self.loc_label.pack(anchor="w", pady=(5, 0))

        self.loc_entry = ctk.CTkEntry(self.form_frame, font=self.default_font, placeholder_text="Enter event location")
        self.loc_entry.insert(0, self.event.venue)  
        self.loc_entry.pack(fill="x", pady=(5, 15))

        # Description
        self.desc_label = ctk.CTkLabel(self.form_frame, text="Description", font=self.default_font)
        self.desc_label.pack(anchor="w", pady=(5, 0))

        self.desc_textbox = ctk.CTkTextbox(self.form_frame, height=100, font=self.default_font)
        self.desc_textbox.insert("0.0", self.event.description)
        self.desc_textbox.pack(fill="x", pady=(5, 15))

        # Visibility
        self.visibility_label = ctk.CTkLabel(self.form_frame, text="Visibility:", font=self.default_font)
        self.visibility_label.pack(anchor="w", pady=(5, 0))

        self.visibility_var = ctk.StringVar(value=self.original_values["visibility"])
        self.visibility_optionmenu = ctk.CTkOptionMenu(self.form_frame, variable=self.visibility_var, values=["public", "private"])
        self.visibility_optionmenu.pack(fill="x", pady=(5, 15))

        # Category
        self.category_label = ctk.CTkLabel(self.form_frame, text="Category:", font=self.default_font)
        self.category_label.pack(anchor="w", pady=(5, 0))

        self.category_entry = ctk.CTkEntry(self.form_frame, font=self.default_font, placeholder_text="Enter event category")
        self.category_entry.insert(0, self.event.category)
        self.category_entry.pack(fill="x", pady=(5, 15))

        # Max Participants
        self.max_participants_label = ctk.CTkLabel(self.form_frame, text="Max Participants:", font=self.default_font)
        self.max_participants_label.pack(anchor="w", pady=(5, 0))

        self.max_participants_entry = ctk.CTkEntry(self.form_frame, font=self.default_font, placeholder_text="Enter max participants")
        self.max_participants_entry.insert(0, str(self.event.max_participants))
        self.max_participants_entry.pack(fill="x", pady=(5, 15))

        # Cost
        self.cost_label = ctk.CTkLabel(self.form_frame, text="Cost:", font=self.default_font)
        self.cost_label.pack(anchor="w", pady=(5, 0))

        self.cost_entry = ctk.CTkEntry(self.form_frame, font=self.default_font, placeholder_text="Enter event cost")
        self.cost_entry.insert(0, str(self.event.cost))
        self.cost_entry.pack(fill="x", pady=(5, 15))

        # Buttons
        self.buttons_frame = ctk.CTkFrame(self.form_frame, fg_color="white")
        self.buttons_frame.pack(pady=10)

        self.save_btn = ctk.CTkButton(self.buttons_frame, text="Save Changes", fg_color="#4CAF50",
                                      hover_color="#45a049", font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                                      width=150, command=self.save_event)
        self.save_btn.grid(row=0, column=0, padx=10)

        self.cancel_btn = ctk.CTkButton(self.buttons_frame, text="Cancel", fg_color="gray",
                                        hover_color="#666666", font=ctk.CTkFont(family="Roboto", size=14),
                                        width=150, command=self.cancel_edit)
        self.cancel_btn.grid(row=0, column=1, padx=10)

    def save_event(self):
        updated_title = self.title_entry.get().strip()
        updated_dt = self.dt_entry.get().strip()
        updated_location = self.loc_entry.get().strip()
        updated_desc = self.desc_textbox.get("0.0", "end").strip()
        updated_visibility = self.visibility_var.get()
        updated_category = self.category_entry.get().strip()

        try:
            updated_max_participants = int(self.max_participants_entry.get().strip())
        except ValueError:
            self.show_error("Max Participants must be an integer.")
            return

        try:
            updated_cost = float(self.cost_entry.get().strip())
        except ValueError:
            self.show_error("Cost must be a number.")
            return

        if not updated_title:
            self.show_error("Event title cannot be empty.")
            return
        if not updated_dt:
            self.show_error("Event date and time cannot be empty.")
            return
        if not updated_location:
            self.show_error("Event location cannot be empty.")
            return
        if len(updated_title) > 100:
            self.show_error("Event title cannot exceed 100 characters.")
            return
        if len(updated_desc) > 500:
            self.show_error("Description cannot exceed 500 characters.")
            return
        if updated_visibility not in ["public", "private"]:
            self.show_error("Visibility must be either 'public' or 'private'.")
            return

        try:
            updated_date = datetime.strptime(updated_dt, '%Y-%m-%d %H:%M')
        except ValueError:
            self.show_error("Invalid date format. Please use 'YYYY-MM-DD HH:MM'.")
            return

        if updated_date < datetime.now():
            self.show_error("Event date and time must be in the future.")
            return

        current_participants = self.event.get_current_participant_count()
        if current_participants is None:
            self.show_error("Error retrieving current participants count.")
            return

        if updated_max_participants < current_participants:
            self.show_error(f"The number of participants ({current_participants}) exceeds the new max participants.")
            return

        if updated_cost < 0:
            self.show_error("Cost cannot be negative.")
            return

        if Event.is_title_duplicate(updated_title, ignore_id=self.event.event_id):
            self.show_error("An event with this title already exists. Please choose a different title.")
            return

        # Update event properties
        self.event.title = updated_title
        self.event.event_date = updated_date
        self.event.venue = updated_location
        self.event.description = updated_desc
        self.event.is_public = (updated_visibility == "public")
        self.event.category = updated_category
        self.event.max_participants = updated_max_participants
        self.event.cost = updated_cost
        self.event.is_paid = updated_cost > 0

        # Save event to database
        success, msg = self.event.update_event()
        if success:
            self.show_success("Event updated successfully!")
            self.dashboard.show_page("Manage Events")
        else:
            self.show_error(msg)

    def cancel_edit(self):
        if self.has_unsaved_changes():
            answer = self.confirmation_dialog("There are unsaved changes. Are you sure you want to cancel?")
            if not answer:
                return
        self.dashboard.show_page("Manage Events")

    def has_unsaved_changes(self):
        return (
            self.title_entry.get().strip() != self.original_values["title"] or
            self.dt_entry.get().strip() != self.original_values["event_date"] or
            self.loc_entry.get().strip() != self.original_values["venue"] or
            self.desc_textbox.get("0.0", "end").strip() != self.original_values["description"] or
            self.visibility_var.get() != self.original_values["visibility"] or
            self.category_entry.get().strip() != self.original_values["category"] or
            self.max_participants_entry.get().strip() != self.original_values["max_participants"] or
            self.cost_entry.get().strip() != self.original_values["cost"]
        )

    def confirmation_dialog(self, message):
        result = CTkMessagebox(title="Confirm", message=message, option_1="Yes", option_2="No")
        return result.get() == "Yes"

    def show_error(self, message):
        CTkMessagebox(title="Error", message=message, icon="cancel")

    def show_success(self, message):
        CTkMessagebox(title="Success", message=message, icon="check")
