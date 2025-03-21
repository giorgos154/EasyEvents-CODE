import customtkinter as ctk
from PIL import Image
import os
from ui.user.findevents import FindEventsPage
from ui.user.myevents import MyEventsPage
from ui.user.myprofile import MyProfilePage
from ui.user.points import PointsPage
from ui.user.rewards import RewardsPage
from ui.user.rate_events import RateEventsPage

class UserDashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.current_page = None

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

        # Center frame for welcome content
        self.welcome_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.welcome_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Load and display welcome logo
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

    def show_page(self, page_name):
        """Update content area based on selected menu item"""
        # Hide welcome frame
        self.welcome_frame.place_forget()

        # Clear current page if exists
        if self.current_page is not None:
            self.current_page.destroy()

        # Show selected page
        if page_name == "Homepage":
            self.welcome_frame.place(relx=0.5, rely=0.5, anchor="center")
            self.current_page = None
        elif page_name == "Find Events":
            self.current_page = FindEventsPage(self.content_area)
            self.current_page.pack(fill="both", expand=True)
        elif page_name == "My Events":
            self.current_page = MyEventsPage(self.content_area)
            self.current_page.pack(fill="both", expand=True)
        elif page_name == "Rate Events":
            self.current_page = RateEventsPage(self.content_area)
            self.current_page.pack(fill="both", expand=True)
            self.current_page.pack(fill="both", expand=True)
        elif page_name == "My Profile":
            self.current_page = MyProfilePage(self.content_area)
            self.current_page.pack(fill="both", expand=True)
        elif page_name == "Points & Rewards":
            self.current_page = PointsPage(self.content_area)
            self.current_page.pack(fill="both", expand=True)

    def show_rewards(self):
        # Switch to rewards page
        if self.current_page is not None:
            self.current_page.destroy()
        self.current_page = RewardsPage(self.content_area)
        self.current_page.pack(fill="both", expand=True)
    
    def back_to_points(self):
        # Return to points page
        if self.current_page is not None:
            self.current_page.destroy()
        self.current_page = PointsPage(self.content_area)
        self.current_page.pack(fill="both", expand=True)
                           
                           
    def logout(self):
        """Handle logout logic"""
        print("Logging out...")
