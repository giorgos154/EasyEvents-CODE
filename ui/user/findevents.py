import customtkinter as ctk
from datetime import datetime
from tkcalendar import DateEntry

class FindEventsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        # Header
        self.header = ctk.CTkLabel(self, text="Find Events", 
                                   font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)
        
        # Main filter container
        self.filter_frame = ctk.CTkFrame(self, fg_color="white")
        self.filter_frame.pack(fill="x", padx=20, pady=(0,20))
        
        # Configure grid weights
        self.filter_frame.grid_columnconfigure(0, weight=1)  # left side
        self.filter_frame.grid_columnconfigure(1, weight=1)  # right side
        
        # Left Frame - dropdowns section
        self.left_filter = ctk.CTkFrame(self.filter_frame, fg_color="white")
        self.left_filter.grid(row=0, column=0, sticky="nsew", padx=(0,20))
        
        # City Dropdown
        cities = [
            "All Cities", "Athens", "Thessaloniki", "Patras", "Heraklion", "Larissa",
            "Volos", "Ioannina", "Chania", "Kalamata", "Rhodes"
        ]
        self.city_dropdown = ctk.CTkComboBox(self.left_filter, values=cities,
                                             font=ctk.CTkFont(family="Roboto", size=14), width=200)
        self.city_dropdown.set("All Cities")
        self.city_dropdown.pack(pady=(0,10), fill="x")
        
        # Category Dropdown
        self.categories = ["All Categories", "Conferences", "Workshops", "Sports", "Music", 
                           "Arts & Culture", "Food & Drink", "Networking"]
        self.category_dropdown = ctk.CTkComboBox(self.left_filter, values=self.categories,
                                                 font=ctk.CTkFont(family="Roboto", size=14), width=200)
        self.category_dropdown.set("All Categories")
        self.category_dropdown.pack(fill="x")
        
        # Right Frame - dates
        self.right_filter = ctk.CTkFrame(self.filter_frame, fg_color="white")
        self.right_filter.grid(row=0, column=1, sticky="nsew")
        self.right_filter.grid_columnconfigure(0, weight=1)
        self.right_filter.grid_columnconfigure(1, weight=1)
        
        # Start Date with Label
        self.start_date_label = ctk.CTkLabel(self.right_filter, text="Start Date:",
                                             font=ctk.CTkFont(family="Roboto", size=14))
        self.start_date_label.grid(row=0, column=0, pady=(0,5))
        self.start_date_entry = DateEntry(self.right_filter, width=15, background='#C8A165',
                                         foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',
                                         font=("Roboto", 12))
        self.start_date_entry.grid(row=1, column=0, padx=20)
        
        # End Date with Label
        self.end_date_label = ctk.CTkLabel(self.right_filter, text="End Date:", 
                                           font=ctk.CTkFont(family="Roboto", size=14))
        self.end_date_label.grid(row=0, column=1, pady=(0,5))
        self.end_date_entry = DateEntry(self.right_filter, width=15, background='#C8A165',
                                       foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',
                                       font=("Roboto", 12))
        self.end_date_entry.grid(row=1, column=1, padx=20)
        
        # Sort and Search Panel
        self.sort_frame = ctk.CTkFrame(self, fg_color="white")
        self.sort_frame.pack(fill="x", padx=20, pady=(20,20))
        
        # Left side - Sort options
        self.sort_label = ctk.CTkLabel(self.sort_frame, text="Sort by:", 
                                       font=ctk.CTkFont(family="Roboto", size=14))
        self.sort_label.pack(side="left", padx=10, pady=10)
        
        sort_options = ["Date (Soonest First)", "Location (Nearest)", "Popularity", "Category"]
        self.sort_dropdown = ctk.CTkComboBox(self.sort_frame, values=sort_options,
                                             font=ctk.CTkFont(family="Roboto", size=14), width=200)
        self.sort_dropdown.set("Date (Soonest First)")
        self.sort_dropdown.pack(side="left", padx=10, pady=10)
        
        # Right side - Search button
        self.search_btn = ctk.CTkButton(self.sort_frame, text="Search  →",
                                        fg_color="#C8A165", hover_color="#b38e58",
                                        font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                                        width=120, height=35, corner_radius=8, text_color="black",
                                        command=self.apply_filters)
        self.search_btn.pack(side="right", padx=20, pady=10)
        
        # Scrollable Event List
        self.events_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        self.events_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Mock events
        self.mock_events = [
            {
                "title": "Tech Conference 2025",
                "category": "Conferences",
                "date": "2025-04-15 09:00",
                "location": "Athens Convention Center",
                "description": "Annual tech conference featuring industry leaders."
            },
            {
                "title": "Summer Music Festival",
                "category": "Music",
                "date": "2025-06-20 18:00",
                "location": "Thessaloniki Park",
                "description": "Enjoy live performances from top artists."
            },
            {
                "title": "Art & Culture Expo",
                "category": "Arts & Culture",
                "date": "2025-05-10 10:00",
                "location": "Heraklion Art Museum",
                "description": "Explore modern art exhibitions and workshops."
            },
            {
                "title": "Sports Tournament",
                "category": "Sports",
                "date": "2025-07-05 14:00",
                "location": "Patras Stadium",
                "description": "Regional sports tournament with multiple competitions."
            },
            {
                "title": "Food & Wine Festival",
                "category": "Food & Drink",
                "date": "2025-08-15 11:00",
                "location": "Larissa Central Plaza",
                "description": "Taste local cuisines and wines from all over Greece."
            }
        ]
        
        self.display_events(self.mock_events)
        
    def display_events(self, events):
        for widget in self.events_frame.winfo_children():
            widget.destroy()
        
        for event in events:
            card = ctk.CTkFrame(self.events_frame, fg_color="white", border_width=1, border_color="#C8A165")
            card.pack(fill="x", padx=10, pady=10)
            
            # Event title
            title_label = ctk.CTkLabel(card, text=event["title"], 
                                        font=ctk.CTkFont(family="Roboto", size=18, weight="bold"))
            title_label.pack(anchor="w", padx=10, pady=(10,0))
            
            # Date & Time
            dt_label = ctk.CTkLabel(card, text=f"Date & Time: {event['date']}", 
                                     font=ctk.CTkFont(family="Roboto", size=14))
            dt_label.pack(anchor="w", padx=10, pady=(5,0))
            
            # Location
            loc_label = ctk.CTkLabel(card, text=f"Location: {event['location']}", 
                                      font=ctk.CTkFont(family="Roboto", size=14))
            loc_label.pack(anchor="w", padx=10, pady=(5,0))
            
            # Description
            desc_label = ctk.CTkLabel(card, text=event["description"], 
                                       font=ctk.CTkFont(family="Roboto", size=14))
            desc_label.pack(anchor="w", padx=10, pady=(5,10))
            
            # Details button
            details_btn = ctk.CTkButton(card, text="Details  →",
                                        fg_color="#C8A165", hover_color="#b38e58",
                                        font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                                        width=120, height=35, corner_radius=8, text_color="black")
            details_btn.pack(anchor="e", padx=10, pady=(0,10))
    
    def apply_filters(self):
        city = self.city_dropdown.get()
        category = self.category_dropdown.get()
        
        filtered_events = self.mock_events
        
        if city != "All Cities":
            filtered_events = [e for e in filtered_events if city in e["location"]]
        
        try:
            start_date = self.start_date_entry.get_date()
            end_date = self.end_date_entry.get_date()
            filtered_events = [
                e for e in filtered_events 
                if start_date <= datetime.strptime(e["date"].split()[0], "%Y-%m-%d").date() <= end_date
            ]
        except Exception as ex:
            print("Date filtering error:", ex)
        
        if category != "All Categories":
            filtered_events = [e for e in filtered_events if e["category"] == category]
        
        self.display_events(filtered_events)
