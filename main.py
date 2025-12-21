"""Main entry point for Gradient Tool application."""
import tkinter as tk
from ui.main_window import MainWindow


import sys
import os

def setup_tkinter_env():
    """Set TCL/TK environment variables if needed."""
    try:
        import tkinter
        return
    except ImportError:
        pass

    # Try to find TCL/TK in standard Python locations
    base_prefix = getattr(sys, 'base_prefix', sys.prefix)
    tcl_path = os.path.join(base_prefix, 'tcl', 'tcl8.6')
    tk_path = os.path.join(base_prefix, 'tcl', 'tk8.6')

    if os.path.exists(tcl_path):
        os.environ['TCL_LIBRARY'] = tcl_path
    if os.path.exists(tk_path):
        os.environ['TK_LIBRARY'] = tk_path


def main():
    """Initialize and run the application."""
    setup_tkinter_env()
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
