import customtkinter as ctk
from ui.Organizer.create_event import CreateEventPage

class ManageEventsPage(ctk.CTkFrame):
    def __init__(self, master, dashboard):
        # -- Dimiourgia tou vasikou frame gia ti selida diaxeirisis events -- #
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard
        
        # -- Container gia to periexomeno -- #
        self.content_frame = ctk.CTkFrame(self, fg_color="white")
        self.content_frame.pack(fill="x", padx=20)
        
        # -- Welcome Title -- #
        self.welcome_label = ctk.CTkLabel(
            self.content_frame,
            text="Event Management",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="black"
        )
        self.welcome_label.pack(pady=(10, 5))

        # -- Welcome Subtitle -- #
        self.subtitle_label = ctk.CTkLabel(
            self.content_frame,
            text="Create and manage your events",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.subtitle_label.pack(pady=(0, 15))
        
        # -- Create Event Button -- #
        self.create_event_btn = ctk.CTkButton(
            self.content_frame,
            text="➕ Create New Event",
            font=ctk.CTkFont(size=18),
            fg_color="#C8A165",
            text_color="black",
            hover_color="#b38e58",
            width=300,
            height=50,
            command=self.show_create_event_page
        )
        self.create_event_btn.pack(pady=10)
        
        # -- Scrollable Events List -- #
        self.events_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        self.events_frame.pack(fill="both", expand=True, padx=20, pady=(10, 0))
        
        # -- Mock Events Data -- #
        self.mock_events = [
            {
                "title": "Tech Conference 2025",
                "date": "2025-04-15 09:00",
                "location": "Athens Convention Center",
                "description": "Annual tech conference featuring industry leaders and innovators.",
                "participants": 150,
                "capacity": 200,
                "ticket_price": "€50"
            },
            {
                "title": "Summer Music Festival",
                "date": "2025-06-20 18:00",
                "location": "Thessaloniki Park",
                "description": "A day of live music performances, food, and entertainment.",
                "participants": 500,
                "capacity": 1000,
                "ticket_price": "€25"
            },
            {
                "title": "Art & Culture Expo",
                "date": "2025-05-10 10:00",
                "location": "Heraklion Art Museum",
                "description": "Showcase of local and international artists featuring workshops.",
                "participants": 200,
                "capacity": 300,
                "ticket_price": "€15"
            }
        ]
        
        # -- Display Events -- #
        self.display_events()

    def display_events(self):
        """
        # -- Display event cards in the scrollable frame -- #
        """
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
                font=ctk.CTkFont(family="Roboto", size=18, weight="bold"),
                text_color="black"
            )
            title_label.pack(anchor="w")
            
            # Date & Time
            dt_label = ctk.CTkLabel(
                content_frame,
                text=f"Date & Time: {event['date']}",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="black"
            )
            dt_label.pack(anchor="w", pady=(5,0))
            
            # Location
            loc_label = ctk.CTkLabel(
                content_frame,
                text=f"Location: {event['location']}",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="black"
            )
            loc_label.pack(anchor="w", pady=(5,0))
            
            # Description
            desc_label = ctk.CTkLabel(
                content_frame,
                text=event["description"],
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="black"
            )
            desc_label.pack(anchor="w", pady=(5,0))
            
            # Participants
            part_label = ctk.CTkLabel(
                content_frame,
                text=f"Participants: {event['participants']}/{event['capacity']} | Ticket: {event['ticket_price']}",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="black"
            )
            part_label.pack(anchor="w", pady=(5,0))
            
            # Buttons Frame (right side)
            buttons_frame = ctk.CTkFrame(card, fg_color="white")
            buttons_frame.pack(side="right", padx=10, pady=10)
            
            # Edit button
            edit_btn = ctk.CTkButton(
                buttons_frame,
                text="Edit →",
                fg_color="#C8A165",
                hover_color="#b38e58",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                width=120,
                height=35,
                corner_radius=8,
                text_color="black"
            )
            edit_btn.pack(pady=(0,5))
            
            # Cancel button
            cancel_btn = ctk.CTkButton(
                buttons_frame,
                text="Cancel ✕",
                fg_color="#f44336",
                hover_color="#e53935",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                width=120,
                height=35,
                corner_radius=8
            )
            cancel_btn.pack(pady=5)
            
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
                text_color="black"
            )
            discussion_btn.pack(pady=5)
            
            # Invite Friends button
            invite_btn = ctk.CTkButton(
                buttons_frame,
                text="Invite Friends",
                fg_color="#2196F3",
                hover_color="#1976D2",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                width=120,
                height=35,
                corner_radius=8
            )
            invite_btn.pack(pady=(5,0))
    
    def show_create_event_page(self):
        """
        # -- Metavasi stin selida dimiourgias event -- #
        """
        # -- Katharismos tis trexousas selidas -- #
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # -- Fortosi tis selidas dimiourgias event -- #
        create_page = CreateEventPage(self.master, self)
        create_page.pack(fill="both", expand=True)
