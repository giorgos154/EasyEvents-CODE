from classes.event.event import Event
from classes.services.notification_service import NotificationService
from datetime import datetime

class WithdrawParticipation:
    def __init__(self):
        pass

    def withdraw(self, event_id, user_id, event):
        # Χρησιμοποιούμε την εκδήλωση που παρέχεται από την κλάση Event
        try:
            # Έλεγχος αν υπάρχει συμμετοχή
            if not event.is_user_participating(user_id):
                return "Participation not found or you are not registered for the event."

            # Έλεγχος ημερομηνίας
            current_date = self.get_current_date()

            if current_date > event.event_date:
                return "Withdrawal is not allowed after the event's deadline."

            # Διαγραφή συμμετοχής μέσω της κλάσης Event
            if not event.remove_participation(user_id):
                return "Failed to withdraw participation."

            return "Your participation has been successfully withdrawn."

        except Exception as e:
            return f"Error during withdrawal: {str(e)}"

    def get_current_date(self):
        # Επιστρέφει την τρέχουσα ημερομηνία ως datetime αντικείμενο
        return datetime.now()


class WithdrawParticipationPage(ctk.CTkFrame):
    def __init__(self, master, dashboard, event_id, user_id):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard
        self.event_id = event_id
        self.user_id = user_id

        # Φέρνουμε τα στοιχεία της εκδήλωσης χρησιμοποιώντας την κλάση Event
        self.event = Event.find_by_id(self.event_id)
        if not self.event:
            error_label = ctk.CTkLabel(self, text="Error: Event not found.", text_color="red", font=ctk.CTkFont(size=16))
            error_label.pack(pady=50)
            return

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
            command=self.dashboard.back_to_manage_events
        )
        back_btn.pack(side="left")

        title = ctk.CTkLabel(
            header_frame,
            text=f"Withdraw from Event: {self.event.title}",
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold")
        )
        title.pack(side="left", padx=20)

        withdraw_button_frame = ctk.CTkFrame(self, fg_color="white")
        withdraw_button_frame.pack(pady=30)

        withdraw_btn = ctk.CTkButton(
            withdraw_button_frame,
            text="Withdraw Participation",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold"),
            fg_color="#D32F2F",
            hover_color="#b62d2d",
            width=200,
            height=50,
            corner_radius=8,
            command=self.show_withdraw_confirmation
        )
        withdraw_btn.pack()

    def show_withdraw_confirmation(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Withdraw Participation")
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        message = ctk.CTkLabel(
            dialog,
            text=f"Are you sure you want to withdraw\nfrom {self.event.title}?\nThis action cannot be undone.",
            font=ctk.CTkFont(family="Roboto", size=14),
            justify="center"
        )
        message.pack(expand=True, padx=20)

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)

        confirm_btn = ctk.CTkButton(
            btn_frame,
            text="Confirm",
            fg_color="#D32F2F",
            hover_color="#b62d2d",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            command=lambda: [dialog.destroy(), self.withdraw_participation()]
        )
        confirm_btn.pack(side="left", padx=10)

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

    def withdraw_participation(self):
        withdrawal = WithdrawParticipation()
        result = withdrawal.withdraw(self.event_id, self.user_id, self.event)

        if "successfully" in result:
            self.show_success()
            NotificationService.notify_participants(
                self.event.title,
                f"A participant has withdrawn from {self.event.title}."
            )
        else:
            self.show_error(result)

    def show_error(self, message):
        error = ctk.CTkToplevel(self)
        error.title("Error")
        error.geometry("300x150")
        error.transient(self)
        error.grab_set()

        error.update_idletasks()
        x = (error.winfo_screenwidth() - error.winfo_width()) // 2
        y = (error.winfo_screenheight() - error.winfo_height()) // 2
        error.geometry(f"+{x}+{y}")

        message_label = ctk.CTkLabel(
            error,
            text=message,
            font=ctk.CTkFont(family="Roboto", size=14),
            text_color="red",
            justify="center"
        )
        message_label.pack(expand=True)

        ok_btn = ctk.CTkButton(
            error,
            text="OK",
            fg_color="gray",
            hover_color="#666666",
            font=ctk.CTkFont(family="Roboto", size=14),
            width=100,
            command=error.destroy
        )
        ok_btn.pack(pady=20)

    def show_success(self):
        success = ctk.CTkToplevel(self)
        success.title("Success!")
        success.geometry("400x150")
        success.transient(self)
        success.grab_set()

        success.update_idletasks()
        x = (success.winfo_screenwidth() - success.winfo_width()) // 2
        y = (success.winfo_screenheight() - success.winfo_height()) // 2
        success.geometry(f"+{x}+{y}")

        message = ctk.CTkLabel(
            success,
            text=f"You have successfully withdrawn from\n{self.event.title}.",
            font=ctk.CTkFont(family="Roboto", size=16),
            justify="center"
        )
        message.pack(expand=True)

        ok_btn = ctk.CTkButton(
            success,
            text="OK",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            command=lambda: [success.destroy(), self.dashboard.show_page("Manage Events")]
        )
        ok_btn.pack(pady=20)
