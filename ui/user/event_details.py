import customtkinter as ctk
from classes.member.member import Member
from classes.services.payment_handler import PaymentHandler
from classes.services.notification_service import NotificationService

class EventDetailsPage(ctk.CTkFrame):
    def __init__(self, master, dashboard, event_id):
        super().__init__(master, fg_color="white")
        self.dashboard = dashboard
        # Fetch event details from database
        from classes.event.event import Event  
        self.event = Event.find_by_id(event_id)
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
            command=self.dashboard.back_to_find_events
        )
        back_btn.pack(side="left")
        
        # Event Title
        title = ctk.CTkLabel(
            header_frame,
            text=self.event.title,
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold")
        )
        title.pack(side="left", padx=20)
        
        # Main Content
        content_frame = ctk.CTkFrame(self, fg_color="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))
        
        # Description
        desc_label = ctk.CTkLabel(
            content_frame,
            text=self.event.description,
            font=ctk.CTkFont(family="Roboto", size=14),
            justify="left",
            wraplength=600
        )
        desc_label.pack(anchor="w", pady=(0,20))
        
        # Separator
        separator = ctk.CTkFrame(content_frame, height=2, fg_color="#E5E5E5")
        separator.pack(fill="x", pady=20)
        
        # Event Details
        # Get current participants and format details
        current_participants = self.event.get_current_participant_count() or 0
        max_part_text = f"{current_participants}/{self.event.max_participants}" if self.event.max_participants else str(current_participants)
        
        # Format cost display
        self.cost_text = "Free" if not self.event.is_paid else f"€{self.event.cost:.2f}"
        
        # Get status based on availability and event status
        if self.event.status == 'cancelled':
            status = 'Cancelled'
        elif self.event.status == 'completed':
            status = 'Completed'
        else:
            status = 'Joinable' if self.event.check_availability() else 'Full'
        
        # Get organizer name
        organizer_name = Member.get_name_by_id(self.event.organizer_id)
        
        details = [
            ("📅 Date", self.event.event_date.strftime('%Y-%m-%d %H:%M')),
            ("📍 Location", self.event.venue),
            ("👥 Status", status),
            ("🌐 Visibility", "Public" if self.event.is_public else "Private"),
            ("👥 Participants", max_part_text),
            ("💶 Cost", self.cost_text),
            ("👤 Organizer", organizer_name)
        ]
        
        for label, value in details:
            detail_frame = ctk.CTkFrame(content_frame, fg_color="white")
            detail_frame.pack(fill="x", pady=5)
            
            label = ctk.CTkLabel(
                detail_frame,
                text=f"{label}:",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold")
            )
            label.pack(side="left")
            
            value = ctk.CTkLabel(
                detail_frame,
                text=value,
                font=ctk.CTkFont(family="Roboto", size=14)
            )
            value.pack(side="left", padx=(10,0))
        
        # Separator before buttons
        separator2 = ctk.CTkFrame(content_frame, height=2, fg_color="#E5E5E5")
        separator2.pack(fill="x", pady=20)
        
        # Buttons Frame
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="white")
        buttons_frame.pack(pady=20)
        
        # Invite Friends Button
        invite_btn = ctk.CTkButton(
            buttons_frame,
            text="Invite Friends  →",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            fg_color="#C8A165",
            hover_color="#b38e58",
            width=200,
            height=40,
            corner_radius=8,
            command=lambda: self.dashboard.show_invite_friends(self.event)
        )
        invite_btn.pack(side="left", padx=10)
        
        # Join Event Button 
        join_btn = ctk.CTkButton(
            buttons_frame,
            text="Join Event  →",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049" if status == 'Joinable' else "#666666",
            width=200,
            height=40,
            corner_radius=8,
            command=self.join_event 
        )
        join_btn.pack(side="left", padx=10)
    
    def join_event(self):
        # Initial confirmation dialog
        self.show_confirmation_dialog()
    
    def show_confirmation_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Join Event")
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
            text=f"Are you sure you want to join\n{self.event.title}?\n\nParticipation cost: {self.cost_text}",
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
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            command=lambda: [dialog.destroy(), self.show_checking_availability()]
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

    def show_checking_availability(self):
        # Check availability dialog
        check_dialog = ctk.CTkToplevel(self)
        check_dialog.title("Checking Availability")
        check_dialog.geometry("300x150")
        check_dialog.transient(self)
        check_dialog.grab_set()
        
        # Center dialog
        check_dialog.update_idletasks()
        x = (check_dialog.winfo_screenwidth() - check_dialog.winfo_width()) // 2
        y = (check_dialog.winfo_screenheight() - check_dialog.winfo_height()) // 2
        check_dialog.geometry(f"+{x}+{y}")
        
        # Message
        message = ctk.CTkLabel(
            check_dialog,
            text="Checking availability...\nPlease wait",
            font=ctk.CTkFont(family="Roboto", size=14),
            justify="center"
        )
        message.pack(expand=True)
        
        # Simulate checking availability
        self.after(1000, lambda: self.check_result(check_dialog))
    
    def check_result(self, check_dialog):
        if self.event.check_availability():
            check_dialog.destroy()
            self.show_payment_dialog()
        else:
            check_dialog.destroy()
            self.show_error("Cannot Join Event. \nEvent has reached max participants.")
    
    def show_payment_dialog(self):
        # Show payment dialog and process payment
        PaymentHandler.show_payment_dialog(
            parent=self,
            event=self.event,
            on_success=self.finalize_registration
        )
    
    def finalize_registration(self):
        
        # Register participant
        from src.classes.event.eventParticipation import EventParticipation
        participation = EventParticipation(self.event.event_id, self.dashboard.current_user.user_id)
        success, message = participation.register()
        if success:
            # Send confirmation email to participant
            NotificationService.send_confirmation_email(
                self.dashboard.current_user.username,
                self.event.title,
                self.event.event_date.strftime('%Y-%m-%d %H:%M'),
                self.event.venue
            )
            
            # Get organizer's username and notify
            organizer = Member.get_name_by_id(self.event.organizer_id)
            NotificationService.notify_organizer(
                organizer,
                self.event.title,
                self.dashboard.current_user.username
            )
            self.show_success()
        else:
            self.show_error("Failed to register. You might already be registered.")
    
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
            text=f"You have successfully joined\n{self.event.title}! Confirmation email sent.",
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
            command=lambda: [success.destroy(), self.dashboard.show_page("My Events")]
        )
        ok_btn.pack(pady=20)
