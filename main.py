import customtkinter as ctk

# ---------------------------
# Global App Configuration
# ---------------------------
APP_TITLE = "EasyEvents"
APP_SIZE = "1000x600"
DEFAULT_THEME = "Light"  # Options: "Light", "Dark", "System"
DEFAULT_COLOR_THEME = "blue"  # Options: "blue", "green", "dark-blue"

# Initialize CustomTkinter Settings
def setup_ctk():
    ctk.set_appearance_mode(DEFAULT_THEME)
    ctk.set_default_color_theme(DEFAULT_COLOR_THEME)
