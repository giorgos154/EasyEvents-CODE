import customtkinter as ctk
from src.db_connection import get_db_connection
from src.auth import Auth

class RateEventsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")

        current_user = Auth.get_current_user()
        self.user_id = current_user.user_id if current_user else None
        if not self.user_id:
            self.show_error("User not logged in.")
            return

        self.header = ctk.CTkLabel(self, text="Rate Events",
                                   font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)

        self.events_label = ctk.CTkLabel(
            self,
            text="Available Events to Rate",
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold")
        )
        self.events_label.pack(padx=20, anchor="w")

        self.events_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        self.events_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.load_events()

    def load_events(self):
        conn = get_db_connection()
        if not conn:
            return
        try:
            with conn.cursor() as cursor:
                query = """
                SELECT e.event_id, e.title, e.event_date, e.venue
                FROM events e
                JOIN event_participations ep ON e.event_id = ep.event_id
                WHERE ep.user_id = %s
                AND NOT EXISTS (
                    SELECT 1 FROM ratings r
                    WHERE r.event_id = e.event_id AND r.user_id = %s
                )
                ORDER BY e.event_date DESC;
                """
                cursor.execute(query, (self.user_id, self.user_id))
                self.events = cursor.fetchall()
        finally:
            conn.close()

        self.display_events()

    def display_events(self):
        for widget in self.events_frame.winfo_children():
            widget.destroy()

        for event in self.events:
            card = ctk.CTkFrame(self.events_frame, fg_color="white",
                                border_width=1, border_color="#E5E5E5")
            card.pack(fill="x", padx=5, pady=5)

            content = ctk.CTkFrame(card, fg_color="white")
            content.pack(side="left", fill="both", expand=True, padx=10, pady=10)

            title = ctk.CTkLabel(
                content,
                text=event["title"],
                font=ctk.CTkFont(family="Roboto", size=16, weight="bold")
            )
            title.pack(anchor="w")

            date = ctk.CTkLabel(
                content,
                text=f"📅 {event['event_date']}",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="gray"
            )
            date.pack(anchor="w", pady=(5, 0))

            location = ctk.CTkLabel(
                content,
                text=f"📍 {event['venue']}",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="gray"
            )
            location.pack(anchor="w", pady=(5, 0))

            rate_btn = ctk.CTkButton(
                card,
                text="Rate & Review",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                fg_color="#C8A165",
                hover_color="#b38e58",
                width=120,
                height=35,
                corner_radius=8,
                command=lambda e=event: self.show_rating_dialog(e)
            )
            rate_btn.pack(side="right", padx=10)

    def show_rating_dialog(self, event):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Rate Event")
        dialog.geometry("400x400")
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text=f"Rate {event['title']}",
                     font=ctk.CTkFont(family="Roboto", size=20, weight="bold"))\
            .pack(pady=20, padx=20)

        self.rating_event = ctk.CTkEntry(dialog, placeholder_text="Event Rating (1-5)")
        self.rating_event.pack(pady=10, padx=20)

        self.rating_org = ctk.CTkEntry(dialog, placeholder_text="Organizer Rating (1-5)")
        self.rating_org.pack(pady=10, padx=20)

        self.comment = ctk.CTkTextbox(dialog, height=100)
        self.comment.pack(pady=10, padx=20)

        ctk.CTkButton(dialog, text="Submit",
                      command=lambda: self.submit_review(event["event_id"], dialog))\
            .pack(pady=20)

    def submit_review(self, event_id, dialog):
        conn = get_db_connection()
        if not conn:
            return

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ratings (event_id, user_id, organizer_rating, event_rating, comment)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    event_id,
                    self.user_id,
                    int(self.rating_org.get()),
                    int(self.rating_event.get()),
                    self.comment.get("1.0", "end").strip()
                ))
                conn.commit()
        finally:
            conn.close()

        dialog.destroy()
        self.load_events()

    def show_error(self, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Error")
        dialog.geometry("400x150")
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(family="Roboto", size=16)
        ).pack(expand=True)

        ctk.CTkButton(
            dialog,
            text="OK",
            fg_color="#f44336",
            hover_color="#e53935",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            command=dialog.destroy
        ).pack(pady=20)
