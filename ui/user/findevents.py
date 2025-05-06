import customtkinter as ctk
from classes.event.event import Event

class FindEventsPage(ctk.CTkFrame):
    def __init__(self, master, dashboard):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard
        
        # Header
        self.header = ctk.CTkLabel(self, text="Find Events", 
                                   font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)
        
        # Search Frame
        search_frame = ctk.CTkFrame(self, fg_color="white")
        search_frame.pack(fill="x", padx=20, pady=(0,20))
        
        # Search bar
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search events...",
            font=ctk.CTkFont(family="Roboto", size=14),
            width=300,
            textvariable=self.search_var
        )
        search_entry.pack(side="left", padx=(0,10))
        
        # Search button
        search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            fg_color="#C8A165",
            hover_color="#b38e58",
            width=100
        )
        search_btn.pack(side="left")
        
        # Filters Frame
        filters_frame = ctk.CTkFrame(self, fg_color="white")
        filters_frame.pack(fill="x", padx=20, pady=(0,10))
        
        # First row of filters
        filter_row1 = ctk.CTkFrame(filters_frame, fg_color="white")
        filter_row1.pack(fill="x", pady=5)
        
        # Category Filter
        ctk.CTkLabel(filter_row1, text="Category:", font=ctk.CTkFont(family="Roboto", size=14)).pack(side="left")
        categories = ["All Categories", "Technology", "Music", "Art", "Food", "Sports", "Business", "Education"]
        category_menu = ctk.CTkOptionMenu(
            filter_row1,
            values=categories,
            fg_color="#C8A165",
            button_color="#b38e58",
            width=150
        )
        category_menu.pack(side="left", padx=(10,20))
        
        # City Filter
        ctk.CTkLabel(filter_row1, text="City:", font=ctk.CTkFont(family="Roboto", size=14)).pack(side="left")
        cities = ["All Cities", "Athens", "Thessaloniki", "Patras", "Heraklion", "Larissa", 
                 "Volos", "Ioannina", "Chania", "Rhodes", "Kalamata"]
        city_menu = ctk.CTkOptionMenu(
            filter_row1,
            values=cities,
            fg_color="#C8A165",
            button_color="#b38e58",
            width=150
        )
        city_menu.pack(side="left", padx=(10,20))
        
        # Second row of filters
        filter_row2 = ctk.CTkFrame(filters_frame, fg_color="white")
        filter_row2.pack(fill="x", pady=5)
        
        # Price Range Filter
        ctk.CTkLabel(filter_row2, text="Price:", font=ctk.CTkFont(family="Roboto", size=14)).pack(side="left")
        price_ranges = ["All Prices", "0-25€", "26-50€", "51-100€", "100€+"]
        price_menu = ctk.CTkOptionMenu(
            filter_row2,
            values=price_ranges,
            fg_color="#C8A165",
            button_color="#b38e58",
            width=150
        )
        price_menu.pack(side="left", padx=(10,20))
        
        # Date Filter
        ctk.CTkLabel(filter_row2, text="Date:", font=ctk.CTkFont(family="Roboto", size=14)).pack(side="left")
        date_options = ["Any Date", "Today", "This Week", "This Month", "Next Month"]
        date_menu = ctk.CTkOptionMenu(
            filter_row2,
            values=date_options,
            fg_color="#C8A165",
            button_color="#b38e58",
            width=150
        )
        date_menu.pack(side="left", padx=(10,20))
        
        # Sort Frame
        sort_frame = ctk.CTkFrame(filters_frame, fg_color="white")
        sort_frame.pack(fill="x", pady=5)
        
        # Sort Options
        ctk.CTkLabel(sort_frame, text="Sort by:", font=ctk.CTkFont(family="Roboto", size=14)).pack(side="left")
        sort_options = ["Date ↑", "Date ↓", "Price ↑", "Price ↓", "Popularity"]
        sort_menu = ctk.CTkOptionMenu(
            sort_frame,
            values=sort_options,
            fg_color="#C8A165",
            button_color="#b38e58",
            width=150
        )
        sort_menu.pack(side="left", padx=(10,20))
        
        # Set default values
        category_menu.set("All Categories")
        city_menu.set("All Cities")
        price_menu.set("All Prices")
        date_menu.set("Any Date")
        sort_menu.set("Date ↑")
        
        # Separator
        separator = ctk.CTkFrame(self, height=2, fg_color="#E5E5E5")
        separator.pack(fill="x", padx=20, pady=10)
        
        # Scrollable Events List Section
        self.events_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        self.events_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Get and display events
        self.display_events()
    
    def display_events(self):
        # Fetch all events from database
        events = Event.find_all_events()
        for event in events:
            # Event Card
            card = ctk.CTkFrame(self.events_frame, fg_color="white", 
                               border_width=1, border_color="#E5E5E5")
            card.pack(fill="x", padx=10, pady=10)
            
            # Content Frame (left side)
            content_frame = ctk.CTkFrame(card, fg_color="white", width=500)
            content_frame.pack_propagate(False)  # Prevent resizing
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
                wraplength=500,
                justify="left"
            )
            desc_label.pack(anchor="w", pady=(5,0))
            
            # Tags Frame
            tags_frame = ctk.CTkFrame(content_frame, fg_color="white")
            tags_frame.pack(anchor="w", pady=(10,0))
            
            # Show category as tag
            tag_label = ctk.CTkLabel(
                tags_frame,
                text=event.category,
                font=ctk.CTkFont(family="Roboto", size=12),
                fg_color="#E5E5E5",
                corner_radius=12,
                padx=10,
                pady=5
            )
            tag_label.pack(side="left", padx=5)
            
            # Buttons Frame (right side)
            buttons_frame = ctk.CTkFrame(card, fg_color="white", width=150)
            buttons_frame.pack_propagate(False) 
            buttons_frame.pack(side="right", padx=10, pady=10)
            
           
            buttons_frame.grid_columnconfigure(0, weight=1)  
            buttons_frame.grid_rowconfigure((0, 1, 2), weight=1)  
            
            # Price Label
            # Format price display
            price_text = f"€{event.cost:.2f}" if event.is_paid else "Free"
            price_label = ctk.CTkLabel(
                buttons_frame,
                text=price_text,
                font=ctk.CTkFont(family="Roboto", size=24, weight="bold"),
                text_color="#C8A165"
            )
            price_label.grid(row=1, column=0, pady=(10,10))
            
            # Details button
            details_btn = ctk.CTkButton(
                buttons_frame,
                text="Details  →",
                fg_color="#C8A165",
                hover_color="#b38e58",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                width=120,
                height=35,
                corner_radius=8,
                text_color="black",
                command=lambda eid=event.event_id: self.dashboard.show_event_details(eid)
            )
            details_btn.grid(row=2, column=0, pady=(0,10))
