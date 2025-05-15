import customtkinter as ctk
from tkinter import messagebox
from src.db_connection import get_db_connection
from src.auth import Auth  # Πρέπει να παρέχει user_id μέσω Auth.get_current_user()
from datetime import datetime


class MyInvitesPage(ctk.CTkFrame):
    def __init__(self, master, dashboard):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard
        self.invites = []

        # Header
        header_frame = ctk.CTkFrame(self, fg_color="white")
        header_frame.pack(fill="x", padx=20, pady=20)

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

        title = ctk.CTkLabel(
            header_frame,
            text="Pending Invites",
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold")
        )
        title.pack(side="left", padx=20)

        self.invites_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        self.invites_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.load_invites()

    def load_invites(self):
        self.invites = []
        current_user = Auth.get_current_user()
        if not current_user:
            messagebox.showerror("Error", "User not logged in.")
            return

        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Error", "Database connection failed.")
            return

        try:
            with conn.cursor() as cursor:
                query = """
                        SELECT i.invitation_id, \
                               i.sender_userid, \
                               u.username                               AS from_username, \
                               CONCAT(ui.first_name, ' ', ui.last_name) AS from_name, \
                               e.title                                  AS event_title, \
                               e.event_date, \
                               e.venue                                  AS event_location, \
                               i.sender_message                         AS message, \
                               i.status
                        FROM invitations i
                                 JOIN users u ON i.sender_userid = u.user_id
                                 JOIN user_info ui ON u.user_id = ui.user_id
                                 JOIN events e ON i.event_id = e.event_id
                        WHERE i.receipient_userid = %s \
                          AND i.status = 'pending' \
                          AND e.status = 'scheduled' \
                        """
                cursor.execute(query, (current_user.user_id,))
                self.invites = cursor.fetchall()  # DictCursor επιστρέφει dicts ήδη
        except Exception as e:
            print(f"[MyInvitesPage] Error loading invites: {e}")
            messagebox.showerror("Error", "Could not load invites.")
        finally:
            conn.close()

        self.display_invites()

    def display_invites(self):
        for widget in self.invites_frame.winfo_children():
            widget.destroy()

        if not self.invites:
            no_invites_label = ctk.CTkLabel(
                self.invites_frame,
                text="No pending invites.",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            no_invites_label.pack(pady=20)
            return

        for invite in self.invites:
            self.create_invite_card(invite)

    def create_invite_card(self, invite):
        card = ctk.CTkFrame(self.invites_frame, fg_color="white", border_width=1, border_color="#E5E5E5")
        card.pack(fill="x", padx=10, pady=10)

        event_frame = ctk.CTkFrame(card, fg_color="white")
        event_frame.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            event_frame,
            text=invite.get("event_title", "No Title"),
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold")
        ).pack(anchor="w")

        event_date = invite.get("event_date")
        if event_date:
            if isinstance(event_date, datetime):
                formatted_date = event_date.strftime("%d %b %Y, %H:%M")
            else:
                formatted_date = str(event_date)
        else:
            formatted_date = "Unknown date"

        ctk.CTkLabel(
            event_frame,
            text=f"📅 Date: {formatted_date}",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", pady=(5, 0))

        ctk.CTkLabel(
            event_frame,
            text=f"📍 Location: {invite.get('event_location', 'Unknown')}",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", pady=(5, 0))

        ctk.CTkFrame(card, height=1, fg_color="#E5E5E5").pack(fill="x", padx=15, pady=10)

        from_frame = ctk.CTkFrame(card, fg_color="white")
        from_frame.pack(fill="x", padx=15, pady=5)

        from_info = ctk.CTkFrame(from_frame, fg_color="white")
        from_info.pack(anchor="w")

        ctk.CTkLabel(from_info, text="👤", font=ctk.CTkFont(size=20)).pack(side="left", padx=(0, 5))
        ctk.CTkLabel(
            from_info,
            text=invite.get("from_name", "Unknown Sender"),
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")
        ctk.CTkLabel(
            from_info,
            text=f"@{invite.get('from_username', 'unknown')}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(side="left", padx=5)

        ctk.CTkLabel(
            card,
            text=invite.get("message", ""),
            font=ctk.CTkFont(size=14),
            wraplength=600,
            justify="left"
        ).pack(anchor="w", padx=15, pady=(5, 15))

        buttons_frame = ctk.CTkFrame(card, fg_color="white")
        buttons_frame.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkButton(
            buttons_frame,
            text="Accept  ✓",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            height=35,
            corner_radius=8,
            command=lambda i=invite: self.accept_invite(i)
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            buttons_frame,
            text="Reject  ×",
            fg_color="#f44336",
            hover_color="#e53935",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            height=35,
            corner_radius=8,
            command=lambda i=invite: self.reject_invite(i)
        ).pack(side="left")

    def accept_invite(self, invite):
        self.update_invite_status(invite["invitation_id"], "accepted")
        messagebox.showinfo("Success", f"You have accepted the invitation to {invite['event_title']}.")
        self.dashboard.show_page("My Events")

    def reject_invite(self, invite):
        result = messagebox.askyesno("Reject Invite", f"Reject invitation to {invite['event_title']}?")
        if result:
            self.update_invite_status(invite["invitation_id"], "rejected")
            self.load_invites()

    def update_invite_status(self, invitation_id, status):
        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Error", "Database connection failed.")
            return

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE invitations SET status = %s WHERE invitation_id = %s",
                    (status, invitation_id)
                )
            conn.commit()
        except Exception as e:
            print(f"[MyInvitesPage] Update error: {e}")
            messagebox.showerror("Error", "Failed to update invitation.")
        finally:
            conn.close()
