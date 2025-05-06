import customtkinter as ctk
from datetime import datetime
import time
import threading
from src.classes.event.event import Event

class MyEventsPage(ctk.CTkFrame):
    def __init__(self, master, dashboard):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard
        
        # Header
        self.header = ctk.CTkLabel(self, text="My Events", 
                                   font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)
        
        # Scrollable Event List Section
        self.events_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        self.events_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Get user's events
        self.events = Event.find_user_events(self.dashboard.current_user.user_id)
        
        # Display events
        if not self.events:
            # Show message if no events
            no_events = ctk.CTkLabel(
                self.events_frame,
                text="You haven't joined any events yet.\nCheck Find Events to discover and join events!",
                font=ctk.CTkFont(family="Roboto", size=16),
                justify="center"
            )
            no_events.pack(expand=True, pady=50)
        else:
            self.display_events()
    
    def display_events(self):
        for event in self.events:
            # Event Card
            card = ctk.CTkFrame(self.events_frame, fg_color="white", 
                               border_width=1, border_color="#C8A165")
            card.pack(fill="x", padx=10, pady=10)
            
            # Content Frame (left side)
            content_frame = ctk.CTkFrame(card, fg_color="white")
            content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            
            # Event Title
            title_label = ctk.CTkLabel(
                content_frame,
                text=event.title,
                font=ctk.CTkFont(family="Roboto", size=18, weight="bold")
            )
            title_label.pack(anchor="w")
            
            # Date & Time
            dt_label = ctk.CTkLabel(
                content_frame,
                text=f"Date & Time: {event.event_date.strftime('%Y-%m-%d %H:%M')}",
                font=ctk.CTkFont(family="Roboto", size=14)
            )
            dt_label.pack(anchor="w", pady=(5,0))
            
            # Location
            loc_label = ctk.CTkLabel(
                content_frame,
                text=f"Location: {event.venue}",
                font=ctk.CTkFont(family="Roboto", size=14)
            )
            loc_label.pack(anchor="w", pady=(5,0))
            
            # Description
            desc_label = ctk.CTkLabel(
                content_frame,
                text=event.description,
                font=ctk.CTkFont(family="Roboto", size=14),
                wraplength=500
            )
            desc_label.pack(anchor="w", pady=(5,0))
            
            # Buttons Frame (right side)
            buttons_frame = ctk.CTkFrame(card, fg_color="white")
            buttons_frame.pack(side="right", padx=10, pady=10)
            
            # Discussion button
            discussion_btn = ctk.CTkButton(
                buttons_frame,
                text="Discussion →",
                fg_color="#C8A165",
                hover_color="#b38e58",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                width=120,
                height=35,
                corner_radius=8,
                text_color="black",
                command=lambda e=event: self.dashboard.show_event_discussion(e.event_id)
            )
            discussion_btn.pack(pady=(0,5))
            
            # Check-in button
            checkin_btn = ctk.CTkButton(
                buttons_frame,
                text="Check-in  ✓",
                fg_color="#4CAF50",
                hover_color="#45a049",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                width=120,
                height=35,
                corner_radius=8,
                command=lambda e=event: self.show_checkin_sequence(e)
            )
            checkin_btn.pack(pady=5)
            
            # Withdraw button
            withdraw_btn = ctk.CTkButton(
                buttons_frame,
                text="Withdraw  ×",
                fg_color="#f44336",
                hover_color="#e53935",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                width=120,
                height=35,
                corner_radius=8,
                command=lambda e=event: self.show_withdraw_warning(e)
            )
            withdraw_btn.pack(pady=(5,0))

    def show_withdraw_warning(self, event):
        # Create warning window
        warning = ctk.CTkToplevel(self)
        warning.title("Warning!")
        warning.geometry("400x200")
        warning.transient(self)
        warning.grab_set()
        
        # Center window
        warning.update_idletasks()
        x = (warning.winfo_screenwidth() - warning.winfo_width()) // 2
        y = (warning.winfo_screenheight() - warning.winfo_height()) // 2
        warning.geometry(f"+{x}+{y}")
        
        # Warning message
        message = ctk.CTkLabel(
            warning,
            text=("Are you sure you want to withdraw from this event?\n\n"
                  "Note: Withdrawing less than 24 hours before the event\n"
                  "may result in penalties and loss of any points."),
            font=ctk.CTkFont(family="Roboto", size=14)
        )
        message.pack(expand=True, padx=20)
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(warning, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        # Confirm button
        confirm_btn = ctk.CTkButton(
            btn_frame,
            text="Confirm",
            fg_color="#f44336",
            hover_color="#e53935",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            command=lambda: [print(f"Withdrawing from {event.title}"), warning.destroy()]
        )
        confirm_btn.pack(side="left", padx=10)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            fg_color="gray",
            hover_color="#666666",
            font=ctk.CTkFont(family="Roboto", size=14),
            width=100,
            command=warning.destroy
        )
        cancel_btn.pack(side="left", padx=10)
    
    def show_checkin_sequence(self, event):
        # Check if event is happening today
        today = datetime.now().date()
        event_date = event.event_date.date()

        if event_date > today:
            self.show_error("Check-in is not available before the event date.")
            return
        elif event_date < today:
            self.show_error("This event has already passed.")
            return

        # Location permission window
        perm = ctk.CTkToplevel(self)
        perm.title("Location Access")
        perm.geometry("400x150")
        perm.transient(self)
        perm.grab_set()
        
        # Center window
        perm.update_idletasks()
        x = (perm.winfo_screenwidth() - perm.winfo_width()) // 2
        y = (perm.winfo_screenheight() - perm.winfo_height()) // 2
        perm.geometry(f"+{x}+{y}")
        
        # Permission message
        message = ctk.CTkLabel(
            perm,
            text="Allow EasyEvents to access your location?",
            font=ctk.CTkFont(family="Roboto", size=14)
        )
        message.pack(expand=True)
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(perm, fg_color="transparent")
        btn_frame.pack(pady=20)

        # Grant access button
        grant_btn = ctk.CTkButton(
            btn_frame,
            text="Grant Access",
            fg_color="#2196F3",
            hover_color="#1976D2",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=120,
            command=lambda: [perm.destroy(), self.start_checkin_progress(event)]
        )
        grant_btn.pack(side="left", padx=10)

        # Deny button
        deny_btn = ctk.CTkButton(
            btn_frame,
            text="Deny",
            fg_color="gray",
            hover_color="#666666",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            command=lambda: [perm.destroy(), 
                           self.show_error("Location access is required to record check-in.")]
        )
        deny_btn.pack(side="left", padx=10)
    
    def start_checkin_progress(self, event):
        from src.classes.services.location_service import LocationService

        # Progress window
        progress = ctk.CTkToplevel(self)
        progress.title("Checking In...")
        progress.geometry("400x150")
        progress.transient(self)
        progress.grab_set()
        
        # Center window
        progress.update_idletasks()
        x = (progress.winfo_screenwidth() - progress.winfo_width()) // 2
        y = (progress.winfo_screenheight() - progress.winfo_height()) // 2
        progress.geometry(f"+{x}+{y}")
        
        # Progress label
        progress_label = ctk.CTkLabel(
            progress,
            text="",
            font=ctk.CTkFont(family="Roboto", size=16)
        )
        progress_label.pack(expand=True)
        
        def update_progress():
            # Get user location
            user_location = LocationService.get_current_location()
            progress_label.configure(text="Checking your location...")
            progress.update()
            time.sleep(1)
            
            # Get venue location
            venue_location = LocationService.get_venue_coordinates(event.venue)
            progress_label.configure(text="Verifying proximity to venue...")
            progress.update()
            time.sleep(2)
            
            # Verify location
            is_valid, msg = LocationService.verify_in_radius(user_location, venue_location)
            if not is_valid:
                progress.destroy()
                self.show_error(msg)
                return
                
            progress_label.configure(text="Processing check-in...")
            progress.update()
            time.sleep(2)
            
            # Record check-in
            from src.classes.event.eventParticipation import EventParticipation
            participation = EventParticipation.find_by_event_user(event.event_id, self.dashboard.current_user.user_id)
            if not participation:
                progress.destroy()
                self.show_error("Not registered for this event")
                return

            success, msg = participation.check_in()
            if not success:
                progress.destroy()
                self.show_error(msg)
                return
            
            # Notify organizer
            from src.classes.services.notification_service import NotificationService
            NotificationService.notify_check_in(
                event.organizer_id,
                event.title,
                self.dashboard.current_user.username
            )
            
            progress.destroy()

            # Show success window
            success = ctk.CTkToplevel(self)
            success.title("Success!")
            success.geometry("400x200")
            success.transient(self)
            success.grab_set()
            
            # Center window
            success.update_idletasks()
            x = (success.winfo_screenwidth() - success.winfo_width()) // 2
            y = (success.winfo_screenheight() - success.winfo_height()) // 2
            success.geometry(f"+{x}+{y}")
            
            # Success message
            message = ctk.CTkLabel(
                success,
                text="You have successfully checked in to the event!",
                font=ctk.CTkFont(family="Roboto", size=16)
            )
            message.pack(expand=True)
            
            # View Ticket button
            view_btn = ctk.CTkButton(
                success,
                text="View E-Ticket",
                fg_color="#4CAF50",
                hover_color="#45a049",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                command=lambda: [
                    success.destroy(), 
                    self.show_ticket(event, participation)
                ]
            )
            view_btn.pack(pady=20)
        
        threading.Thread(target=update_progress).start()

    def show_ticket(self, event, participation):
        """Display e-ticket with QR code"""
        # Generate ticket info
        qr_code = participation.generate_ticket()
        ticket_info = participation.get_ticket_info()
        if not qr_code or not ticket_info:
            self.show_error("Could not generate ticket")
            return

        # Show ticket window
        ticket_win = ctk.CTkToplevel(self)
        ticket_win.title("E-Ticket")
        ticket_win.geometry("400x600")
        ticket_win.transient(self)
        ticket_win.grab_set()
        
        # Center window
        ticket_win.update_idletasks()
        x = (ticket_win.winfo_screenwidth() - ticket_win.winfo_width()) // 2
        y = (ticket_win.winfo_screenheight() - ticket_win.winfo_height()) // 2
        ticket_win.geometry(f"+{x}+{y}")
        
        # Header
        header = ctk.CTkLabel(
            ticket_win,
            text="Your E-Ticket",
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold")
        )
        header.pack(pady=20)
        
        # Event details
        details = ctk.CTkLabel(
            ticket_win,
            text=f"Event: {ticket_info['event_title']}\n"
                 f"Date: {ticket_info['event_date'].strftime('%Y-%m-%d %H:%M')}\n"
                 f"Venue: {ticket_info['venue']}\n"
                 f"Attendee: {ticket_info['attendee']}\n",
            font=ctk.CTkFont(family="Roboto", size=14)
        )
        details.pack(pady=20)
        
        # QR Code
        from PIL import ImageTk
        qr_photo = ImageTk.PhotoImage(qr_code)
        qr_label = ctk.CTkLabel(
            ticket_win,
            text="",  
            image=qr_photo
        )
        qr_label.image = qr_photo 
        qr_label.pack(pady=20)
        
        # Close button
        ctk.CTkButton(
            ticket_win,
            text="Close",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            command=ticket_win.destroy
        ).pack(pady=20)

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
        message_label = ctk.CTkLabel(
            error,
            text=message,
            font=ctk.CTkFont(family="Roboto", size=14),
            text_color="red",
            justify="center"
        )
        message_label.pack(expand=True)
        
        # OK button
        ok_btn = ctk.CTkButton(
            error,
            text="OK",
            fg_color="gray",
            hover_color="#666666",
            font=ctk.CTkFont(family="Roboto", size=14),
            width=100,
            command=error.destroy
        )
        ok_btn.pack(pady=20)
