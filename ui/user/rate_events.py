import customtkinter as ctk
from src.db_connection import get_db_connection
from src.auth import Auth


class StarRatingWidget(ctk.CTkFrame):
    def __init__(self, master, initial_value=0, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.stars = []
        self.current_rating = initial_value
        
        # Dimiourgia 5 koumpion gia ta asteria
        for i in range(5):
            star = ctk.CTkButton(
                self,
                text="★",
                width=30,
                height=30,
                fg_color="transparent",
                text_color="gray",
                hover_color="#C8A165",
                font=ctk.CTkFont(family="Roboto", size=20),
                command=lambda x=i+1: self.set_rating(x)
            )
            star.pack(side="left", padx=2)
            self.stars.append(star)
            
    def set_rating(self, rating):
        self.current_rating = rating
        # Allagi xromatos asterion analoga me tin axiologisi
        for i, star in enumerate(self.stars):
            star.configure(text_color="#C8A165" if i < rating else "gray")
            
    def get_rating(self):
        return self.current_rating

class RateEventsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")

        current_user = Auth.get_current_user()
        self.user_id = current_user.user_id if current_user else None
        if not self.user_id:
            self.show_error("User not logged in.")
            return

        
        self.header = ctk.CTkLabel(
            self,
            text="Rate Events",
            font=ctk.CTkFont(family="Roboto", size=28, weight="bold")
        )
        self.header.pack(pady=(30, 20), padx=20)

       
        self.events_label = ctk.CTkLabel(
            self,
            text="Share Your Experience",
            font=ctk.CTkFont(family="Roboto", size=18),
            text_color="gray"
        )
        self.events_label.pack(padx=20, pady=(0, 20))

        
        separator = ctk.CTkFrame(self, height=2, fg_color="#E5E5E5")
        separator.pack(fill="x", padx=20, pady=(0, 20))

        self.events_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        self.events_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.load_events()

    def load_events(self):
        from src.classes.event.eventParticipation import EventParticipation
        self.events = EventParticipation.get_unrated_events(self.user_id)
        
        if not self.events:
            self.show_error("There are no events available for review.")
        else:
            self.display_events()

    def display_events(self):
        for widget in self.events_frame.winfo_children():
            widget.destroy()

        for event in self.events:
            card = ctk.CTkFrame(self.events_frame, fg_color="white",
                                border_width=1, border_color="#E5E5E5")
            card.pack(fill="x", padx=20, pady=10)

            content = ctk.CTkFrame(card, fg_color="white")
            content.pack(side="left", fill="both", expand=True, padx=15, pady=15)

            # Titlos event me megalitero megethos grammatoseiras
            title = ctk.CTkLabel(
                content,
                text=event["title"],
                font=ctk.CTkFont(family="Roboto", size=20, weight="bold")
            )
            title.pack(anchor="w")

            # Info me icons kai xroma
            info_frame = ctk.CTkFrame(content, fg_color="transparent")
            info_frame.pack(fill="x", pady=(10, 0))

            date = ctk.CTkLabel(
                info_frame,
                text=f"📅 {event['event_date']}",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="#666666"
            )
            date.pack(side="left", padx=(0, 15))

            location = ctk.CTkLabel(
                info_frame,
                text=f"📍 {event['venue']}",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="#666666"
            )
            location.pack(side="left")

            # Rating button me kalitero style
            button_frame = ctk.CTkFrame(card, fg_color="white")
            button_frame.pack(side="right", padx=15, pady=15)

            rate_btn = ctk.CTkButton(
                button_frame,
                text="Rate & Review →",
                font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                fg_color="#C8A165",
                hover_color="#b38e58",
                width=140,
                height=38,
                corner_radius=8,
                command=lambda e=event: self.show_rating_dialog(e)
            )
            rate_btn.pack(expand=True)

    def show_rating_dialog(self, event):
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Rate Event")
        dialog.geometry("500x600")
        
        
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 600) // 2
        dialog.geometry(f"500x600+{x}+{y}")
        dialog.transient(self)
        dialog.grab_set()

       
        ctk.CTkLabel(
            dialog,
            text=f"Share Your Experience",
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold")
        ).pack(pady=(30, 5), padx=30)

        ctk.CTkLabel(
            dialog,
            text=event['title'],
            font=ctk.CTkFont(family="Roboto", size=16),
            text_color="gray"
        ).pack(pady=(0, 20))

        # Event Rating section
        ctk.CTkLabel(
            dialog,
            text="How was the event?",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold")
        ).pack(pady=(20, 10), padx=30, anchor="w")

        self.rating_event = StarRatingWidget(dialog)
        self.rating_event.pack(pady=(0, 20), padx=30)

        # Organizer Rating section
        ctk.CTkLabel(
            dialog,
            text="Rate the organizer",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold")
        ).pack(pady=(0, 10), padx=30, anchor="w")

        self.rating_org = StarRatingWidget(dialog)
        self.rating_org.pack(pady=(0, 20), padx=30)

        # Comment section
        ctk.CTkLabel(
            dialog,
            text="Share your thoughts",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold")
        ).pack(pady=(0, 10), padx=30, anchor="w")

        self.comment = ctk.CTkTextbox(
            dialog,
            height=150,
            font=ctk.CTkFont(family="Roboto", size=14),
            border_color="#E5E5E5",
            border_width=2
        )
        self.comment.pack(pady=(0, 30), padx=30, fill="x")

        # Submit button
        submit_btn = ctk.CTkButton(
            dialog,
            text="Submit Review",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold"),
            fg_color="#C8A165",
            hover_color="#b38e58",
            height=45,
            corner_radius=8,
            command=lambda: self.submit_review(event["event_id"], dialog)
        )
        submit_btn.pack(pady=(0, 30), padx=30, fill="x")

    def submit_review(self, event_id, dialog):
        from src.classes.event.eventParticipation import EventParticipation
        
        try:
            event_rating = self.rating_event.get_rating()
            organizer_rating = self.rating_org.get_rating()
        except ValueError:
            self.show_error("Please provide a valid rating and review")
            return
            
        comment = self.comment.get("1.0", "end").strip()
        
        if not event_rating or not organizer_rating or not comment:
            self.show_error("Please provide a valid rating and review")
            return
            
        participation = EventParticipation(event_id, self.user_id)
        success, message = participation.rate_event(
            event_rating,
            organizer_rating,
            comment
        )
        
        if success:
            dialog.destroy()
            self.show_success(message)
            self.load_events()
        else:
            self.show_error(message)

    def center_dialog(self, dialog):
        """Center a dialog window on the screen"""
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        
        dialog_width = 400
        dialog_height = 150
        
        x = (screen_width - dialog_width) // 2
        y = (screen_height - dialog_height) // 2
        
        dialog.geometry(f"400x150+{x}+{y}")

    def show_success(self, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Success")
        self.center_dialog(dialog)
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
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            command=dialog.destroy
        ).pack(pady=20)

    def show_error(self, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Error")
        self.center_dialog(dialog)
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
