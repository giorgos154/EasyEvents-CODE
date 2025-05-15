from datetime import datetime
import customtkinter as ctk
from src.classes.event import Event  

class EditEventPage(ctk.CTkFrame):
    def __init__(self, master, dashboard, event_id):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard
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
        # Simply go back to the previous page
        self.dashboard.show_previous_page()

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
