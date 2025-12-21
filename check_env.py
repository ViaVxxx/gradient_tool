import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")

try:
    import tkinter
    print(f"Tkinter found: {tkinter}")
    print(f"Tkinter file: {tkinter.__file__}")
    import _tkinter
    print(f"_tkinter found: {_tkinter}")
except ImportError as e:
    print(f"Error importing tkinter: {e}")

try:
    import PyInstaller
    print(f"PyInstaller version: {PyInstaller.__version__}")
except ImportError:
    print("PyInstaller not found")
