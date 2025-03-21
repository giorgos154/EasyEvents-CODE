import customtkinter as ctk
from datetime import datetime

class EventDiscussionPage(ctk.CTkFrame):
    def __init__(self, master, event):
        super().__init__(master, fg_color="white")
        self.event = event
        
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="white")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        # Back button
        self.back_btn = ctk.CTkButton(
            header_frame,
            text="← Back",
            fg_color="#C8A165",
            hover_color="#b38e58",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            height=32,
            corner_radius=8,
            text_color="black"
        )
        self.back_btn.pack(side="left")
        
        # Event Title
        title = ctk.CTkLabel(
            header_frame,
            text=event["title"],
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold")
        )
        title.pack(side="left", padx=20)
        
        # Messages Area
        self.messages_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        self.messages_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))
        
        # Mock messages
        self.mock_messages = [
            {
                "user": "EventOrganizer",
                "timestamp": "2025-03-21 14:30",
                "message": "Welcome everyone to the discussion! Feel free to ask any questions about the event."
            },
            {
                "user": "JohnDoe",
                "timestamp": "2025-03-21 14:35",
                "message": "Looking forward to this! Will there be a networking session?"
            },
            {
                "user": "EventOrganizer",
                "timestamp": "2025-03-21 14:37",
                "message": "Yes! We have a dedicated networking hour planned after the main presentations."
            },
            {
                "user": "Alice123",
                "timestamp": "2025-03-21 14:40",
                "message": "Great to hear that! Can't wait to meet everyone."
            },
            {
                "user": "TechEnthusiast",
                "timestamp": "2025-03-21 14:45",
                "message": "Will the presentations be recorded for later viewing?"
            }
        ]
        
        # Display messages
        self.display_messages()
        # Input Area
        input_frame = ctk.CTkFrame(self, fg_color="white", height=100)
        input_frame.pack(fill="x", padx=20, pady=(0,20))
        input_frame.pack_propagate(False)
        
        self.message_input = ctk.CTkTextbox(
            input_frame,
            font=ctk.CTkFont(family="Roboto", size=14),
            height=60,
            corner_radius=8,
            border_width=1,
            border_color="black"
        )
        self.message_input.pack(side="left", fill="both", expand=True, padx=(0,10))
        
        send_btn = ctk.CTkButton(
            input_frame,
            text="Send →",
            fg_color="#C8A165",
            hover_color="#b38e58",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            height=35,
            corner_radius=8,
            text_color="black",
            command=self.send_message
        )
        send_btn.pack(side="right", pady=12.5)
        
    def display_messages(self):
        # Clear existing messages
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        
        # Display messages
        for message in self.mock_messages:
            # Message container
            msg_frame = ctk.CTkFrame(self.messages_frame, fg_color="white")
            msg_frame.pack(fill="x", pady=5)
            
            # User and timestamp
            header_frame = ctk.CTkFrame(msg_frame, fg_color="white")
            header_frame.pack(fill="x")
            
            user_label = ctk.CTkLabel(
                header_frame,
                text=message["user"],
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                text_color="#C8A165" if message["user"] == "EventOrganizer" else "black"
            )
            user_label.pack(side="left")
            
            time_label = ctk.CTkLabel(
                header_frame,
                text=message["timestamp"],
                font=ctk.CTkFont(family="Roboto", size=12),
                text_color="gray"
            )
            time_label.pack(side="left", padx=10)
            
            # Message text
            msg_label = ctk.CTkLabel(
                msg_frame,
                text=message["message"],
                font=ctk.CTkFont(family="Roboto", size=14),
                wraplength=600,
                justify="left"
            )
            msg_label.pack(anchor="w", pady=(5,10))
            
            # Separator
            separator = ctk.CTkFrame(msg_frame, height=1, fg_color="#E5E5E5")
            separator.pack(fill="x", pady=(0,5))
    
    def send_message(self):
        message = self.message_input.get("1.0", "end-1c").strip()
        if not message:
            return
        
        # Add new message
        self.mock_messages.append({
            "user": "CurrentUser",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "message": message
        })
        
        # Clear input
        self.message_input.delete("1.0", "end")
        
        # Refresh display
        self.display_messages()
        
        # Scroll to bottom
        self.messages_frame._parent_canvas.yview_moveto(1.0)
