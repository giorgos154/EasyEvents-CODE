from datetime import datetime
import customtkinter as ctk
from src.classes.event.event import Event
import customtkinter.messagebox as messagebox
from src.classes.event import Event


class EditEventPage(ctk.CTkFrame):
    def __init__(self, master, dashboard, event_id):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard

        self.event = Event.find_by_id(event_id)  
        self.event = Event.find_by_id(event_id)


        if not self.event:
            self.show_error("Event not found!")
            return


        # Header
        self.header = ctk.CTkLabel(self, text="Edit Event", 
                                   font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)
        
        # Form Section
        self.form_frame = ctk.CTkFrame(self, fg_color="white")
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Event Title
        self.title_label = ctk.CTkLabel(self.form_frame, text="Event Title", font=ctk.CTkFont(family="Roboto", size=14))
        self.title_label.pack(anchor="w", pady=(5, 0))
        
        self.title_entry = ctk.CTkEntry(self.form_frame, font=ctk.CTkFont(family="Roboto", size=14), placeholder_text="Enter event title")
        self.title_entry.insert(0, self.event.title)  
        self.title_entry.pack(fill="x", pady=(5, 15))

        # Date & Time
        self.dt_label = ctk.CTkLabel(self.form_frame, text="Date & Time", font=ctk.CTkFont(family="Roboto", size=14))
        self.dt_label.pack(anchor="w", pady=(5, 0))

        self.dt_entry = ctk.CTkEntry(self.form_frame, font=ctk.CTkFont(family="Roboto", size=14), placeholder_text="Enter event date and time (YYYY-MM-DD HH:MM)")
        self.dt_entry.insert(0, self.event.event_date.strftime('%Y-%m-%d %H:%M'))  
        self.dt_entry.pack(fill="x", pady=(5, 15))
        
        # Location
        self.loc_label = ctk.CTkLabel(self.form_frame, text="Location", font=ctk.CTkFont(family="Roboto", size=14))
        self.loc_label.pack(anchor="w", pady=(5, 0))

        self.loc_entry = ctk.CTkEntry(self.form_frame, font=ctk.CTkFont(family="Roboto", size=14), placeholder_text="Enter event location")
        self.loc_entry.insert(0, self.event.venue)  
        self.loc_entry.pack(fill="x", pady=(5, 15))
        
        # Description
        self.desc_label = ctk.CTkLabel(self.form_frame, text="Description", font=ctk.CTkFont(family="Roboto", size=14))
        self.desc_label.pack(anchor="w", pady=(5, 0))

        self.desc_entry = ctk.CTkEntry(self.form_frame, font=ctk.CTkFont(family="Roboto", size=14), placeholder_text="Enter event description")
        self.desc_entry.insert(0, self.event.description) 
        self.desc_entry.pack(fill="x", pady=(5, 15))
        
        # Save Button
        self.save_btn = ctk.CTkButton(self.form_frame, text="Save Changes", fg_color="#4CAF50", hover_color="#45a049", font=ctk.CTkFont(family="Roboto", size=14, weight="bold"), width=150, command=self.save_event)
        self.save_btn.pack(pady=15)

        # Cancel Button
        self.cancel_btn = ctk.CTkButton(self.form_frame, text="Cancel", fg_color="gray", hover_color="#666666", font=ctk.CTkFont(family="Roboto", size=14), width=150, command=self.cancel_edit)
        self.cancel_btn.pack(pady=5)
    
    def save_event(self):
        # Get updated details from form entries
        updated_title = self.title_entry.get()
        updated_dt = self.dt_entry.get()
        updated_location = self.loc_entry.get()
        updated_desc = self.desc_entry.get()
        
        # Validate date format

        self.original_values = {
            "title": self.event.title,
            "event_date": self.event.event_date.strftime('%Y-%m-%d %H:%M'),
            "venue": self.event.venue,
            "description": self.event.description,
            "visibility": self.event.visibility,
            "category": self.event.category,
            "max_participants": str(self.event.max_participants),
            "cost": str(self.event.cost)
        }

        # Header
        self.header = ctk.CTkLabel(self, text="Edit Event",
                                   font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)

        # Form Section
        self.form_frame = ctk.CTkFrame(self, fg_color="white")
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Event Title
        self.title_label = ctk.CTkLabel(self.form_frame, text="Event Title",
                                        font=ctk.CTkFont(family="Roboto", size=14))
        self.title_label.pack(anchor="w", pady=(5, 0))

        self.title_entry = ctk.CTkEntry(self.form_frame,
                                        font=ctk.CTkFont(family="Roboto", size=14),
                                        placeholder_text="Enter event title")
        self.title_entry.insert(0, self.event.title)
        self.title_entry.pack(fill="x", pady=(5, 15))

        # Date & Time
        self.dt_label = ctk.CTkLabel(self.form_frame, text="Date & Time",
                                     font=ctk.CTkFont(family="Roboto", size=14))
        self.dt_label.pack(anchor="w", pady=(5, 0))

        self.dt_entry = ctk.CTkEntry(self.form_frame,
                                     font=ctk.CTkFont(family="Roboto", size=14),
                                     placeholder_text="Enter event date and time (YYYY-MM-DD HH:MM)")
        self.dt_entry.insert(0, self.event.event_date.strftime('%Y-%m-%d %H:%M'))
        self.dt_entry.pack(fill="x", pady=(5, 15))

        # Location
        self.loc_label = ctk.CTkLabel(self.form_frame, text="Location",
                                      font=ctk.CTkFont(family="Roboto", size=14))
        self.loc_label.pack(anchor="w", pady=(5, 0))

        self.loc_entry = ctk.CTkEntry(self.form_frame,
                                      font=ctk.CTkFont(family="Roboto", size=14),
                                      placeholder_text="Enter event location")
        self.loc_entry.insert(0, self.event.venue)
        self.loc_entry.pack(fill="x", pady=(5, 15))

        # Description
        self.desc_label = ctk.CTkLabel(self.form_frame, text="Description",
                                       font=ctk.CTkFont(family="Roboto", size=14))
        self.desc_label.pack(anchor="w", pady=(5, 0))

        self.desc_textbox = ctk.CTkTextbox(self.form_frame, height=100,
                                           font=ctk.CTkFont(family="Roboto", size=14))
        self.desc_textbox.insert("0.0", self.event.description)
        self.desc_textbox.pack(fill="x", pady=(5, 15))

        # Visibility
        self.visibility_label = ctk.CTkLabel(self.form_frame, text="Visibility:",
                                             font=ctk.CTkFont(family="Roboto", size=14))
        self.visibility_label.pack(anchor="w", pady=(5, 0))

        self.visibility_var = ctk.StringVar(value=self.event.visibility)
        self.visibility_optionmenu = ctk.CTkOptionMenu(self.form_frame, variable=self.visibility_var,
                                                       values=["public", "private"])
        self.visibility_optionmenu.pack(fill="x", pady=(5, 15))

        # Category
        self.category_label = ctk.CTkLabel(self.form_frame, text="Category:",
                                           font=ctk.CTkFont(family="Roboto", size=14))
        self.category_label.pack(anchor="w", pady=(5, 0))

        self.category_entry = ctk.CTkEntry(self.form_frame,
                                           font=ctk.CTkFont(family="Roboto", size=14),
                                           placeholder_text="Enter event category")
        self.category_entry.insert(0, self.event.category)
        self.category_entry.pack(fill="x", pady=(5, 15))

        # Max Participants
        self.max_participants_label = ctk.CTkLabel(self.form_frame, text="Max Participants:",
                                                   font=ctk.CTkFont(family="Roboto", size=14))
        self.max_participants_label.pack(anchor="w", pady=(5, 0))

        self.max_participants_entry = ctk.CTkEntry(self.form_frame,
                                                   font=ctk.CTkFont(family="Roboto", size=14),
                                                   placeholder_text="Enter max participants")
        self.max_participants_entry.insert(0, str(self.event.max_participants))
        self.max_participants_entry.pack(fill="x", pady=(5, 15))

        # Cost
        self.cost_label = ctk.CTkLabel(self.form_frame, text="Cost:",
                                       font=ctk.CTkFont(family="Roboto", size=14))
        self.cost_label.pack(anchor="w", pady=(5, 0))

        self.cost_entry = ctk.CTkEntry(self.form_frame,
                                       font=ctk.CTkFont(family="Roboto", size=14),
                                       placeholder_text="Enter event cost")
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

        # Empty fields
        if not updated_title:
            self.show_error("Event title cannot be empty.")
            return
        if not updated_dt:
            self.show_error("Event date and time cannot be empty.")
            return
        if not updated_location:
            self.show_error("Event location cannot be empty.")
            return

        # Length validation
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
            updated_max_participants = int(self.max_participants_entry.get().strip())
            if updated_max_participants <= 0:
                self.show_error("Max Participants must be a positive integer.")
                return
        except ValueError:
            self.show_error("Max Participants must be an integer.")
            return

        try:
            updated_cost = float(self.cost_entry.get().strip())
            if updated_cost < 0:
                self.show_error("Cost cannot be negative.")
                return
        except ValueError:
            self.show_error("Cost must be a number.")
            return


        try:
            updated_date = datetime.strptime(updated_dt, '%Y-%m-%d %H:%M')
        except ValueError:
            self.show_error("Invalid date format. Please use 'YYYY-MM-DD HH:MM'.")
            return


        # Check for duplicate event title
        if self.event.is_title_duplicate(updated_title):
            self.show_error("An event with this title already exists. Please choose a different title.")
            return
        
        # Check for valid cost for free event
        if not self.event.is_paid and float(self.event.cost) > 0:
            self.show_error("For a free event, the cost must be 0.")
            return

        # Check if max participants exceed current participants
        if self.event.current_participants > self.event.max_participants:
            self.show_error(f"The number of participants ({self.event.current_participants}) exceeds the new limit.")
            return

        # Update event object

        if updated_date < datetime.now():
            self.show_error("Event date and time must be in the future.")
            return

        if self.event.is_title_duplicate(updated_title, ignore_id=self.event.id):
            self.show_error("An event with this title already exists. Please choose a different title.")
            return

        if updated_max_participants < self.event.current_participants:
            self.show_error(f"The number of participants ({self.event.current_participants}) exceeds the new max participants.")
            return

        is_paid = updated_cost > 0


        self.event.title = updated_title
        self.event.event_date = updated_date
        self.event.venue = updated_location
        self.event.description = updated_desc

        
        # Save event to database
        success, msg = self.event.update_event()
        if success:
            self.show_success("Event updated successfully!")
        else:
            self.show_error(msg)
    
    def cancel_edit(self):
        # Go back to Manage Events page
        self.dashboard.show_page("Manage Events")

    def show_error(self, message):
        """Display error message in a dialog"""
        error = ctk.CTkToplevel(self)
        error.title("Error")
        error.geometry("300x150")
        error.transient(self)
        error.grab_set()
        
        # Center window
        error.update_idletasks()
        x = (error.winfo_screenwidth() - error.winfo_width()) // 2
        y = (error.winfo_screenheight() - error.winfo_height()) // 2
        error.geometry(f"+{x}+{y}")
        
        # Error message
        message_label = ctk.CTkLabel(error, text=message, font=ctk.CTkFont(family="Roboto", size=14), text_color="red", justify="center")
        message_label.pack(expand=True)
        
        # OK button
        ok_btn = ctk.CTkButton(error, text="OK", fg_color="gray", hover_color="#666666", font=ctk.CTkFont(family="Roboto", size=14), width=100, command=error.destroy)
        ok_btn.pack(pady=20)

    def show_success(self, message):
        """Display success message"""
        success = ctk.CTkToplevel(self)
        success.title("Success")
        success.geometry("300x150")
        success.transient(self)
        success.grab_set()

        # Center window
        success.update_idletasks()
        x = (success.winfo_screenwidth() - success.winfo_width()) // 2
        y = (success.winfo_screenheight() - success.winfo_height()) // 2
        success.geometry(f"+{x}+{y}")

        # Success message
        message_label = ctk.CTkLabel(success, text=message, font=ctk.CTkFont(family="Roboto", size=14), text_color="green", justify="center")
        message_label.pack(expand=True)

        # OK button
        ok_btn = ctk.CTkButton(success, text="OK", fg_color="#4CAF50", hover_color="#45a049", font=ctk.CTkFont(family="Roboto", size=14), width=100, command=success.destroy)
        ok_btn.pack(pady=20)

        self.event.visibility = updated_visibility
        self.event.category = updated_category
        self.event.max_participants = updated_max_participants
        self.event.cost = updated_cost
        self.event.is_paid = is_paid

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
        current_values = {
            "title": self.title_entry.get().strip(),
            "event_date": self.dt_entry.get().strip(),
            "venue": self.loc_entry.get().strip(),
            "description": self.desc_textbox.get("0.0", "end").strip(),
            "visibility": self.visibility_var.get(),
            "category": self.category_entry.get().strip(),
            "max_participants": self.max_participants_entry.get().strip(),
            "cost": self.cost_entry.get().strip()
        }
        for key, value in current_values.items():
            if value != self.original_values[key]:
                return True
        return False

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def show_success(self, message):
        messagebox.showinfo("Success", message)

    def confirmation_dialog(self, message):
        return messagebox.askyesno("Confirm", message)
>>>>>>> abf4267b57b6d9cf32a3bae290b99e4258b12298
