import customtkinter as ctk

class EventDetailsPage(ctk.CTkFrame):
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
            command=self.dashboard.back_to_find_events
        )
        back_btn.pack(side="left")
        
        # Event Title
        title = ctk.CTkLabel(
            header_frame,
            text=event["title"],
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold")
        )
        title.pack(side="left", padx=20)
        
        # Main Content
        content_frame = ctk.CTkFrame(self, fg_color="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))
        
        # Description
        desc_label = ctk.CTkLabel(
            content_frame,
            text=event["description"],
            font=ctk.CTkFont(family="Roboto", size=14),
            justify="left",
            wraplength=600
        )
        desc_label.pack(anchor="w", pady=(0,20))
        
        # Separator
        separator = ctk.CTkFrame(content_frame, height=2, fg_color="#E5E5E5")
        separator.pack(fill="x", pady=20)
        
        # Event Details
        details = [
            ("📅 Date", event["date"]),
            ("📍 Location", event["location"]),
            ("👥 Status", "Joinable"),
            ("🌐 Visibility", "Public"),
            ("👥 Participants", "180/250"),
            ("💶 Cost", "80€"),
            ("👤 Organizer", "Tech Community Athens")
        ]
        
        for label, value in details:
            detail_frame = ctk.CTkFrame(content_frame, fg_color="white")
            detail_frame.pack(fill="x", pady=5)
            
            label = ctk.CTkLabel(
                detail_frame,
                text=f"{label}:",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold")
            )
            label.pack(side="left")
            
            value = ctk.CTkLabel(
                detail_frame,
                text=value,
                font=ctk.CTkFont(family="Roboto", size=14)
            )
            value.pack(side="left", padx=(10,0))
        
        # Separator before buttons
        separator2 = ctk.CTkFrame(content_frame, height=2, fg_color="#E5E5E5")
        separator2.pack(fill="x", pady=20)
        
        # Buttons Frame
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="white")
        buttons_frame.pack(pady=20)
        
        # Invite Friends Button
        invite_btn = ctk.CTkButton(
            buttons_frame,
            text="Invite Friends  →",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            fg_color="#C8A165",
            hover_color="#b38e58",
            width=200,
            height=40,
            corner_radius=8,
            command=lambda: print("Inviting friends...")
        )
        invite_btn.pack(side="left", padx=10)
        
        # Join Event Button
        join_btn = ctk.CTkButton(
            buttons_frame,
            text="Join Event  →",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049",
            width=200,
            height=40,
            corner_radius=8,
            command=self.join_event
        )
        join_btn.pack(side="left", padx=10)
    
    def join_event(self):
        # Show confirmation dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Join Event")
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
            text=f"Are you sure you want to join\n{self.event['title']}?\n\nParticipation cost: 80€",
            font=ctk.CTkFont(family="Roboto", size=14),
            justify="center"
        )
        message.pack(expand=True, padx=20)
        
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
            text=f"You have successfully joined\n{self.event['title']}!",
            font=ctk.CTkFont(family="Roboto", size=16),
            justify="center"
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
            command=success.destroy
        )
        ok_btn.pack(pady=20)
