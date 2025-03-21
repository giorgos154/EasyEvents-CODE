import customtkinter as ctk
from main import setup_ctk, APP_TITLE, APP_SIZE
from ui.home import HomePage
from ui.user.dashboard import UserDashboard

# Initialize global settings
setup_ctk()

# Main App Window
class EasyEventsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_SIZE)
        self.resizable(False, False)

        # Load the first page (Home)
        self.show_page(HomePage)

    def show_page(self, page_class):
        """Switch to a new page."""
        for widget in self.winfo_children():
            widget.destroy()  # Remove old page content

        page = page_class(self)
        page.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = EasyEventsApp()
    app.mainloop()
