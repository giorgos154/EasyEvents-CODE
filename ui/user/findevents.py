import customtkinter as ctk
from datetime import datetime, timedelta
from src.classes.event.event import Event

def get_events_from_db():
    # Xrisi tis methodou find_all_events() apo tin klasi Event
    events_list = Event.find_all_events()
    
    # Metatropi Event objects se lista
    events = []
    for event in events_list:
        events.append({
            "title": event.title,
            "date": event.event_date.strftime("%Y-%m-%d %H:%M"),
            "location": event.venue,
            "description": event.description,
            "price": f"{int(event.cost)}€" if event.is_paid else "0€",  # Format gia times / Free events
            "event_id": event.event_id,  # Add event_id for details page
            "is_paid": event.is_paid  # Add is_paid flag for price display
        })

    return events


class FindEventsPage(ctk.CTkFrame):
    def __init__(self, master, dashboard):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard

        self.header = ctk.CTkLabel(self, text="Find Events",
                                   font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)

        search_frame = ctk.CTkFrame(self, fg_color="white")
        search_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search events...",
            font=ctk.CTkFont(family="Roboto", size=14),
            width=300,
            textvariable=self.search_var
        )
        search_entry.pack(side="left", padx=(0, 10))

        search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            fg_color="#C8A165",
            hover_color="#b38e58",
            width=100,
            command=self.filter_and_search_events
        )
        search_btn.pack(side="left")

        filters_frame = ctk.CTkFrame(self, fg_color="white")
        filters_frame.pack(fill="x", padx=20, pady=(0, 10))

        filter_row1 = ctk.CTkFrame(filters_frame, fg_color="white")
        filter_row1.pack(fill="x", pady=5)

        ctk.CTkLabel(filter_row1, text="Category:", font=ctk.CTkFont(family="Roboto", size=14)).pack(side="left")
        categories = ["All Categories", "Technology", "Music", "Art", "Food", "Sports", "Business", "Education"]
        self.category_menu = ctk.CTkOptionMenu(filter_row1, values=categories, fg_color="#C8A165",
                                               button_color="#b38e58", width=150)
        self.category_menu.pack(side="left", padx=(10, 20))

        ctk.CTkLabel(filter_row1, text="City:", font=ctk.CTkFont(family="Roboto", size=14)).pack(side="left")
        cities = ["All Cities", "Athens", "Thessaloniki", "Patras", "Heraklion", "Larissa", "Volos", "Ioannina",
                  "Chania", "Rhodes", "Kalamata"]
        self.city_menu = ctk.CTkOptionMenu(filter_row1, values=cities, fg_color="#C8A165", button_color="#b38e58",
                                           width=150)
        self.city_menu.pack(side="left", padx=(10, 20))

        filter_row2 = ctk.CTkFrame(filters_frame, fg_color="white")
        filter_row2.pack(fill="x", pady=5)

        ctk.CTkLabel(filter_row2, text="Price:", font=ctk.CTkFont(family="Roboto", size=14)).pack(side="left")
        price_ranges = ["All Prices", "0-25€", "26-50€", "51-100€", "100€+"]
        self.price_menu = ctk.CTkOptionMenu(filter_row2, values=price_ranges, fg_color="#C8A165",
                                            button_color="#b38e58", width=150)
        self.price_menu.pack(side="left", padx=(10, 20))

        ctk.CTkLabel(filter_row2, text="Date:", font=ctk.CTkFont(family="Roboto", size=14)).pack(side="left")
        date_options = ["Any Date", "Today", "This Week", "This Month", "Next Month"]
        self.date_menu = ctk.CTkOptionMenu(filter_row2, values=date_options, fg_color="#C8A165", button_color="#b38e58",
                                           width=150)
        self.date_menu.pack(side="left", padx=(10, 20))

        sort_frame = ctk.CTkFrame(filters_frame, fg_color="white")
        sort_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(sort_frame, text="Sort by:", font=ctk.CTkFont(family="Roboto", size=14)).pack(side="left")
        sort_options = ["Date ↑", "Date ↓", "Price ↑", "Price ↓", "Popularity"]
        self.sort_menu = ctk.CTkOptionMenu(sort_frame, values=sort_options, fg_color="#C8A165", button_color="#b38e58",
                                           width=150)
        self.sort_menu.pack(side="left", padx=(10, 20))

        self.category_menu.set("All Categories")
        self.city_menu.set("All Cities")
        self.price_menu.set("All Prices")
        self.date_menu.set("Any Date")
        self.sort_menu.set("Date ↑")

        separator = ctk.CTkFrame(self, height=2, fg_color="#E5E5E5")
        separator.pack(fill="x", padx=20, pady=10)

        self.events_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        self.events_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.mock_events = get_events_from_db()
        self.display_filtered_events(self.mock_events)

    def filter_and_search_events(self):
        search_text = self.search_var.get().lower()
        selected_category = self.category_menu.get()
        selected_city = self.city_menu.get()
        selected_price = self.price_menu.get()
        selected_date = self.date_menu.get()
        sort_option = self.sort_menu.get()

        filtered = []
        for event in self.mock_events:
            if not self.matches_search(event, search_text):
                continue
            if not self.matches_category(event, selected_category):
                continue
            if not self.matches_city(event, selected_city):
                continue
            if not self.matches_price(event, selected_price):
                continue
            if not self.matches_date(event, selected_date):
                continue
            filtered.append(event)

        sorted_events = self.sort_events(filtered, sort_option)

        for widget in self.events_frame.winfo_children():
            widget.destroy()

        self.display_filtered_events(sorted_events)

    def display_filtered_events(self, events):
        for event in events:
            card = ctk.CTkFrame(self.events_frame, fg_color="white", border_width=1, border_color="#E5E5E5")
            card.pack(fill="x", padx=10, pady=10)

            content_frame = ctk.CTkFrame(card, fg_color="white")
            content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

            ctk.CTkLabel(content_frame, text=event["title"],
                         font=ctk.CTkFont(family="Roboto", size=18, weight="bold")).pack(anchor="w")
            ctk.CTkLabel(content_frame, text=f"Date & Time: {event['date']}",
                         font=ctk.CTkFont(family="Roboto", size=14)).pack(anchor="w", pady=(5, 0))
            ctk.CTkLabel(content_frame, text=f"Location: {event['location']}",
                         font=ctk.CTkFont(family="Roboto", size=14)).pack(anchor="w", pady=(5, 0))
            ctk.CTkLabel(content_frame, text=event["description"], font=ctk.CTkFont(family="Roboto", size=14),
                         wraplength=500, justify="left").pack(anchor="w", pady=(5, 0))

            buttons_frame = ctk.CTkFrame(card, fg_color="white", width=150)
            buttons_frame.pack_propagate(False) 
            buttons_frame.pack(side="right", padx=10, pady=10)
            
           
            buttons_frame.grid_columnconfigure(0, weight=1)  
            buttons_frame.grid_rowconfigure((0, 1, 2), weight=1)  

            # Price Label
            # Format price display
            price_text = "Free" if event["price"] == "0€" else event["price"]
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
                command=lambda eid=event["event_id"]: self.dashboard.show_event_details(eid)
            )
            details_btn.grid(row=2, column=0, pady=(0,10))

    def matches_search(self, event, search_text):
        return search_text in event["title"].lower() or search_text in event["description"].lower()

    def matches_category(self, event, category):
        return category == "All Categories"  # Δεν υπάρχει ανάγκη να εξετάσουμε tags

    def matches_city(self, event, city):
        return city == "All Cities" or city.lower() in event["location"].lower()

    def matches_price(self, event, price_range):
        try:
            price = int(event["price"].replace("€", "").strip())
        except ValueError:
            return False
        if price_range == "All Prices":
            return True
        if price_range == "0-25€":
            return price <= 25
        if price_range == "26-50€":
            return 26 <= price <= 50
        if price_range == "51-100€":
            return 51 <= price <= 100
        if price_range == "100€+":
            return price > 100
        return True

    def matches_date(self, event, date_option):
        current_date = datetime.now()

        if date_option == "Any Date":
            return True
        if date_option == "Today":
            return current_date.date() == datetime.strptime(event["date"], "%Y-%m-%d %H:%M").date()
        if date_option == "This Week":
            start_of_week = current_date - timedelta(days=current_date.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            event_date = datetime.strptime(event["date"], "%Y-%m-%d %H:%M")
            return start_of_week <= event_date <= end_of_week
        if date_option == "This Month":
            start_of_month = current_date.replace(day=1)
            next_month = current_date.replace(month=current_date.month + 1, day=1)
            end_of_month = next_month - timedelta(days=1)
            event_date = datetime.strptime(event["date"], "%Y-%m-%d %H:%M")
            return start_of_month <= event_date <= end_of_month
        if date_option == "Next Month":
            next_month = current_date.replace(month=current_date.month + 1, day=1)
            start_of_next_month = next_month
            next_next_month = next_month.replace(month=next_month.month + 1, day=1)
            end_of_next_month = next_next_month - timedelta(days=1)
            event_date = datetime.strptime(event["date"], "%Y-%m-%d %H:%M")
            return start_of_next_month <= event_date <= end_of_next_month
        return False

    def sort_events(self, events, sort_option):
        if sort_option == "Date ↑":
            return sorted(events, key=lambda e: datetime.strptime(e["date"], "%Y-%m-%d %H:%M"))
        if sort_option == "Date ↓":
            return sorted(events, key=lambda e: datetime.strptime(e["date"], "%Y-%m-%d %H:%M"), reverse=True)
        if sort_option == "Price ↑":
            return sorted(events, key=lambda e: int(e["price"].replace("€", "").strip()))
        if sort_option == "Price ↓":
            return sorted(events, key=lambda e: int(e["price"].replace("€", "").strip()), reverse=True)
        return events  # Επιστροφή της λίστας χωρίς αλλαγές εάν η ταξινόμηση είναι κατά "Popularity"
