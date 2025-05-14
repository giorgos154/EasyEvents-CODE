import customtkinter as ctk
from datetime import datetime
from src.auth import Auth
from src.classes.points.points import Points


class PointsPage(ctk.CTkFrame):
    def __init__(self, master, dashboard):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard
        self.current_user = Auth.get_current_user()

        # Header
        self.header = ctk.CTkLabel(self, text="Points Overview",
                                  font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)

        # Points Overview Section
        self.points_frame = ctk.CTkFrame(self, fg_color="white")
        self.points_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Initialize data
        self.points_history = Points.get_points_history(self.current_user.user_id)
        self.total_points = Points.get_user_points(self.current_user.user_id)

        # Points Display
        self.points_button = ctk.CTkButton(
            self.points_frame,
            text=str(self.total_points),
            font=ctk.CTkFont(family="Roboto", size=48, weight="bold"),
            text_color="#C8A165",
            fg_color="transparent",
            hover_color="#F0F0F0",
            command=self.show_points_popup
        )
        self.points_button.pack(pady=(0, 5))

        self.points_label = ctk.CTkLabel(
            self.points_frame,
            text="POINTS AVAILABLE",
            font=ctk.CTkFont(family="Roboto", size=14)
        )
        self.points_label.pack(pady=(0, 20))

        # Redeem Points Button
        self.redeem_btn = ctk.CTkButton(
            self.points_frame,
            text="Redeem Points →",
            command=lambda: self.dashboard.show_rewards(),
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

        # Points History Section
        self.history_label = ctk.CTkLabel(
            self,
            text="Points History",
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold")
        )
        self.history_label.pack(padx=20, anchor="w")

        # Scrollable Frame
        self.history_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        self.history_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Display Points History
        self.display_points_history()

    def display_points_history(self):
        for transaction in self.points_history:
            card = ctk.CTkFrame(self.history_frame, fg_color="white",
                               border_width=1, border_color="#E5E5E5")
            card.pack(fill="x", padx=5, pady=5)

            # Event label
            source_label = ctk.CTkLabel(
                card,
                text=transaction["event_name"],
                font=ctk.CTkFont(family="Roboto", size=16, weight="bold")
            )
            source_label.pack(anchor="w", padx=10, pady=(10, 0))

            # Reason and points
            reason_label = ctk.CTkLabel(
                card,
                text=f"✓ {transaction['reason']} ({transaction['points_change']} pts)",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="#4CAF50" if transaction["points_change"] > 0 else "#F44336"
            )
            reason_label.pack(anchor="w", padx=10, pady=(5, 0))

            # Date
            date_label = ctk.CTkLabel(
                card,
                text=f"📅 {transaction['transaction_date'].strftime('%Y-%m-%d %H:%M')}",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="gray"
            )
            date_label.pack(anchor="w", padx=10, pady=(5, 10))

    def show_points_popup(self):
        dialog = ctk.CTkDialog(
            master=self,
            title="Points Summary",
            text=f"You have accumulated {self.total_points} points!\n\n"
                 f"Positive points come from event participation and achievements.\n"
                 f"Negative points may result from cancellations or penalties.",
            corner_radius=10,
            title_color="#C8A165",
        )
        dialog.get_button("OK").configure(
            fg_color="#C8A165",
            hover_color="#b38e58",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold")
        )
