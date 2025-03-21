import customtkinter as ctk
from datetime import datetime
import time
import threading

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
        
        # Mock events data
        self.mock_events = [
            {
                "id": 1,
                "title": "Tech Conference 2025",
                "date": "2025-04-15 09:00",
                "location": "Athens Convention Center",
                "description": "Annual tech conference featuring industry leaders."
            },
            {
                "title": "Summer Music Festival",
                "date": "2025-06-20 18:00",
                "location": "Thessaloniki Park",
                "description": "Enjoy live performances from top artists."
            },
            {
                "title": "Art & Culture Expo",
                "date": "2025-05-10 10:00",
                "location": "Heraklion Art Museum",
                "description": "Explore modern art exhibitions and workshops."
            }
        ]
        
        # Display events
        self.display_events()
    
    def display_events(self):
        for event in self.mock_events:
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
                text=event["title"],
                font=ctk.CTkFont(family="Roboto", size=18, weight="bold")
            )
            title_label.pack(anchor="w")
            
            # Date & Time
            dt_label = ctk.CTkLabel(
                content_frame,
                text=f"Date & Time: {event['date']}",
                font=ctk.CTkFont(family="Roboto", size=14)
            )
            dt_label.pack(anchor="w", pady=(5,0))
            
            # Location
            loc_label = ctk.CTkLabel(
                content_frame,
                text=f"Location: {event['location']}",
                font=ctk.CTkFont(family="Roboto", size=14)
            )
            loc_label.pack(anchor="w", pady=(5,0))
            
            # Description
            desc_label = ctk.CTkLabel(
                content_frame,
                text=event["description"],
                font=ctk.CTkFont(family="Roboto", size=14)
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
                command=lambda e=event: self.dashboard.show_event_discussion(e)
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
            command=lambda: [print(f"Withdrawing from {event['title']}"), warning.destroy()]
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
        
        # Grant access button
        grant_btn = ctk.CTkButton(
            perm,
            text="Grant Access",
            fg_color="#2196F3",
            hover_color="#1976D2",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            command=lambda: [perm.destroy(), self.start_checkin_progress()]
        )
        grant_btn.pack(pady=20)
    
    def start_checkin_progress(self):
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
            messages = [
                ("Checking location...", 1),
                ("Within event bounds...", 1),
                ("Event Date correct...", 1),
                ("Checked in successfully! Enjoy your event!", 2)
            ]
            
            for msg, delay in messages:
                progress_label.configure(text=msg)
                progress.update()
                time.sleep(delay)
            
            progress.destroy()
            
            # Show success window
            success = ctk.CTkToplevel(self)
            success.title("Success!")
            success.geometry("400x150")
            success.transient(self)
            success.grab_set()
            
            # Center window
            success.update_idletasks()
            x = (success.winfo_screenwidth() - success.winfo_width()) // 2
            y = (success.winfo_screenheight() - success.winfo_height()) // 2
            success.geometry(f"+{x}+{y}")
            
            # Success message
            ctk.CTkLabel(
                success,
                text="You have successfully checked in to the event!",
                font=ctk.CTkFont(family="Roboto", size=16)
            ).pack(expand=True)
            
            # OK button
            ctk.CTkButton(
                success,
                text="OK",
                fg_color="#4CAF50",
                hover_color="#45a049",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                command=success.destroy
            ).pack(pady=20)
        
        # Start progress in a separate thread
        threading.Thread(target=update_progress).start()
