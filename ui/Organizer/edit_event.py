from datetime import datetime
import customtkinter as ctk
from src.classes.event.ManageEvent import ManageEvent  
from src.classes.event.event import Event
from CTkMessagebox import CTkMessagebox

class EditEventPage(ctk.CTkFrame):
    def __init__(self, master, dashboard, event_id):
        super().__init__(master, fg_color="transparent")
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

        # Header with gold accent
        header_frame = ctk.CTkFrame(self, fg_color="#C8A165", height=60)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)

        self.header = ctk.CTkLabel(
            header_frame, 
            text="Edit Event",
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold"),
            text_color="black"
        )
        self.header.pack(expand=True)

        # Main content in white frame
        main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Scrollable frame for the form
        self.scrollable_frame = ctk.CTkScrollableFrame(
            main_frame, 
            fg_color="transparent",
            width=600,
            height=500
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.form_frame = self.scrollable_frame

        # Event Title Section
        title_section = self.create_section("Basic Information")
        
        self.title_label = ctk.CTkLabel(
            title_section,
            text="Event Title",
            font=self.default_font,
            text_color="black"
        )
        self.title_label.pack(anchor="w", pady=(5, 0))

        self.title_entry = ctk.CTkEntry(
            title_section,
            font=self.default_font,
            placeholder_text="Enter event title",
            height=35,
            border_width=2,
            border_color="#C8A165",
            fg_color="white",
            corner_radius=8
        )
        self.title_entry.insert(0, self.event.title)
        self.title_entry.pack(fill="x", pady=(5, 15))

        # Date & Time Section
        self.dt_label = ctk.CTkLabel(
            title_section,
            text="Date & Time",
            font=self.default_font,
            text_color="black"
        )
        self.dt_label.pack(anchor="w", pady=(5, 0))

        self.dt_entry = ctk.CTkEntry(
            title_section,
            font=self.default_font,
            placeholder_text="YYYY-MM-DD HH:MM",
            height=35,
            border_width=2,
            border_color="#C8A165",
            fg_color="white",
            corner_radius=8
        )
        self.dt_entry.insert(0, self.event.event_date.strftime('%Y-%m-%d %H:%M'))
        self.dt_entry.pack(fill="x", pady=(5, 15))

        # Location Section
        self.loc_label = ctk.CTkLabel(
            title_section,
            text="Location",
            font=self.default_font,
            text_color="black"
        )
        self.loc_label.pack(anchor="w", pady=(5, 0))

        self.loc_entry = ctk.CTkEntry(
            title_section,
            font=self.default_font,
            placeholder_text="Enter event location",
            height=35,
            border_width=2,
            border_color="#C8A165",
            fg_color="white",
            corner_radius=8
        )
        self.loc_entry.insert(0, self.event.venue)
        self.loc_entry.pack(fill="x", pady=(5, 15))

        # Description Section
        description_section = self.create_section("Description")
        
        self.desc_label = ctk.CTkLabel(
            description_section,
            text="Event Description",
            font=self.default_font,
            text_color="black"
        )
        self.desc_label.pack(anchor="w", pady=(5, 0))

        self.desc_textbox = ctk.CTkTextbox(
            description_section,
            height=100,
            font=self.default_font,
            border_width=2,
            border_color="#C8A165",
            fg_color="white",
            corner_radius=8
        )
        self.desc_textbox.insert("0.0", self.event.description)
        self.desc_textbox.pack(fill="x", pady=(5, 15))

        # Event Settings Section
        settings_section = self.create_section("Event Settings")

        # Visibility
        self.visibility_label = ctk.CTkLabel(
            settings_section,
            text="Visibility",
            font=self.default_font,
            text_color="black"
        )
        self.visibility_label.pack(anchor="w", pady=(5, 0))

        self.visibility_var = ctk.StringVar(value=self.original_values["visibility"])
        self.visibility_optionmenu = ctk.CTkOptionMenu(
            settings_section,
            variable=self.visibility_var,
            values=["public", "private"],
            fg_color="#C8A165",
            button_color="#C8A165",
            button_hover_color="#b38e58",
            dropdown_hover_color="#b38e58",
            text_color="black"
        )
        self.visibility_optionmenu.pack(fill="x", pady=(5, 15))

        # Category
        self.category_label = ctk.CTkLabel(
            settings_section,
            text="Category",
            font=self.default_font,
            text_color="black"
        )
        self.category_label.pack(anchor="w", pady=(5, 0))

        self.category_entry = ctk.CTkEntry(
            settings_section,
            font=self.default_font,
            placeholder_text="Enter event category",
            height=35,
            border_width=2,
            border_color="#C8A165",
            fg_color="white",
            corner_radius=8
        )
        self.category_entry.insert(0, self.event.category)
        self.category_entry.pack(fill="x", pady=(5, 15))

        # Capacity Section
        capacity_section = self.create_section("Capacity & Cost")

        # Max Participants
        self.max_participants_label = ctk.CTkLabel(
            capacity_section,
            text="Maximum Participants",
            font=self.default_font,
            text_color="black"
        )
        self.max_participants_label.pack(anchor="w", pady=(5, 0))

        self.max_participants_entry = ctk.CTkEntry(
            capacity_section,
            font=self.default_font,
            placeholder_text="Enter max participants",
            height=35,
            border_width=2,
            border_color="#C8A165",
            fg_color="white",
            corner_radius=8
        )
        self.max_participants_entry.insert(0, str(self.event.max_participants))
        self.max_participants_entry.pack(fill="x", pady=(5, 15))

        # Cost
        self.cost_label = ctk.CTkLabel(
            capacity_section,
            text="Event Cost",
            font=self.default_font,
            text_color="black"
        )
        self.cost_label.pack(anchor="w", pady=(5, 0))

        self.cost_entry = ctk.CTkEntry(
            capacity_section,
            font=self.default_font,
            placeholder_text="Enter event cost",
            height=35,
            border_width=2,
            border_color="#C8A165",
            fg_color="white",
            corner_radius=8
        )
        self.cost_entry.insert(0, str(self.event.cost))
        self.cost_entry.pack(fill="x", pady=(5, 15))

        # Buttons Section
        self.buttons_frame = ctk.CTkFrame(capacity_section, fg_color="transparent")
        self.buttons_frame.pack(pady=(20, 0), fill="x")

        self.save_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Save Changes",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=150,
            height=40,
            corner_radius=8,
            command=self.save_event
        )
        self.save_btn.pack(side="left", padx=10)

        self.cancel_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Cancel",
            fg_color="gray",
            hover_color="#666666",
            font=ctk.CTkFont(family="Roboto", size=14),
            width=150,
            height=40,
            corner_radius=8,
            command=self.cancel_edit
        )
        self.cancel_btn.pack(side="left", padx=10)

    def create_section(self, title):
        """Creates a new section with a title and returns the content frame"""
        section = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        section.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            section,
            text=title,
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold"),
            text_color="black"
        )
        title_label.pack(anchor="w", pady=(0, 10))
        
        separator = ctk.CTkFrame(section, height=2, fg_color="#E5E5E5")
        separator.pack(fill="x", pady=(0, 10))
        
        return section

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
            self.show_error(f"Maximum participants cannot be less than current participants ({current_participants}).")
            return

        if updated_cost < 0:
            self.show_error("Cost cannot be negative.")
            return

        if Event.is_title_duplicate(updated_title, ignore_id=self.event.event_id):
            self.show_error("An event with this title already exists.")
            return

        class SimpleUser:
            def __init__(self, user_id):
                self.user_id = user_id

        user = SimpleUser(self.event.organizer_id)

        manage_event = ManageEvent(user)   
        manage_event.event_id = self.event.event_id
        manage_event.title = updated_title 
        manage_event.event_date = updated_date
        manage_event.venue = updated_location
        manage_event.description = updated_desc
        manage_event.is_public = (updated_visibility == "public")
        manage_event.category = updated_category
        manage_event.max_participants = updated_max_participants
        manage_event.cost = updated_cost
        manage_event.is_paid = updated_cost > 0
        manage_event.status = self.event.status  
        
        success, msg = manage_event.edit_event()
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
        result = CTkMessagebox(
            title="Confirm",
            message=message,
            icon="question",
            option_1="Yes",
            option_2="No"
        )
        return result.get() == "Yes"

    def show_error(self, message):
        CTkMessagebox(title="Error", message=message, icon="cancel")

    def show_success(self, message):
        CTkMessagebox(title="Success", message=message, icon="check")
