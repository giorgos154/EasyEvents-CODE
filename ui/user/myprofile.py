import customtkinter as ctk

class MyProfilePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        # Header
        self.header = ctk.CTkLabel(self, text="My Profile", 
                                   font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)
        
        # Main container with two columns
        self.main_frame = ctk.CTkFrame(self, fg_color="white")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left column: profile info
        self.left_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0,20))
        
        # Right column: action buttons
        self.right_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        
        # Column weights (60% - 40%)
        self.main_frame.grid_columnconfigure(0, weight=3)
        self.main_frame.grid_columnconfigure(1, weight=2)
        
        # Profile fields
        self.personal_frame = ctk.CTkFrame(self.left_frame, fg_color="white")
        self.personal_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        
        # Mock profile data
        self.mock_profile = {
            "Username": "johndoe",
            "First Name": "John",
            "Last Name": "Doe",
            "Email Address": "john@example.com",
            "Phone Number": "+30 123 456 7890",
            "Address": "123 Main Street",
            "City": "Athens",
            "Postcode": "12345"
        }
        
        # Create and populate fields
        self.entries = {}
        for i, (field, value) in enumerate(self.mock_profile.items()):
            label = ctk.CTkLabel(
                self.personal_frame,
                text=field,
                font=ctk.CTkFont(family="Roboto", size=16)
            )
            label.grid(row=i, column=0, sticky="w", pady=10)
            
            entry = ctk.CTkEntry(
                self.personal_frame,
                width=250,
                font=ctk.CTkFont(family="Roboto", size=14)
            )
            entry.insert(0, value)
            entry.configure(state="disabled")
            entry.grid(row=i, column=1, pady=10, padx=(10,0))
            self.entries[field] = entry
        
        # Buttons container
        self.button_container = ctk.CTkFrame(self.right_frame, fg_color="white")
        self.button_container.pack(expand=True)
        
        # Edit button
        self.edit_btn = ctk.CTkButton(
            self.button_container,
            text="Edit Profile  →",
            fg_color="#C8A165",
            hover_color="#b38e58",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=300,
            height=40,
            corner_radius=8,
            text_color="black",
            command=self.enable_editing
        )
        self.edit_btn.pack(pady=(0,10))
        
        # View Past Events button
        self.view_events_btn = ctk.CTkButton(
            self.button_container,
            text="View Past Events  →",
            fg_color="#C8A165",
            hover_color="#b38e58",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=300,
            height=40,
            corner_radius=8,
            text_color="black",
            command=self.show_past_events
        )
        self.view_events_btn.pack(pady=10)
        
        # Save and Cancel buttons (hidden by default)
        self.save_btn = ctk.CTkButton(
            self.button_container,
            text="Save Changes  →",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=300,
            height=40,
            corner_radius=8,
            text_color="black",
            command=self.save_changes
        )
        
        self.cancel_btn = ctk.CTkButton(
            self.button_container,
            text="Cancel  →",
            fg_color="#f44336",
            hover_color="#e53935",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=300,
            height=40,
            corner_radius=8,
            text_color="black",
            command=self.disable_editing
        )
        
        self.edit_mode = False
        
    def enable_editing(self):
        """Enable editing of profile fields"""
        for entry in self.entries.values():
            entry.configure(state="normal")
        
        self.edit_btn.pack_forget()
        self.view_events_btn.pack_forget()
        self.save_btn.pack(pady=(0,10))
        self.cancel_btn.pack(pady=10)
        self.edit_mode = True
        
    def disable_editing(self):
        """Disable editing of profile fields"""
        for entry in self.entries.values():
            entry.configure(state="disabled")
        
        self.save_btn.pack_forget()
        self.cancel_btn.pack_forget()
        self.edit_btn.pack(pady=(0,10))
        self.view_events_btn.pack(pady=10)
        self.edit_mode = False
    
    def save_changes(self):
        """Save profile changes"""
        # Update mock data
        for field, entry in self.entries.items():
            self.mock_profile[field] = entry.get()
        
        # Show success message
        dialog = ctk.CTkDialog(
            master=self,
            title="Success!",
            text="Your profile has been updated successfully.",
            corner_radius=10
        )
        dialog.get_button("OK").configure(
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold")
        )
        
        self.disable_editing()
    
    def show_past_events(self):
        """Show past events dialog"""
        # Create dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Past Events I've Attended")
        dialog.geometry("500x600")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog on screen
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Dialog header
        header = ctk.CTkLabel(
            dialog,
            text="Past Events",
            font=ctk.CTkFont(family="Roboto", size=20, weight="bold")
        )
        header.pack(pady=20, padx=20)
        
        # Scrollable frame for events
        events_frame = ctk.CTkScrollableFrame(dialog, fg_color="white")
        events_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))
        
        # Mock past events
        past_events = [
            {
                "title": "Tech Conference 2024",
                "date": "March 15, 2024",
                "location": "Athens Convention Center"
            },
            {
                "title": "Summer Music Festival",
                "date": "February 20, 2024",
                "location": "Thessaloniki Park"
            },
            {
                "title": "Art Exhibition",
                "date": "January 10, 2024",
                "location": "National Gallery"
            },
            {
                "title": "Networking Event",
                "date": "December 5, 2023",
                "location": "Business Center"
            }
        ]
        
        # Display events
        for event in past_events:
            card = ctk.CTkFrame(events_frame, fg_color="white", 
                               border_width=1, border_color="#E5E5E5")
            card.pack(fill="x", padx=5, pady=5)
            
            # Title
            title = ctk.CTkLabel(
                card,
                text=event["title"],
                font=ctk.CTkFont(family="Roboto", size=16, weight="bold")
            )
            title.pack(anchor="w", padx=10, pady=(10,5))
            
            # Date
            date = ctk.CTkLabel(
                card,
                text=f"📅 {event['date']}",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="gray"
            )
            date.pack(anchor="w", padx=10, pady=2)
            
            # Location
            location = ctk.CTkLabel(
                card,
                text=f"📍 {event['location']}",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="gray"
            )
            location.pack(anchor="w", padx=10, pady=(2,10))
