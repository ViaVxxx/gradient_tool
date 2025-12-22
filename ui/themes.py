"""UI themes for the gradient tool."""
import tkinter as tk
from tkinter import ttk


class DarkTheme:
    """Dark theme based on DaisyUI dark theme colors."""
    
    # Convert oklch colors to approximate RGB hex values
    COLORS = {
        # Base colors
        'base_100': '#1f1f23',      # oklch(12% 0.042 264.695)
        'base_200': '#2a2a2f',      # oklch(20% 0.042 265.755)  
        'base_300': '#35353a',      # oklch(27% 0.041 260.031)
        'base_content': '#f4f4f5',  # oklch(96% 0.007 247.896)
        
        # Accent colors
        'primary': '#ff6b35',       # oklch(71% 0.194 13.428)
        'primary_content': '#2d1b0f', # oklch(27% 0.105 12.094)
        'secondary': '#d946ef',     # oklch(70% 0.183 293.541)
        'secondary_content': '#2d1b2f', # oklch(28% 0.141 291.089)
        'accent': '#a8a8aa',        # oklch(70% 0.015 286.067)
        'accent_content': '#1a1a1b', # oklch(14% 0.005 285.823)
        
        # Status colors
        'info': '#3b82f6',          # oklch(60% 0.126 221.723)
        'success': '#10b981',       # oklch(60% 0.118 184.704)
        'warning': '#f59e0b',       # oklch(68% 0.162 75.834)
        'error': '#ef4444',         # oklch(57% 0.245 27.325)
        
        # Neutral
        'neutral': '#52525b',       # oklch(44% 0.043 257.281)
        'neutral_content': '#fafafa', # oklch(98% 0.003 247.858)
    }

    @classmethod
    def apply_to_root(cls, root):
        """Apply dark theme to root window."""
        root.configure(bg=cls.COLORS['base_100'])
        
        # Configure ttk styles
        style = ttk.Style()
        
        # Set theme base - use clam for better color customization support
        # 'vista' and 'winnative' often ignore background colors for Entry/Combobox
        try:
            style.theme_use('clam')
        except:
            style.theme_use('default')

        # Configure global options
        root.option_add('*Background', cls.COLORS['base_100'])
        root.option_add('*Foreground', cls.COLORS['base_content'])
        root.option_add('*selectBackground', cls.COLORS['primary'])
        root.option_add('*selectForeground', cls.COLORS['primary_content'])
        root.option_add('*insertBackground', cls.COLORS['base_content'])
        
        # Configure Frame
        style.configure('TFrame', 
                       background=cls.COLORS['base_100'],
                       borderwidth=0)
        
        # Configure LabelFrame
        style.configure('TLabelframe', 
                       background=cls.COLORS['base_100'],
                       foreground=cls.COLORS['base_content'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=cls.COLORS['base_300'])
        style.configure('TLabelframe.Label',
                       background=cls.COLORS['base_100'],
                       foreground=cls.COLORS['primary'],
                       font=('TkDefaultFont', 9, 'bold'))
        
        # Configure Label
        style.configure('TLabel',
                       background=cls.COLORS['base_100'],
                       foreground=cls.COLORS['base_content'])
        
        # Configure Button
        style.configure('TButton',
                       background=cls.COLORS['base_200'],
                       foreground=cls.COLORS['base_content'],
                       borderwidth=1,
                       focuscolor='none',
                       relief='flat',
                       padding=(10, 5))
        style.map('TButton',
                 background=[('active', cls.COLORS['base_300']),
                           ('pressed', cls.COLORS['primary'])],
                 foreground=[('pressed', cls.COLORS['primary_content'])])
        
        # Configure Entry
        style.configure('TEntry',
                       fieldbackground=cls.COLORS['base_200'],
                       foreground=cls.COLORS['base_content'],
                       borderwidth=1,
                       insertcolor=cls.COLORS['base_content'],
                       selectbackground=cls.COLORS['primary'],
                       selectforeground=cls.COLORS['primary_content'])
        style.map('TEntry',
                 fieldbackground=[('focus', cls.COLORS['base_300'])],
                 bordercolor=[('focus', cls.COLORS['primary'])])
        
        # Configure Combobox
        style.configure('TCombobox',
                       fieldbackground=cls.COLORS['base_200'],
                       foreground=cls.COLORS['base_content'],
                       borderwidth=1,
                       selectbackground=cls.COLORS['primary'],
                       selectforeground=cls.COLORS['primary_content'],
                       arrowcolor=cls.COLORS['base_content'])
        style.map('TCombobox',
                 fieldbackground=[('readonly', cls.COLORS['base_200']),
                                ('focus', cls.COLORS['base_300'])],
                 bordercolor=[('focus', cls.COLORS['primary'])],
                 arrowcolor=[('active', cls.COLORS['primary'])])
        
        # Configure Combobox dropdown
        root.option_add('*TCombobox*Listbox.Background', cls.COLORS['base_200'])
        root.option_add('*TCombobox*Listbox.Foreground', cls.COLORS['base_content'])
        root.option_add('*TCombobox*Listbox.selectBackground', cls.COLORS['primary'])
        root.option_add('*TCombobox*Listbox.selectForeground', cls.COLORS['primary_content'])
        
        # Configure Scale
        style.configure('TScale',
                       background=cls.COLORS['base_100'],
                       troughcolor=cls.COLORS['base_200'],
                       borderwidth=0,
                       lightcolor=cls.COLORS['primary'],
                       darkcolor=cls.COLORS['primary'])
        
        # Configure Radiobutton
        style.configure('TRadiobutton',
                       background=cls.COLORS['base_100'],
                       foreground=cls.COLORS['base_content'],
                       focuscolor='none')
        
        # Configure Scrollbar with more aggressive styling
        style.configure('TScrollbar',
                       background=cls.COLORS['base_200'],
                       troughcolor=cls.COLORS['base_100'],
                       borderwidth=1,
                       relief='flat',
                       arrowcolor=cls.COLORS['base_content'],
                       darkcolor=cls.COLORS['base_300'],
                       lightcolor=cls.COLORS['base_200'])
        
        # Map scrollbar states
        style.map('TScrollbar',
                 background=[('active', cls.COLORS['base_300']),
                           ('pressed', cls.COLORS['primary'])],
                 arrowcolor=[('active', cls.COLORS['primary'])])
        
        # Try to configure scrollbar elements if available
        try:
            style.element_create('Vertical.Scrollbar.trough', 'from', 'clam')
            style.element_create('Vertical.Scrollbar.thumb', 'from', 'clam')
            style.element_create('Vertical.Scrollbar.uparrow', 'from', 'clam')
            style.element_create('Vertical.Scrollbar.downarrow', 'from', 'clam')
        except:
            pass  # Element creation might fail on some systems
        
        # Additional scrollbar styling options
        try:
            style.configure('Vertical.TScrollbar',
                           background=cls.COLORS['base_200'],
                           troughcolor=cls.COLORS['base_100'],
                           borderwidth=1,
                           arrowcolor=cls.COLORS['base_content'])
            style.configure('Horizontal.TScrollbar',
                           background=cls.COLORS['base_200'],
                           troughcolor=cls.COLORS['base_100'],
                           borderwidth=1,
                           arrowcolor=cls.COLORS['base_content'])
        except:
            pass

    @classmethod
    def configure_canvas(cls, canvas):
        """Configure canvas with dark theme."""
        canvas.configure(bg=cls.COLORS['base_200'],
                        highlightthickness=0)

    @classmethod
    def configure_listbox(cls, listbox):
        """Configure listbox with dark theme."""
        listbox.configure(bg=cls.COLORS['base_200'],
                         fg=cls.COLORS['base_content'],
                         selectbackground=cls.COLORS['primary'],
                         selectforeground=cls.COLORS['primary_content'],
                         borderwidth=0,
                         highlightthickness=0)


class LightTheme:
    """Light theme (default)."""
    
    @classmethod
    def apply_to_root(cls, root):
        """Apply light theme to root window."""
        # Reset to default theme
        style = ttk.Style()
        style.theme_use('default')

    @classmethod
    def configure_canvas(cls, canvas):
        """Configure canvas with light theme."""
        canvas.configure(bg='#2b2b2b',  # Keep dark for better gradient preview
                        highlightthickness=0)

    @classmethod
    def configure_listbox(cls, listbox):
        """Configure listbox with light theme."""
        listbox.configure(bg='white',
                         fg='black',
                         selectbackground='#0078d4',
                         selectforeground='white')


def apply_theme(root, theme_name='light'):
    """Apply theme to the application.
    
    Args:
        root: Root tkinter window
        theme_name: 'light' or 'dark'
    """
    if theme_name == 'dark':
        DarkTheme.apply_to_root(root)
        return DarkTheme
    else:
        LightTheme.apply_to_root(root)
        return LightTheme