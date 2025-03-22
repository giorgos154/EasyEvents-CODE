import customtkinter as ctk

class InviteFriendsPage(ctk.CTkFrame):
    def __init__(self, master, dashboard, event):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard
        self.event = event
        
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
            command=lambda: self.dashboard.back_to_find_events()
        )
        back_btn.pack(side="left")
        
        # Event Title
        title = ctk.CTkLabel(
            header_frame,
            text=f"Invite Friends to {event['title']}",
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold")
        )
        title.pack(side="left", padx=20)
        
        # Main content frame
        content_frame = ctk.CTkFrame(self, fg_color="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))
        
        # Mock friends data
        self.mock_friends = [
            {
                "name": "Maria Papadopoulos",
                "username": "@maria_p",
                "avatar": "🧑"
            },
            {
                "name": "Nikos Georgiou",
                "username": "@nikos_g",
                "avatar": "👤"
            },
            {
                "name": "Elena Dimitriou",
                "username": "@elena_d",
                "avatar": "👩"
            },
            {
                "name": "Alexandros Ioannou",
                "username": "@alex_i",
                "avatar": "👤"
            },
            {
                "name": "Sofia Antoniou",
                "username": "@sofia_a",
                "avatar": "👩"
            }
        ]
        
        # Friends list section
        list_label = ctk.CTkLabel(
            content_frame,
            text="Select Friends to Invite:",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold")
        )
        list_label.pack(anchor="w", pady=(0,10))
        
        # Friends list frame with scroll
        self.friends_frame = ctk.CTkScrollableFrame(content_frame, fg_color="white")
        self.friends_frame.pack(fill="both", expand=True)
        
        # Checkboxes for friends
        self.selected_friends = {}
        for friend in self.mock_friends:
            friend_frame = ctk.CTkFrame(self.friends_frame, fg_color="white")
            friend_frame.pack(fill="x", pady=5)
            
            # Checkbox
            var = ctk.BooleanVar()
            self.selected_friends[friend["username"]] = var
            checkbox = ctk.CTkCheckBox(
                friend_frame,
                text="",
                variable=var,
                width=20,
                fg_color="#C8A165",
                hover_color="#b38e58"
            )
            checkbox.pack(side="left", padx=(5,10))
            
            # Avatar
            avatar = ctk.CTkLabel(
                friend_frame,
                text=friend["avatar"],
                font=ctk.CTkFont(size=20)
            )
            avatar.pack(side="left", padx=(0,10))
            
            # Name and username
            name = ctk.CTkLabel(
                friend_frame,
                text=friend["name"],
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold")
            )
            name.pack(side="left")
            
            username = ctk.CTkLabel(
                friend_frame,
                text=friend["username"],
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="gray"
            )
            username.pack(side="left", padx=5)
        
        # Personal message section
        message_label = ctk.CTkLabel(
            content_frame,
            text="Personal Message:",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold")
        )
        message_label.pack(anchor="w", pady=(20,10))
        
        self.message_box = ctk.CTkTextbox(
            content_frame,
            height=100,
            font=ctk.CTkFont(family="Roboto", size=14)
        )
        self.message_box.pack(fill="x")
        self.message_box.insert("1.0", f"Hey! Join me at {event['title']}!")
        
        # Send button
        send_btn = ctk.CTkButton(
            content_frame,
            text="Send Invites →",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049",
            width=200,
            height=40,
            corner_radius=8,
            command=self.send_invites
        )
        send_btn.pack(pady=20)
    
    def send_invites(self):
        # Get selected friends
        selected = [username for username, var in self.selected_friends.items() if var.get()]
        
        if not selected:
            self.show_error("Please select at least one friend to invite.")
            return
        
        # Show confirmation dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm Invites")
        dialog.geometry("400x200")
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
            text=f"Send invites to {len(selected)} friend{'s' if len(selected) > 1 else ''}?",
            font=ctk.CTkFont(family="Roboto", size=16)
        )
        message.pack(expand=True)
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        # Confirm button
        confirm_btn = ctk.CTkButton(
            btn_frame,
            text="Confirm",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            command=lambda: [dialog.destroy(), self.show_success()]
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
    
    def show_success(self):
        # Success dialog
        success = ctk.CTkToplevel(self)
        success.title("Success!")
        success.geometry("400x150")
        success.transient(self)
        success.grab_set()
        
        # Center dialog
        success.update_idletasks()
        x = (success.winfo_screenwidth() - success.winfo_width()) // 2
        y = (success.winfo_screenheight() - success.winfo_height()) // 2
        success.geometry(f"+{x}+{y}")
        
        # Success message
        message = ctk.CTkLabel(
            success,
            text="Invites have been sent successfully!",
            font=ctk.CTkFont(family="Roboto", size=16)
        )
        message.pack(expand=True)
        
        # OK button
        ok_btn = ctk.CTkButton(
            success,
            text="OK",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            command=lambda: [success.destroy(), self.dashboard.back_to_find_events()]
        )
        ok_btn.pack(pady=20)
    
    def show_error(self, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Error")
        dialog.geometry("400x150")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Error message
        ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(family="Roboto", size=16)
        ).pack(expand=True)
        
        # OK button
        ctk.CTkButton(
            dialog,
            text="OK",
            fg_color="#f44336",
            hover_color="#e53935",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            command=dialog.destroy
        ).pack(pady=20)
