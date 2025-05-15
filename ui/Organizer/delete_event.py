import customtkinter as ctk
from classes.event.event import Event
from classes.services.notification_service import NotificationService
from classes.event.event_deletion import EventDeletion
# Αφαιρέθηκε το import ManageEventsPage από εδώ


class DeleteEventPopup(ctk.CTkToplevel):
    def __init__(self, master, dashboard, event_id, organizer_id):
        super().__init__(master)
        self.dashboard = dashboard
        self.event_id = event_id
        self.organizer_id = organizer_id
        self.title("Delete Event")
        self.geometry("600x300")
        self.transient(master)
        self.grab_set()

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
            text=f"Delete Event: {self.event.title}",
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold")
        )
        title.pack(side="left", padx=20)

        delete_button_frame = ctk.CTkFrame(self, fg_color="white")
        delete_button_frame.pack(pady=30)

        delete_btn = ctk.CTkButton(
            delete_button_frame,
            text="Delete Event",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold"),
            fg_color="#D32F2F",
            hover_color="#b62d2d",
            width=200,
            height=50,
            corner_radius=8,
            command=self.show_delete_confirmation
        )
        delete_btn.pack()

    def show_delete_confirmation(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Delete Event")
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        message = ctk.CTkLabel(
            dialog,
            text=f"Are you sure you want to delete\n{self.event.title}?\nThis action cannot be undone.",
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

    def _on_confirm(self, dialog):
        dialog.destroy()
        self.delete_event()

    def delete_event(self):
        event_deletion = EventDeletion()
        result = event_deletion.delete_event(self.event_id, self.organizer_id)

        if "successfully" in result:
            self.show_success()
            NotificationService.notify_participants(
                self.event.title,
                "The event has been deleted."
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
            text=f"{self.event.title} has been successfully deleted.",
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
       # Αν η τρέχουσα σελίδα είναι ManageEventsPage κάνε refresh
       if hasattr(self.dashboard, 'current_page') and isinstance(self.dashboard.current_page, ManageEventsPage):
           self.dashboard.current_page.refresh_events()
       self.destroy()

