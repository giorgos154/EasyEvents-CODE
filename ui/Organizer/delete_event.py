import customtkinter as ctk
from classes.event.event import Event
from classes.services.notification_service import NotificationService

class EventDeletion:
    def __init__(self):
        pass

    def delete_event(self, event_id, organizer_id):
        event = Event.find_by_id(event_id)  # Fetch the event using Event class
        if not event:
            return "Event not found."

        if event.organizer_id != organizer_id:
            return "You do not have permission to delete this event."

        try:
            # Check for paid participants
            if event.has_paid_participants():
                return "There are paid participants. A refund is required before deletion."

            # Proceed to delete participants and the event
            event.delete_participants()
            event.delete_event()

            return "Event deleted successfully."

        except Exception as e:
            return f"Error during deletion: {str(e)}"


class DeleteEventPage(ctk.CTkFrame):
    def __init__(self, master, dashboard, event_id, organizer_id):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard
        self.event_id = event_id
        self.organizer_id = organizer_id

        # Fetch event details
        self.event = Event.find_by_id(self.event_id)
        if not self.event:
            # Show error if event not found
            error_label = ctk.CTkLabel(self, text="Error: Event not found.", text_color="red", font=ctk.CTkFont(size=16))
            error_label.pack(pady=50)
            return

        # Header
        header_frame = ctk.CTkFrame(self, fg_color="white")
        header_frame.pack(fill="x", padx=20, pady=20)

        # Back button
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

        # Event Title
        title = ctk.CTkLabel(
            header_frame,
            text=f"Delete Event: {self.event.title}",
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold")
        )
        title.pack(side="left", padx=20)

        # Confirm Deletion button
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

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        # Confirmation message
        message = ctk.CTkLabel(
            dialog,
            text=f"Are you sure you want to delete\n{self.event.title}?\nThis action cannot be undone.",
            font=ctk.CTkFont(family="Roboto", size=14),
            justify="center"
        )
        message.pack(expand=True, padx=20)

        # Buttons frame
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)

        # Confirm button
        confirm_btn = ctk.CTkButton(
            btn_frame,
            text="Confirm",
            fg_color="#D32F2F",
            hover_color="#b62d2d",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            command=lambda: [dialog.destroy(), self.delete_event()]
        )
        confirm_btn.pack(side="left", padx=10)

        # Cancel button
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

    def delete_event(self):
        # Delete the event from the database
        event_deletion = EventDeletion()
        result = event_deletion.delete_event(self.event_id, self.organizer_id)

        if "successfully" in result:
            self.show_success()
            # Notify the users of the cancellation
            NotificationService.notify_participants(
                self.event.title,
                "The event has been deleted."
            )
        else:
            self.show_error(result)

    def show_error(self, message):
        # Error dialog
        error = ctk.CTkToplevel(self)
        error.title("Error")
        error.geometry("300x150")
        error.transient(self)
        error.grab_set()

        # Center dialog
        error.update_idletasks()
        x = (error.winfo_screenwidth() - error.winfo_width()) // 2
        y = (error.winfo_screenheight() - error.winfo_height()) // 2
        error.geometry(f"+{x}+{y}")

        # Error message
        message_label = ctk.CTkLabel(
            error,
            text=message,
            font=ctk.CTkFont(family="Roboto", size=14),
            text_color="red",
            justify="center"
        )
        message_label.pack(expand=True)

        # OK button
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
        # Success dialog
        success = ctk.CTkToplevel(self)
        success.title("Success!")
        success.geometry("400x150")
        success.transient(self)
        success.grab_set()

        # Center dialog
        success.update_idletasks()
        x = (success.winfo_screenwidth() - success.winfo_width()) // 2
        y = (success.winfo_screenheight() - success.winfo_height()) // 2
        success.geometry(f"+{x}+{y}")

        # Success message
        message = ctk.CTkLabel(
            success,
            text=f"{self.event.title} has been successfully deleted.",
            font=ctk.CTkFont(family="Roboto", size=16),
            justify="center"
        )
        message.pack(expand=True)

        # OK button
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
