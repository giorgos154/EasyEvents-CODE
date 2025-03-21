import customtkinter as ctk

class RateEventsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        
        # Header
        self.header = ctk.CTkLabel(self, text="Rate Events", 
                                   font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)
        
        # Events List Section
        self.events_label = ctk.CTkLabel(
            self,
            text="Available Events to Rate",
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold")
        )
        self.events_label.pack(padx=20, anchor="w")
        
        # Scrollable Events List
        self.events_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        self.events_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Mock Events Data
        self.mock_events = [
            {
                "id": 1,
                "title": "Tech Conference 2025",
                "date": "2025-04-15",
                "location": "Athens Convention Center",
                "rated": False
            },
            {
                "id": 2,
                "title": "Summer Music Festival",
                "date": "2025-06-20",
                "location": "Thessaloniki Park",
                "rated": True
            },
            {
                "id": 3,
                "title": "Art & Culture Expo",
                "date": "2025-05-10",
                "location": "Heraklion Art Museum",
                "rated": False
            },
            {
                "id": 4,
                "title": "Sports Tournament",
                "date": "2025-07-05",
                "location": "Patras Stadium",
                "rated": True
            }
        ]
        
        # Display Events
        self.display_events()
    
    def display_events(self):
        # Clear existing events
        for widget in self.events_frame.winfo_children():
            widget.destroy()
            
        for event in self.mock_events:
            # Event Card
            card = ctk.CTkFrame(self.events_frame, fg_color="white",
                               border_width=1, border_color="#E5E5E5")
            card.pack(fill="x", padx=5, pady=5)
            
            # Left side content
            content = ctk.CTkFrame(card, fg_color="white")
            content.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            
            # Event Title
            title = ctk.CTkLabel(
                content,
                text=event["title"],
                font=ctk.CTkFont(family="Roboto", size=16, weight="bold")
            )
            title.pack(anchor="w")
            
            # Date
            date = ctk.CTkLabel(
                content,
                text=f"📅 {event['date']}",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="gray"
            )
            date.pack(anchor="w", pady=(5,0))
            
            # Location
            location = ctk.CTkLabel(
                content,
                text=f"📍 {event['location']}",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="gray"
            )
            location.pack(anchor="w", pady=(5,0))
            
            # Right side - Rate button or Already Rated label
            if not event["rated"]:
                rate_btn = ctk.CTkButton(
                    card,
                    text="Rate & Review",
                    font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                    fg_color="#C8A165",
                    hover_color="#b38e58",
                    width=120,
                    height=35,
                    corner_radius=8,
                    command=lambda e=event: self.show_rating_dialog(e)
                )
                rate_btn.pack(side="right", padx=10)
            else:
                rated_label = ctk.CTkLabel(
                    card,
                    text="✓ Already Rated",
                    font=ctk.CTkFont(family="Roboto", size=14),
                    text_color="#4CAF50"
                )
                rated_label.pack(side="right", padx=10)
    
    def show_rating_dialog(self, event):
        # Create popup dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Rate Event")
        dialog.geometry("400x500")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog on screen
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Dialog content
        title = ctk.CTkLabel(
            dialog,
            text=f"Rate {event['title']}",
            font=ctk.CTkFont(family="Roboto", size=20, weight="bold")
        )
        title.pack(pady=20, padx=20)
        
        # Event Rating
        event_rating_label = ctk.CTkLabel(
            dialog,
            text="Event Rating:",
            font=ctk.CTkFont(family="Roboto", size=16)
        )
        event_rating_label.pack(pady=(20,5), padx=20, anchor="w")
        
        event_stars = ctk.CTkFrame(dialog, fg_color="transparent")
        event_stars.pack(fill="x", padx=20)
        for i in range(5):
            star_btn = ctk.CTkButton(
                event_stars,
                text="★",
                width=30,
                height=30,
                fg_color="transparent",
                text_color="#C8A165",
                hover_color="#F0F0F0",
                font=ctk.CTkFont(family="Roboto", size=20)
            )
            star_btn.pack(side="left", padx=2)
        
        # Organizer Rating
        org_rating_label = ctk.CTkLabel(
            dialog,
            text="Organizer Rating:",
            font=ctk.CTkFont(family="Roboto", size=16)
        )
        org_rating_label.pack(pady=(20,5), padx=20, anchor="w")
        
        org_stars = ctk.CTkFrame(dialog, fg_color="transparent")
        org_stars.pack(fill="x", padx=20)
        for i in range(5):
            star_btn = ctk.CTkButton(
                org_stars,
                text="★",
                width=30,
                height=30,
                fg_color="transparent",
                text_color="#C8A165",
                hover_color="#F0F0F0",
                font=ctk.CTkFont(family="Roboto", size=20)
            )
            star_btn.pack(side="left", padx=2)
        
        # Comment Box
        comment_label = ctk.CTkLabel(
            dialog,
            text="Your Review:",
            font=ctk.CTkFont(family="Roboto", size=16)
        )
        comment_label.pack(pady=(20,5), padx=20, anchor="w")
        
        comment_box = ctk.CTkTextbox(
            dialog,
            height=100,
            font=ctk.CTkFont(family="Roboto", size=14)
        )
        comment_box.pack(fill="x", padx=20, pady=(0,20))
        
        # Submit Button
        submit_btn = ctk.CTkButton(
            dialog,
            text="Submit Review",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            fg_color="#C8A165",
            hover_color="#b38e58",
            width=200,
            height=40,
            corner_radius=8,
            command=lambda: self.submit_review(dialog, event)
        )
        submit_btn.pack(pady=20)
    
    def submit_review(self, dialog, event):
        dialog.destroy()
        
        # Show success message
        success = ctk.CTkDialog(
            master=self,
            title="Success!",
            text="Your review has been submitted.",
            corner_radius=10
        )
        success.get_button("OK").configure(
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold")
        )
        
        # Update event status
        for e in self.mock_events:
            if e["id"] == event["id"]:
                e["rated"] = True
                break
        
        # Refresh display
        self.display_events()
