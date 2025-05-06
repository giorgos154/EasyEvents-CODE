# -- Imports -- #
from ui.login import LoginPage  # Import moved to top
import customtkinter as ctk
from PIL import Image
import os

class HomePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

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
            text="All your event planning needs\nin one place !\n\nStart now !",
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

        self.role_label = ctk.CTkLabel(
            self.right_center,
            text="Choose your role",
            text_color="black",
            font=ctk.CTkFont(family="Helvetica", size=20, weight="bold")
        )
        self.role_label.pack(pady=(0, 30))

        self.user_login_btn = ctk.CTkButton(
            self.right_center,
            text="User Login  →",
            fg_color="#C8A165",
            text_color="black",
            hover_color="#b38e58",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            width=300,
            height=40,
            corner_radius=8,
            command=lambda: master.show_page(LoginPage, is_organizer=False)
        )
        self.user_login_btn.pack(pady=10)

        self.organiser_login_btn = ctk.CTkButton(
            self.right_center,
            text="Organiser Login  →",
            fg_color="#C8A165",
            text_color="black",
            hover_color="#b38e58",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            width=300,
            height=40,
            corner_radius=8,
            command=lambda: master.show_page(LoginPage, is_organizer=True)
        )
        self.organiser_login_btn.pack(pady=10)
