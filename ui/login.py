import customtkinter as ctk
from PIL import Image
import os
from tkinter import messagebox
from src.auth import Auth

class LoginPage(ctk.CTkFrame):
    def __init__(self, master, is_organizer=False):
        super().__init__(master)
        self.is_organizer = is_organizer
        self.master = master  

        # -- Fortosi tou logo -- #
        image_path = os.path.join("assets", "logo_transparent.png")
        logo_image = Image.open(image_path)
        self.logo_ctk = ctk.CTkImage(light_image=logo_image, 
                                    dark_image=logo_image,
                                    size=(350, 80))  #fixed megethos

        # -- Left Panel (Gold xroma) -- #
        self.left_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#C8A165")
        self.left_frame.pack(side="left", fill="both", expand=True)

        # --  frame gia left content -- #
        self.left_center = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.left_center.place(relx=0.5, rely=0.5, anchor="center")

        # -- Logo -- #
        self.logo_label = ctk.CTkLabel(
            self.left_center,
            text="",  
            image=self.logo_ctk
        )
        self.logo_label.pack(pady=10)

        self.subtitle_label = ctk.CTkLabel(
            self.left_center,
            text="All your event planning needs\nin one place !\nStart now !",
            text_color="white",
            font=ctk.CTkFont(family="Helvetica", size=23)
        )
        self.subtitle_label.pack(pady=20)

        self.copyright_label = ctk.CTkLabel(
            self.left_frame,
            text="© CEID, 2025",
            text_color="white",
            font=ctk.CTkFont(family="Helvetica", size=12)
        )
        self.copyright_label.pack(side="bottom", pady=20)

        # -- Right Panel (White background) -- #
        self.right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="white")
        self.right_frame.pack(side="right", fill="both", expand=True)

        # --  frame gia right content -- #
        self.right_center = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.right_center.place(relx=0.5, rely=0.5, anchor="center")

        self.login_title = ctk.CTkLabel(
            self.right_center,
            text="Organizer Login" if self.is_organizer else "User Login",
            text_color="black",
            font=ctk.CTkFont(family="Helvetica", size=25, weight="bold")
        )
        self.login_title.pack(pady=(0, 10))

        self.login_subtitle = ctk.CTkLabel(
            self.right_center,
            text="Enter your organizer credentials" if self.is_organizer else "Enter your user credentials",
            text_color="black",
            font=ctk.CTkFont(family="Helvetica", size=18)
        )
        self.login_subtitle.pack(pady=(0, 30))

        self.username_entry = ctk.CTkEntry(
            self.right_center,
            placeholder_text="Username",
            width=300,
            height=40,
            border_width=1,
            corner_radius=8
        )
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self.right_center,
            placeholder_text="Password",
            width=300,
            height=40,
            border_width=1,
            corner_radius=8,
            show="*"
        )
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(
            self.right_center,
            text="Login  →",
            fg_color="#C8A165",
            text_color="black",
            hover_color="#b38e58",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            width=300,
            height=40,
            corner_radius=8,
            command=self.on_login_clicked
        )
        self.login_button.pack(pady=(30, 0))

    def on_login_clicked(self):
     
        from ui.user.dashboard import UserDashboard
        from ui.Organizer.dashboard import OrganizerDashboard

        username = self.username_entry.get()
        password = self.password_entry.get()

        # Attempt login
        if Auth.login(username, password, self.is_organizer):
            # Remove login page
            self.pack_forget()

            # Show the appropriate dashboard
            if self.is_organizer:
                dash = OrganizerDashboard(self.master)
            else:
                dash = UserDashboard(self.master)

            dash.pack(fill="both", expand=True)

