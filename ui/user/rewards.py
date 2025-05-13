import customtkinter as ctk
from datetime import datetime
import pymysql
from src.auth import Auth
from CTkMessagebox import CTkMessagebox


class RewardsPage(ctk.CTkFrame):
    def __init__(self, master, dashboard):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard
        self.current_user = Auth.get_current_user()
        self.available_points = self.get_user_points()
        self.redeemed_rewards = []

        # Header
        self.header = ctk.CTkLabel(self, text="Available Rewards",
                                   font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)

        # Points Display
        self.points_frame = ctk.CTkFrame(self, fg_color="white")
        self.points_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.points_display = ctk.CTkLabel(
            self.points_frame,
            text=f"{self.available_points}",
            font=ctk.CTkFont(family="Roboto", size=48, weight="bold"),
            text_color="#C8A165"
        )
        self.points_display.pack(pady=(0, 5))

        self.points_label = ctk.CTkLabel(
            self.points_frame,
            text="POINTS AVAILABLE",
            font=ctk.CTkFont(family="Roboto", size=14)
        )
        self.points_label.pack(pady=(0, 20))

        self.separator = ctk.CTkFrame(self, height=2, fg_color="#E5E5E5")
        self.separator.pack(fill="x", padx=20, pady=20)

        self.rewards_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        self.rewards_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        self.rewards = self.fetch_rewards()
        self.display_rewards()

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

    def get_user_points(self):
        try:
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="Denistheking123!",
                database="easyeventsdatabase",
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
            )
            with conn.cursor() as cursor:
                cursor.execute("SELECT COALESCE(SUM(points_change), 0) AS total FROM points WHERE user_id = %s",
                               (self.current_user.user_id,))
                result = cursor.fetchone()
                return result["total"] if result else 0
        except Exception as e:
            print("Error fetching user points:", e)
            return 0

    def fetch_rewards(self):
        try:
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="Denistheking123!",
                database="easyeventsdatabase",
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
            )
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM rewards")
                return cursor.fetchall()
        except Exception as e:
            print("Error fetching rewards:", e)
            return []

    def display_rewards(self):
        for reward in self.rewards:
            card = ctk.CTkFrame(self.rewards_frame, fg_color="white",
                                border_width=1, border_color="#C8A165")
            card.pack(fill="x", padx=5, pady=5)

            content = ctk.CTkFrame(card, fg_color="white")
            content.pack(side="left", fill="both", expand=True, padx=10, pady=10)

            title = ctk.CTkLabel(
                content,
                text=reward["name"],
                font=ctk.CTkFont(family="Roboto", size=16, weight="bold")
            )
            title.pack(anchor="w")

            points = ctk.CTkLabel(
                content,
                text=f"{reward['points_required']} pts required",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="#C8A165"
            )
            points.pack(anchor="w", pady=(5, 0))

            desc = ctk.CTkLabel(
                content,
                text=reward["description"],
                font=ctk.CTkFont(family="Roboto", size=14)
            )
            desc.pack(anchor="w", pady=(5, 0))

            redeem_btn = ctk.CTkButton(
                card,
                text="Redeem  →",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                fg_color="#C8A165",
                hover_color="#b38e58",
                width=120,
                height=35,
                corner_radius=8,
                state="normal",
                command=lambda r=reward: self.attempt_redeem(r)
            )
            redeem_btn.pack(side="right", padx=10)

    def attempt_redeem(self, reward):
        if self.available_points < reward["points_required"]:
            CTkMessagebox(title="Error", message="Not enough points to redeem this reward.", icon="cancel")
        else:
            self.show_confirm_dialog(reward)

    def show_confirm_dialog(self, reward):
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Confirm Redemption")
        confirm_window.geometry("400x200")
        confirm_window.grab_set()

        label = ctk.CTkLabel(confirm_window, text=f"Redeem '{reward['name']}' for {reward['points_required']} points?")
        label.pack(pady=20)

        btn_frame = ctk.CTkFrame(confirm_window)
        btn_frame.pack(pady=10)

        def confirm_action():
            confirm_window.destroy()
            self.perform_redemption(reward)

        ok_btn = ctk.CTkButton(btn_frame, text="OK", command=confirm_action, fg_color="#C8A165")
        ok_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=confirm_window.destroy)
        cancel_btn.pack(side="left", padx=10)

    def perform_redemption(self, reward):
        try:
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="Denistheking123!",
                database="easyeventsdatabase",
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
            )
            with conn.cursor() as cursor:
                insert_query = """
                INSERT INTO points (user_id, event_id, reason, points_change, transaction_date)
                VALUES (%s, NULL, %s, %s, NOW())
                """
                cursor.execute(insert_query, (
                    self.current_user.user_id,
                    f"Redeemed: {reward['name']}",
                    -reward['points_required']
                ))
                conn.commit()
        except Exception as e:
            print("Database insert error:", e)
            return

        self.available_points -= reward["points_required"]
        self.points_display.configure(text=str(self.available_points))

        success_window = ctk.CTkToplevel(self)
        success_window.title("Success")
        success_window.geometry("300x150")
        success_window.grab_set()

        label = ctk.CTkLabel(success_window, text="Redemption successful!")
        label.pack(pady=20)

        ok_btn = ctk.CTkButton(success_window, text="OK", command=lambda: [success_window.destroy(), self.refresh_rewards()])
        ok_btn.pack(pady=10)

    def refresh_rewards(self):
        for widget in self.rewards_frame.winfo_children():
            widget.destroy()
        self.available_points = self.get_user_points()
        self.points_display.configure(text=str(self.available_points))
        self.rewards = self.fetch_rewards()
        self.display_rewards()
