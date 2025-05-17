import customtkinter as ctk
from classes.event.event import Event
from classes.services.notification_service import NotificationService
from classes.event.ManageEvent import ManageEvent

class DeleteEventPopup(ctk.CTkToplevel):
    def __init__(self, master, dashboard, event_id, organizer_id):
        super().__init__(master)
        self.dashboard = dashboard
        self.event_id = event_id
        self.organizer_id = organizer_id
        self.title("Cancel Event")
        self.geometry("600x400")
        self.transient(master)
        self.grab_set()

        # Periexei to reason pou tha steilei sto notification
        self.cancel_reason = ctk.StringVar()

        self.event = Event.find_by_id(self.event_id)
        if not self.event:
            error_label = ctk.CTkLabel(
                self,
                text="Error: Event not found.",
                text_color="red",
                font=ctk.CTkFont(size=16)
            )
            error_label.pack(pady=50)
            return

        header_frame = ctk.CTkFrame(self, fg_color="white")
        header_frame.pack(fill="x", padx=20, pady=20)

        back_btn = ctk.CTkButton(
            header_frame,
            text="← Back",
            height=32,
            corner_radius=8,
            text_color="black",
            command=self.destroy
        )
        back_btn.pack(side="left")

        title = ctk.CTkLabel(
            header_frame,
            text=f"Cancel Event: {self.event.title}",
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold")
        )
        title.pack(side="left", padx=20)

        # Prosthetoume to input field gia to reason tis akyrwsis
        reason_frame = ctk.CTkFrame(self, fg_color="transparent")
        reason_frame.pack(pady=20)

        reason_label = ctk.CTkLabel(
            reason_frame,
            text="Please provide a reason for cancellation:",
            font=ctk.CTkFont(family="Roboto", size=14)
        )
        reason_label.pack()

        reason_entry = ctk.CTkTextbox(
            reason_frame,
            width=400,
            height=100,
            font=ctk.CTkFont(family="Roboto", size=13)
        )
        reason_entry.pack(pady=10)

        cancel_button_frame = ctk.CTkFrame(self, fg_color="white")
        cancel_button_frame.pack(pady=30)

        cancel_btn = ctk.CTkButton(
            cancel_button_frame,
            text="Continue",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold"),
            fg_color="#D32F2F",
            hover_color="#b62d2d",
            width=200,
            height=50,
            corner_radius=8,
            command=lambda: self.show_cancel_confirmation(reason_entry.get("1.0", "end-1c"))
        )
        cancel_btn.pack()

    def show_cancel_confirmation(self, reason):
        if not reason.strip():
            self.show_error("Please provide a reason for cancellation.")
            return
            
        self.cancel_reason.set(reason)
        dialog = ctk.CTkToplevel(self)
        dialog.title("Cancel Event")
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        # Elegxoume an yparxoun plirwmenoi symmetexontes
        has_paid_participants = self._check_paid_participants()
        
        if has_paid_participants:
            message_text = (
                f"WARNING: There are participants who have paid.\n"
                f"Refund is required.\n\n"
                f"Are you sure you want to cancel {self.event.title}?"
            )
        else:
            message_text = (
                f"Are you sure you want to cancel\n{self.event.title}?\n"
                f"This action cannot be undone."
            )

        message = ctk.CTkLabel(
            dialog,
            text=message_text,
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
            command=lambda: self._on_confirm(dialog)
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

    def _check_paid_participants(self):
        return self.event.is_paid


    def _on_confirm(self, dialog):
        dialog.destroy()
        self.cancel_event()

    def cancel_event(self):
        manage_event = ManageEvent(None)  # To none einai OK giati den xrisimopoioume to current_user
        result = manage_event.cancel_event(self.event_id, self.organizer_id)

        if "successfully" in result:
            self.show_success()
            # Stelnoume to notification me to reason
            NotificationService.notify_participants(
                self.event.title,
                f"The event has been cancelled.\nReason: {self.cancel_reason.get()}"
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
            text=f"{self.event.title} has been successfully cancelled.",
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
            command=lambda: [success.destroy(), self._on_success_ok()]
        )
        ok_btn.pack(pady=20)

    def _on_success_ok(self):
       from ui.Organizer.manage_events import ManageEventsPage
       # An i trexousa selida einai ManageEventsPage kane refresh
       if hasattr(self.dashboard, 'current_page') and isinstance(self.dashboard.current_page, ManageEventsPage):
           self.dashboard.current_page.refresh_events()
       self.destroy()
