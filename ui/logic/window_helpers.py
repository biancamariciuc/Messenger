def center_window(window, width, height):
    """
    Function that center the main window in the center of the computer screen

    This function calculates the appropriate X and Y coordinates based on the
    user's screen resolution to place the window exactly in the middle.

    """

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")

def clear_window(window):
        """Removes all widgets from a given window or frame"""
        for widget in window.winfo_children():
            widget.destroy()

def center_emoji_window(child_window, parent_window, width, height):
    """
    Function that center picker window in the center of the main window.

    Instead of using screen coordinates, this calculates the position based on
    where the main application window is currently located.
    """

    main_x = parent_window.winfo_x()
    main_y = parent_window.winfo_y()
    main_w = parent_window.winfo_width()
    main_h = parent_window.winfo_height()

    x = main_x + (main_w // 2) - (width // 2)
    y = main_y + (main_h // 2) - (height // 2)

    child_window.geometry(f"{width}x{height}+{x}+{y}")