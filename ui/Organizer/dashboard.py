import customtkinter as ctk
from PIL import Image
import os
from ui.Organizer.manage_events import ManageEventsPage

class OrganizerDashboard(ctk.CTkFrame):
    def __init__(self, master):
        # -- Dimiourgoume to vasiko frame tou dashboard -- #
        super().__init__(master)
        self.current_page = None
        
        # -- Dimiourgia tou sidebar (xriso fonto) -- #
        self.sidebar = ctk.CTkFrame(self, corner_radius=0, fg_color="#C8A165", width=250)
        self.sidebar.pack(side="left", fill="y", expand=False)
        self.sidebar.pack_propagate(False)

        # -- Fortosi kai emfanisi tou logo -- #
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

        # -- Menu epilogon -- #
        self.menu_items = [
            ("Homepage", "🏠"),
            ("Manage Events", "📋")
        ]

        self.menu_buttons = []
        # -- Dimiourgia koumpion gia kathe epilogi tou menu -- #
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

        # -- Koumpi Logout sto kato meros -- #
        self.logout_btn = ctk.CTkButton(
            self.sidebar,
            text="🚪 Logout",
            fg_color="#b38e58",
            text_color="white",
            hover_color="#96753d",
            command=self.logout
        )
        self.logout_btn.pack(side="bottom", pady=20, padx=10, fill="x")

        # -- Perioxi periexomenou (Mauro fonto) -- #
        self.content_area = ctk.CTkFrame(self, corner_radius=0, fg_color="black")
        self.content_area.pack(side="left", fill="both", expand=True)

        # -- Arxiki othoni kalwsorismatos -- #
        self.setup_welcome_frame()

    def setup_welcome_frame(self):
        """Dimiourgia tis arxikis othonis me to logo kai to minima kalwsorismatos"""
        # -- Dimiourgia tou frame kalwsorismatos -- #
        self.welcome_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.welcome_frame.place(relx=0.5, rely=0.5, anchor="center")

        # -- Fortosi tou logo gia tin arxiki othoni -- #
        welcome_image_path = os.path.join("assets", "logo_transparent2.png")
        welcome_image = Image.open(welcome_image_path)
        self.welcome_logo = ctk.CTkImage(
            light_image=welcome_image,
            dark_image=welcome_image,
            size=(400, 90)
        )

        # -- Emfanisi tou logo -- #
        self.welcome_logo_label = ctk.CTkLabel(
            self.welcome_frame,
            text="",
            image=self.welcome_logo
        )
        self.welcome_logo_label.pack(pady=(10, 5))

        # -- Minima kalwsorismatos -- #
        self.welcome_text = ctk.CTkLabel(
            self.welcome_frame,
            text="Welcome to EasyEvents Organizer Panel!\nUse the sidebar to manage your events!",
            font=ctk.CTkFont(size=20),
            text_color="white"
        )
        self.welcome_text.pack(pady=10)

    def clear_content(self):
        """Katharismos tis perioxi periexomenou"""
        if self.current_page is not None:
            self.current_page.destroy()
        self.welcome_frame.place_forget()

    def show_page(self, page_name):
        """Enallagi metaxi selidon"""
        self.clear_content()

        if page_name == "Homepage":
            # -- Allagí background se mauro gia tin arxiki -- #
            self.content_area.configure(fg_color="black")
            # -- Emfanisi tis arxikis selidas -- #
            self.welcome_frame.place(relx=0.5, rely=0.5, anchor="center")
            self.current_page = None
        elif page_name == "Manage Events":
            # -- Allagi background se leuko gia ta events -- #
            self.content_area.configure(fg_color="white")
            # -- Fortosi tis selidas diaxeirisis ekdiloseon -- #
            self.current_page = ManageEventsPage(self.content_area, self)
            self.current_page.pack(fill="both", expand=True)

    def logout(self):
        """Diaxeirisi tis diadikasias logout"""
        from src.auth import Auth  # Import here to avoid circular imports
        Auth.logout()
        from ui.home import HomePage  # Import here to avoid circular imports
        self.master.show_page(HomePage)
