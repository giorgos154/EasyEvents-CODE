# -- System imports -- #
import os
import sys

sys.dont_write_bytecode = True  

# -- Add project root and src directory to Python path -- #
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
for path in [project_root, src_path]:
    if path not in sys.path:
        sys.path.insert(0, path)

# -- Third-party imports -- #
import customtkinter as ctk

# -- Local imports -- #
from main import setup_ctk, APP_TITLE, APP_SIZE
from ui.home import HomePage

# -- Initialize global settings -- #
setup_ctk()

# -- Main App Window -- #
class EasyEventsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_SIZE)
        self.resizable(False, False)

        # -- Initialize first page (Home) -- #
        self.show_page(HomePage)

    def show_page(self, page_class, **kwargs):
        # Clear current widgets
        for widget in self.winfo_children():
            widget.destroy()
            
        # Create and show new page
        page = page_class(self, **kwargs)
        page.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = EasyEventsApp()
    app.mainloop()
