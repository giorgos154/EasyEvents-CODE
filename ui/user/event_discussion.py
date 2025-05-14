import customtkinter as ctk
from datetime import datetime
from src.db_connection import get_db_connection
from src.auth import Auth

class EventDiscussionPage(ctk.CTkFrame):
    def __init__(self, master, dashboard, event):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard
        self.event = event

        current_user = Auth.get_current_user()
        self.user_id = current_user.user_id if current_user else None
        if not self.user_id:
            self.show_error("User not logged in.")
            return

        self.build_ui()
        self.load_messages()

    def build_ui(self):
        
        header_frame = ctk.CTkFrame(self, fg_color="white")
        header_frame.pack(fill="x", padx=20, pady=20)

        self.back_btn = ctk.CTkButton(
            header_frame,
            text="← Back",
            command=self.dashboard.back_to_events,
            fg_color="#C8A165",
            hover_color="#b38e58",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            height=32,
            corner_radius=8,
            text_color="black"
        )
        self.back_btn.pack(side="left")

        title = ctk.CTkLabel(
            header_frame,
            text=self.event["title"],
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold")
        )
        title.pack(side="left", padx=20)


        self.messages_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        self.messages_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # εισαγωγή νέου μηνύματος
        input_frame = ctk.CTkFrame(self, fg_color="white", height=100)
        input_frame.pack(fill="x", padx=20, pady=(0, 20))
        input_frame.pack_propagate(False)

        self.message_input = ctk.CTkTextbox(
            input_frame,
            font=ctk.CTkFont(family="Roboto", size=14),
            height=60,
            corner_radius=8,
            border_width=1,
            border_color="black"
        )
        self.message_input.pack(side="left", fill="both", expand=True, padx=(0, 10))

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

    def load_messages(self):
        # Φόρτωση μηνυμάτων από τη βάση
        conn = get_db_connection()
        if not conn:
            return

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT d.message_text, d.timestamp, u.username
                    FROM discussions d
                    JOIN users u ON d.user_id = u.user_id
                    WHERE d.event_id = %s
                    ORDER BY d.timestamp ASC
                """, (self.event["event_id"],))
                self.messages = cursor.fetchall()
        finally:
            conn.close()

        self.display_messages()

    def display_messages(self):
        # Εμφάνιση όλων των μηνυμάτων
        for widget in self.messages_frame.winfo_children():
            widget.destroy()

        for msg in self.messages:
            msg_frame = ctk.CTkFrame(self.messages_frame, fg_color="white")
            msg_frame.pack(fill="x", pady=5)

            header_frame = ctk.CTkFrame(msg_frame, fg_color="white")
            header_frame.pack(fill="x")

            user_label = ctk.CTkLabel(
                header_frame,
                text=msg["username"],
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                text_color="#C8A165" if msg["username"] == "EventOrganizer" else "black"
            )
            user_label.pack(side="left")

            time_label = ctk.CTkLabel(
                header_frame,
                text=str(msg["timestamp"])[0:16],
                font=ctk.CTkFont(family="Roboto", size=12),
                text_color="gray"
            )
            time_label.pack(side="left", padx=10)

            msg_label = ctk.CTkLabel(
                msg_frame,
                text=msg["message_text"],
                font=ctk.CTkFont(family="Roboto", size=14),
                wraplength=600,
                justify="left"
            )
            msg_label.pack(anchor="w", pady=(5, 10))

            separator = ctk.CTkFrame(msg_frame, height=1, fg_color="#E5E5E5")
            separator.pack(fill="x", pady=(0, 5))


        self.messages_frame._parent_canvas.yview_moveto(1.0)

    def send_message(self):
        #Λήψη κειμένου από input
        message = self.message_input.get("1.0", "end-1c").strip()
        if not message:
            return

        #Αποθήκευση νέου μηνύματος στη βάση
        conn = get_db_connection()
        if not conn:
            return

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO discussions (event_id, user_id, message_text)
                    VALUES (%s, %s, %s)
                """, (self.event["event_id"], self.user_id, message))
                conn.commit()
        finally:
            conn.close()

        
        self.message_input.delete("1.0", "end")
        self.load_messages()

    def show_error(self, message):
        # Εμφάνιση σφάλματος
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
