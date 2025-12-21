"""Main entry point for Gradient Tool application."""
import tkinter as tk
from ui.main_window import MainWindow


def main():
    """Initialize and run the application."""
    root = tk.Tk()
    app = MainWindow(root)

    # Setup keyboard shortcuts
    root.bind('<Control-z>', lambda e: app.undo())
    root.bind('<Control-Z>', lambda e: app.undo())
    root.bind('<Control-y>', lambda e: app.redo())
    root.bind('<Control-Y>', lambda e: app.redo())
    root.bind('<Control-Shift-Z>', lambda e: app.redo())
    root.bind('<Control-Shift-z>', lambda e: app.redo())
    root.bind('<Control-s>', lambda e: app.export_image('png'))
    root.bind('<Control-S>', lambda e: app.export_image('png'))
    root.bind('<space>', lambda e: app.random_gradient())
    root.bind('r', lambda e: app.random_gradient())
    root.bind('R', lambda e: app.random_gradient())

    # Run application
    root.mainloop()


if __name__ == "__main__":
    main()
