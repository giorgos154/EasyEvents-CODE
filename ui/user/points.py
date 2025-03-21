import customtkinter as ctk
from datetime import datetime

class PointsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        
        # Header
        self.header = ctk.CTkLabel(self, text="Points Overview", 
                                   font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)
        
        # Points Overview Section
        self.points_frame = ctk.CTkFrame(self, fg_color="white")
        self.points_frame.pack(fill="x", padx=20, pady=(0,20))
        
        # Current Points Display (clickable)
        self.points_button = ctk.CTkButton(
            self.points_frame,
            text="750",
            font=ctk.CTkFont(family="Roboto", size=48, weight="bold"),
            text_color="#C8A165",
            fg_color="transparent",
            hover_color="#F0F0F0",
            command=self.show_points_popup
        )
        self.points_button.pack(pady=(0,5))
        
        self.points_label = ctk.CTkLabel(
            self.points_frame,
            text="POINTS AVAILABLE",
            font=ctk.CTkFont(family="Roboto", size=14)
        )
        self.points_label.pack(pady=(0,20))
        
        # Redeem Points Button
        self.redeem_btn = ctk.CTkButton(
            self.points_frame,
            text="Redeem Points  →",
            command=lambda: master.master.show_rewards(),
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049",
            width=200,
            height=40,
            corner_radius=8
        )
        self.redeem_btn.pack(pady=10)
        
        # Separator
        self.separator = ctk.CTkFrame(self, height=2, fg_color="#E5E5E5")
        self.separator.pack(fill="x", padx=20, pady=20)
        
        # Activities History Section
        self.activities_label = ctk.CTkLabel(
            self,
            text="Recent Activities",
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold")
        )
        self.activities_label.pack(padx=20, anchor="w")
        
        # Scrollable Activities List
        self.activities_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        self.activities_frame.pack(fill="both", expand=True, padx=20, pady=(10,20))
        
        # Mock Activities Data
        self.mock_activities = [
            {
                "event": "Tech Conference 2025",
                "type": "Event Participation",
                "points": 100,
                "date": "2025-04-15"
            },
            {
                "event": "Summer Music Festival",
                "type": "Event Review",
                "points": 50,
                "date": "2025-06-20"
            },
            {
                "event": "Art & Culture Expo",
                "type": "Event Check-in",
                "points": 75,
                "date": "2025-05-10"
            }
        ]
        
        # Display Activities
        self.display_activities()
    
    def display_activities(self):
        for activity in self.mock_activities:
            # Activity Card
            card = ctk.CTkFrame(self.activities_frame, fg_color="white", 
                               border_width=1, border_color="#E5E5E5")
            card.pack(fill="x", padx=5, pady=5)
            
            # Event Name
            event_label = ctk.CTkLabel(
                card,
                text=activity["event"],
                font=ctk.CTkFont(family="Roboto", size=16, weight="bold")
            )
            event_label.pack(anchor="w", padx=10, pady=(10,0))
            
            # Activity Type and Points
            type_points = ctk.CTkLabel(
                card,
                text=f"✓ {activity['type']} (+{activity['points']} pts)",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="#4CAF50"
            )
            type_points.pack(anchor="w", padx=10, pady=(5,0))
            
            # Date
            date_label = ctk.CTkLabel(
                card,
                text=f"📅 {activity['date']}",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="gray"
            )
            date_label.pack(anchor="w", padx=10, pady=(5,10))
    
    def show_points_popup(self):
        total_points = sum(activity["points"] for activity in self.mock_activities)
        dialog = ctk.CTkDialog(
            master=self,
            title="Congratulations!",
            text=f"You have collected {total_points} points for completing activities!",
            corner_radius=10,
            title_color="#C8A165",
        )
        dialog.get_button("OK").configure(
            fg_color="#C8A165",
            hover_color="#b38e58",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold")
        )
