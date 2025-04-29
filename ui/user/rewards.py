import customtkinter as ctk
from datetime import datetime

class RewardsPage(ctk.CTkFrame):
    def __init__(self, master, available_points=750):  # Accept points parameter
        super().__init__(master, fg_color="white")
        self.available_points = available_points
        
        # Header
        self.header = ctk.CTkLabel(self, text="Available Rewards", 
                                   font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)
        
        # Current Points Display
        self.points_frame = ctk.CTkFrame(self, fg_color="white")
        self.points_frame.pack(fill="x", padx=20, pady=(0,20))
        
        self.points_display = ctk.CTkLabel(
            self.points_frame,
            text=f"{self.available_points}",
            font=ctk.CTkFont(family="Roboto", size=48, weight="bold"),
            text_color="#C8A165"
        )
        self.points_display.pack(pady=(0,5))
        
        self.points_label = ctk.CTkLabel(
            self.points_frame,
            text="POINTS AVAILABLE",
            font=ctk.CTkFont(family="Roboto", size=14)
        )
        self.points_label.pack(pady=(0,20))
        
        # Separator
        self.separator = ctk.CTkFrame(self, height=2, fg_color="#E5E5E5")
        self.separator.pack(fill="x", padx=20, pady=20)
        
        # Rewards Section
        self.rewards_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        self.rewards_frame.pack(fill="both", expand=True, padx=20, pady=(10,20))
        
        # Mock Rewards Data
        self.mock_rewards = [
            {
                "title": "Free Event Ticket",
                "points_required": 500,
                "description": "Get a free ticket to any upcoming event of your choice."
            },
            {
                "title": "VIP Access Pass",
                "points_required": 1000,
                "description": "Upgrade your next event experience with VIP access."
            },
            {
                "title": "Premium Membership",
                "points_required": 2000,
                "description": "Get premium membership benefits for 3 months."
            },
            {
                "title": "Event Organization Workshop",
                "points_required": 1500,
                "description": "Join an exclusive workshop on event organization."
            },
            {
                "title": "Networking Event Access",
                "points_required": 800,
                "description": "Get access to an exclusive networking event."
            }
        ]
        
        # Display Rewards
        self.display_rewards()
        
        # Back to Points button
        self.back_btn = ctk.CTkButton(
            self,
            text="← Back to Points",
            command=lambda: master.master.back_to_points(),
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            fg_color="#C8A165",
            hover_color="#b38e58",
            width=150,
            height=35,
            corner_radius=8,
        )
        self.back_btn.pack(pady=20)
    
    def display_rewards(self):
        for reward in self.mock_rewards:
            # Reward Card
            card = ctk.CTkFrame(self.rewards_frame, fg_color="white",
                               border_width=1, border_color="#C8A165")
            card.pack(fill="x", padx=5, pady=5)
            
            # Content Frame (left side)
            content = ctk.CTkFrame(card, fg_color="white")
            content.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            
            # Reward Title
            title = ctk.CTkLabel(
                content,
                text=reward["title"],
                font=ctk.CTkFont(family="Roboto", size=16, weight="bold")
            )
            title.pack(anchor="w")
            
            # Points Required
            points = ctk.CTkLabel(
                content,
                text=f"{reward['points_required']} pts required",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="#C8A165"
            )
            points.pack(anchor="w", pady=(5,0))
            
            # Description
            desc = ctk.CTkLabel(
                content,
                text=reward["description"],
                font=ctk.CTkFont(family="Roboto", size=14)
            )
            desc.pack(anchor="w", pady=(5,0))
            
            # Redeem Button (right side)
            can_redeem = self.available_points >= reward["points_required"]
            redeem_btn = ctk.CTkButton(
                card,
                text="Redeem  →",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                fg_color="#C8A165" if can_redeem else "#A0A0A0",
                hover_color="#b38e58" if can_redeem else "#A0A0A0",
                width=120,
                height=35,
                corner_radius=8,
                state="normal" if can_redeem else "disabled",
                command=lambda r=reward: self.redeem_reward(r)
            )
            redeem_btn.pack(side="right", padx=10)
    
    def redeem_reward(self, reward):
        # Show confirmation dialog
        dialog = ctk.CTkDialog(
            master=self,
            title="Confirm Redemption",
            text=f"Are you sure you want to redeem {reward['title']} for {reward['points_required']} points?",
            corner_radius=10
        )
        if dialog.get_input() == "OK":  # User confirmed
            # Update points
            self.available_points -= reward['points_required']
            self.points_display.configure(text=str(self.available_points))
            
            # Show success message
            success_dialog = ctk.CTkDialog(
                master=self,
                title="Success!",
                text=f"Points were redeemed successfully! Your new balance is {self.available_points} points.",
                corner_radius=10
            )
            success_dialog.get_button("OK").configure(
                fg_color="#4CAF50",
                hover_color="#45a049",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold")
            )
    
    def go_back(self):
      
        print("Going back to Points page...")
