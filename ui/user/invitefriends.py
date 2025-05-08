import pymysql
import customtkinter as ctk
from src.auth import Auth


class InviteFriendsPage(ctk.CTkFrame):
    def __init__(self, master, dashboard, event):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard
        self.event = event
        self.selected_friends = {}

        self.build_ui()

    def build_ui(self):

        header = ctk.CTkFrame(self, fg_color="white")
        header.pack(fill="x", padx=20, pady=20)

        ctk.CTkButton(
            header,
            text="← Back",
            fg_color="#C8A165",
            hover_color="#b38e58",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            height=32,
            corner_radius=8,
            text_color="black",
            command=self.dashboard.back_to_find_events
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text=f"Invite Friends to {self.event.title}",
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold")
        ).pack(side="left", padx=20)


        content = ctk.CTkFrame(self, fg_color="white")
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        ctk.CTkLabel(
            content,
            text="Select Friends to Invite:",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold")
        ).pack(anchor="w", pady=(0, 10))

        self.friends_frame = ctk.CTkScrollableFrame(content, fg_color="white")
        self.friends_frame.pack(fill="both", expand=True)

        self.load_friends()

        ctk.CTkLabel(
            content,
            text="Personal Message:",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold")
        ).pack(anchor="w", pady=(20, 10))

        self.message_box = ctk.CTkTextbox(content, height=100, font=ctk.CTkFont(family="Roboto", size=14))
        self.message_box.pack(fill="x")
        self.message_box.insert("1.0", f"Hey! Join me at {self.event.title}!")

        ctk.CTkButton(
            content,
            text="Send Invites →",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049",
            width=200,
            height=40,
            corner_radius=8,
            command=self.confirm_invites
        ).pack(pady=20)

    def load_friends(self):
        current_user = Auth.get_current_user()
        if not current_user:
            self.show_error("User not logged in.")
            return

        user_id = current_user.user_id

        try:

            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="root",
                database="τλ",
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = conn.cursor()


            query = """
                    SELECT u.username
                    FROM users u
                             JOIN friendships f ON
                        (u.user_id = f.user1_id AND f.user2_id = %s)
                            OR (u.user_id = f.user2_id AND f.user1_id = %s)
                    WHERE u.user_id != %s \
                    """
            cursor.execute(query, (user_id, user_id, user_id))
            friends = cursor.fetchall()


            for widget in self.friends_frame.winfo_children():
                widget.destroy()


            if not friends:
                ctk.CTkLabel(self.friends_frame, text="No friends found.", font=ctk.CTkFont(size=14)).pack()
                return


            self.selected_friends = {}
            for friend in friends:
                username = friend["username"]

                friend_frame = ctk.CTkFrame(self.friends_frame, fg_color="white")
                friend_frame.pack(fill="x", pady=5)

                var = ctk.BooleanVar()
                self.selected_friends[username] = var

                ctk.CTkCheckBox(
                    friend_frame,
                    text=username,
                    variable=var,
                    fg_color="#C8A165",
                    hover_color="#b38e58"
                ).pack(side="left", padx=10)


            conn.close()

        except Exception as e:
            self.show_error(f"Failed to load friends: {str(e)}")

    def confirm_invites(self):
        selected = [username for username, var in self.selected_friends.items() if var.get()]
        if not selected:
            self.show_error("Please select at least one friend to invite.")
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm Invites")
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()

        self.center_window(dialog)

        ctk.CTkLabel(
            dialog,
            text=f"Send invites to {len(selected)} friend{'s' if len(selected) > 1 else ''}?",
            font=ctk.CTkFont(family="Roboto", size=16)
        ).pack(expand=True)

        buttons = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons.pack(pady=20)

        ctk.CTkButton(
            buttons,
            text="Confirm",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            command=lambda: [dialog.destroy(), self.send_invites()]
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            buttons,
            text="Cancel",
            fg_color="gray",
            hover_color="#666666",
            font=ctk.CTkFont(family="Roboto", size=14),
            width=100,
            command=dialog.destroy
        ).pack(side="left", padx=10)

    def send_invites(self):

        self.show_success()

    def show_success(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Success")
        dialog.geometry("400x150")
        dialog.transient(self)
        dialog.grab_set()

        self.center_window(dialog)

        ctk.CTkLabel(
            dialog,
            text="Invites have been sent successfully!",
            font=ctk.CTkFont(family="Roboto", size=16)
        ).pack(expand=True)

        ctk.CTkButton(
            dialog,
            text="OK",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            command=lambda: [dialog.destroy(), self.dashboard.back_to_find_events()]
        ).pack(pady=20)

    def show_error(self, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Error")
        dialog.geometry("400x150")
        dialog.transient(self)
        dialog.grab_set()

        self.center_window(dialog)

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

    def center_window(self, window):
        window.update_idletasks()
        x = (window.winfo_screenwidth() - window.winfo_width()) // 2
        y = (window.winfo_screenheight() - window.winfo_height()) // 2
        window.geometry(f"+{x}+{y}")
