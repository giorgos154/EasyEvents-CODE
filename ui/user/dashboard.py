import customtkinter as ctk
from PIL import Image
import os
from src.auth import Auth
from ui.user.findevents import FindEventsPage
from ui.user.myevents import MyEventsPage
from ui.user.myprofile import MyProfilePage
from ui.user.points import PointsPage
from ui.user.rewards import RewardsPage
from ui.user.rate_events import RateEventsPage
from ui.user.event_discussion import EventDiscussionPage
from ui.user.event_details import EventDetailsPage
from ui.user.invitefriends import InviteFriendsPage
from ui.user.my_invites import MyInvitesPage

class UserDashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.current_user = Auth.get_current_user()  # Store current user
        if not self.current_user:
            raise ValueError("No authenticated user found")
        self.current_page = None
        self.last_page = None  # Track last main page for back navigation

        # Sidebar (Gold background)
        self.sidebar = ctk.CTkFrame(self, corner_radius=0, fg_color="#C8A165", width=250)
        self.sidebar.pack(side="left", fill="y", expand=False)
        self.sidebar.pack_propagate(False)

        # Load and display logo
        image_path = os.path.join("assets", "logo_transparent.png")
        logo_image = Image.open(image_path)
        self.logo_ctk = ctk.CTkImage(light_image=logo_image, 
                                    dark_image=logo_image,
                                    size=(200, 45))
        
        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="",
            image=self.logo_ctk
        )
        self.logo_label.pack(pady=(20, 110))

        # Menu items
        self.menu_items = [
            ("Homepage", "🏠"),
            ("Find Events", "🔍"),
            ("My Events", "📅"),
            ("Rate Events", "⭐"),
            ("My Profile", "👤"),
            ("Points & Rewards", "🌟")
        ]

        self.menu_buttons = []
        for text, icon in self.menu_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"{icon} {text}",
                fg_color="transparent",
                text_color="white",
                hover_color="#b38e58",
                anchor="w",
                font=ctk.CTkFont(size=16),
                command=lambda t=text: self.show_page(t)
            )
            btn.pack(pady=5, padx=10, fill="x")
            self.menu_buttons.append(btn)

        # Username display
        self.username_label = ctk.CTkLabel(
            self.sidebar,
            text=f"👤 {self.current_user.username}",
            fg_color="#96753d",
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=6,
            height=32
        )
        self.username_label.pack(side="bottom", pady=(0, 10), padx=10, fill="x")

        # Logout button at bottom
        self.logout_btn = ctk.CTkButton(
            self.sidebar,
            text="🚪 Logout",
            fg_color="#b38e58",
            text_color="white",
            hover_color="#96753d",
            command=self.logout
        )
        self.logout_btn.pack(side="bottom", pady=20, padx=10, fill="x")

        # Content area (White background)
        self.content_area = ctk.CTkFrame(self, corner_radius=0, fg_color="black")
        self.content_area.pack(side="left", fill="both", expand=True)

        # Welcome frame
        self.setup_welcome_frame()

    def setup_welcome_frame(self):
        """Setup welcome frame with logo and text"""
        self.welcome_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.welcome_frame.place(relx=0.5, rely=0.5, anchor="center")

        welcome_image_path = os.path.join("assets", "logo_transparent2.png")
        welcome_image = Image.open(welcome_image_path)
        self.welcome_logo = ctk.CTkImage(
            light_image=welcome_image,
            dark_image=welcome_image,
            size=(400, 90)
        )

        self.welcome_logo_label = ctk.CTkLabel(
            self.welcome_frame,
            text="",
            image=self.welcome_logo
        )
        self.welcome_logo_label.pack(pady=20)

        self.welcome_text = ctk.CTkLabel(
            self.welcome_frame,
            text="Welcome to EasyEvents!\nNavigate in the app using the sidebar!",
            font=ctk.CTkFont(size=20),
            text_color="white"
        )
        self.welcome_text.pack(pady=20)

    def clear_content(self):
        """Clear current content area"""
        if self.current_page is not None:
            self.current_page.destroy()
        self.welcome_frame.place_forget()

    def show_page(self, page_name):
        """Update content area based on selected menu item"""
        self.clear_content()
        self.last_page = page_name

        # Show selected page
        if page_name == "Homepage":
            self.welcome_frame.place(relx=0.5, rely=0.5, anchor="center")
            self.current_page = None
        elif page_name == "Find Events":
            self.current_page = FindEventsPage(self.content_area, self)
            self.current_page.pack(fill="both", expand=True)
        elif page_name == "My Events":
            self.current_page = MyEventsPage(self.content_area, self)
            self.current_page.pack(fill="both", expand=True)
        elif page_name == "Rate Events":
            self.current_page = RateEventsPage(self.content_area)
            self.current_page.pack(fill="both", expand=True)
        elif page_name == "My Profile":
            self.current_page = MyProfilePage(self.content_area, self)
            self.current_page.pack(fill="both", expand=True)
        elif page_name == "Points & Rewards":
            self.current_page = PointsPage(self.content_area, self)
            self.current_page.pack(fill="both", expand=True)

    def show_event_details(self, event):
        """Show event details page"""
        self.clear_content()
        self.current_page = EventDetailsPage(self.content_area, self, event)
        self.current_page.pack(fill="both", expand=True)
    
    def show_event_discussion(self, event):
        """Show event discussion page"""
        self.clear_content()
        self.current_page = EventDiscussionPage(self.content_area, self, event)
        self.current_page.pack(fill="both", expand=True)
    
    def show_invite_friends(self, event):
        """Show invite friends page"""
        self.clear_content()
        self.current_page = InviteFriendsPage(self.content_area, self, event)
        self.current_page.pack(fill="both", expand=True)
    
    def show_my_invites(self):
        """Show my invites page"""
        self.clear_content()
        self.current_page = MyInvitesPage(self.content_area, self)
        self.current_page.pack(fill="both", expand=True)

    def show_rewards(self):
        """Show rewards page"""
        self.clear_content()
        self.current_page = RewardsPage(self.content_area, self)  #
        self.current_page.pack(fill="both", expand=True)
    
    def back_to_events(self):
        """Return to events list"""
        self.show_page("My Events")
    
    def back_to_find_events(self):
        """Return to find events list"""
        self.show_page("Find Events")

    def logout(self):
        """Handle logout logic"""
        from src.auth import Auth  
        Auth.logout()
        from ui.home import HomePage 
        self.master.show_page(HomePage)
