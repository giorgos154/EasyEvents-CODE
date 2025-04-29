import customtkinter as ctk

class MyInvitesPage(ctk.CTkFrame):
    def __init__(self, master, dashboard):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard
        
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="white")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        # Back button
        back_btn = ctk.CTkButton(
            header_frame,
            text="← Back",
            fg_color="#C8A165",
            hover_color="#b38e58",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            height=32,
            corner_radius=8,
            text_color="black",
            command=lambda: self.dashboard.show_page("My Profile")
        )
        back_btn.pack(side="left")
        
        # Title
        title = ctk.CTkLabel(
            header_frame,
            text="Pending Invites",
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold")
        )
        title.pack(side="left", padx=20)
        
        # Mock invites data
        self.mock_invites = [
            {
                "event_title": "Tech Conference 2025",
                "event_date": "2025-04-15",
                "event_location": "Athens Convention Center",
                "event_description": "Annual tech conference featuring industry leaders.",
                "from_name": "Maria P.",
                "from_username": "@maria_p",
                "from_avatar": "🧑",
                "message": "Hey! Would love to have you join me at this tech conference! It's going to be amazing!"
            },
            {
                "event_title": "Summer Music Festival",
                "event_date": "2025-06-20",
                "event_location": "Thessaloniki Park",
                "event_description": "A weekend of live music performances.",
                "from_name": "Nikos G.",
                "from_username": "@nikos_g",
                "from_avatar": "👤",
                "message": "Let's enjoy some great music together! Don't miss this festival!"
            }
        ]
        
        # Scrollable frame for invites
        self.invites_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        self.invites_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))
        
        # Display invites
        self.display_invites()
    
    def display_invites(self):
        for invite in self.mock_invites:
            # Invite Card
            card = ctk.CTkFrame(self.invites_frame, fg_color="white", 
                               border_width=1, border_color="#E5E5E5")
            card.pack(fill="x", padx=10, pady=10)
            
            # Event Info Frame
            event_frame = ctk.CTkFrame(card, fg_color="white")
            event_frame.pack(fill="x", padx=15, pady=(15,5))
            
            # Event Title
            event_title = ctk.CTkLabel(
                event_frame,
                text=invite["event_title"],
                font=ctk.CTkFont(family="Roboto", size=18, weight="bold")
            )
            event_title.pack(anchor="w")
            
            # Event Details
            event_date = ctk.CTkLabel(
                event_frame,
                text=f"📅 Date: {invite['event_date']}",
                font=ctk.CTkFont(family="Roboto", size=14)
            )
            event_date.pack(anchor="w", pady=(5,0))
            
            event_location = ctk.CTkLabel(
                event_frame,
                text=f"📍 Location: {invite['event_location']}",
                font=ctk.CTkFont(family="Roboto", size=14)
            )
            event_location.pack(anchor="w", pady=(5,0))
            
            # Separator
            separator = ctk.CTkFrame(card, height=1, fg_color="#E5E5E5")
            separator.pack(fill="x", padx=15, pady=10)
            
            # From Frame
            from_frame = ctk.CTkFrame(card, fg_color="white")
            from_frame.pack(fill="x", padx=15, pady=5)
            
            # From info with avatar
            from_info = ctk.CTkFrame(from_frame, fg_color="white")
            from_info.pack(anchor="w")
            
            avatar = ctk.CTkLabel(
                from_info,
                text=invite["from_avatar"],
                font=ctk.CTkFont(size=20)
            )
            avatar.pack(side="left", padx=(0,5))
            
            name = ctk.CTkLabel(
                from_info,
                text=invite["from_name"],
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold")
            )
            name.pack(side="left")
            
            username = ctk.CTkLabel(
                from_info,
                text=invite["from_username"],
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="gray"
            )
            username.pack(side="left", padx=5)
            
            # Message
            message = ctk.CTkLabel(
                card,
                text=invite["message"],
                font=ctk.CTkFont(family="Roboto", size=14),
                wraplength=600,
                justify="left"
            )
            message.pack(anchor="w", padx=15, pady=(5,15))
            
            # Buttons Frame
            buttons_frame = ctk.CTkFrame(card, fg_color="white")
            buttons_frame.pack(fill="x", padx=15, pady=(0,15))
            
            # Accept button
            accept_btn = ctk.CTkButton(
                buttons_frame,
                text="Accept  ✓",
                fg_color="#4CAF50",
                hover_color="#45a049",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                width=150,
                height=35,
                corner_radius=8,
                command=lambda i=invite: self.accept_invite(i)
            )
            accept_btn.pack(side="left", padx=(0,10))
            
            # Reject button
            reject_btn = ctk.CTkButton(
                buttons_frame,
                text="Reject  ×",
                fg_color="#f44336",
                hover_color="#e53935",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                width=150,
                height=35,
                corner_radius=8,
                command=lambda i=invite: self.reject_invite(i)
            )
            reject_btn.pack(side="left")
    
    def accept_invite(self, invite):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Success!")
        dialog.geometry("400x150")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Success message
        message = ctk.CTkLabel(
            dialog,
            text=f"You have joined {invite['event_title']}!",
            font=ctk.CTkFont(family="Roboto", size=16)
        )
        message.pack(expand=True)
        
        # OK button
        ok_btn = ctk.CTkButton(
            dialog,
            text="OK",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            command=lambda: [dialog.destroy(), self.dashboard.show_page("My Events")]
        )
        ok_btn.pack(pady=20)
    
    def reject_invite(self, invite):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm Reject")
        dialog.geometry("400x150")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Confirmation message
        message = ctk.CTkLabel(
            dialog,
            text=f"Are you sure you want to reject\nthe invitation to {invite['event_title']}?",
            font=ctk.CTkFont(family="Roboto", size=14)
        )
        message.pack(expand=True)
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        # Confirm button
        confirm_btn = ctk.CTkButton(
            btn_frame,
            text="Confirm",
            fg_color="#f44336",
            hover_color="#e53935",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            command=lambda: [dialog.destroy(), self.remove_invite()]
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
            command=dialog.destroy
        )
        cancel_btn.pack(side="left", padx=10)
    
    def remove_invite(self):
      
        for widget in self.invites_frame.winfo_children():
            widget.destroy()
        self.mock_invites.pop()
        self.display_invites()
