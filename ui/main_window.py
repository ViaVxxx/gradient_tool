"""Main application window."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import random
import os

from core.gradient_engine import GradientEngine, GradientType
from core.color_utils import Color, ColorStop
from core.presets import PresetLibrary
from core.effects import Effects
from utils.export import ExportManager
from utils.history import HistoryManager
from utils.favorites import FavoritesManager
from ui.themes import apply_theme, DarkTheme, LightTheme


class GradientState:
    """Current gradient state for history management."""

    def __init__(self):
        self.gradient_type = GradientType.LINEAR
        self.angle = 90
        self.stops = [
            ColorStop(0.0, Color.from_hex("#667EEA")),
            ColorStop(1.0, Color.from_hex("#764BA2"))
        ]
        self.noise_intensity = 0.0
        self.vignette_intensity = 0.0
        self.width = 800
        self.height = 600


class MainWindow:
    """Main application window."""

    def __init__(self, root):
        """Initialize main window."""
        self.root = root
        self.root.title("Gradient Tool - 渐变色图像生成器")
        self.root.geometry("1400x1000")  # 增加宽度从1200到1400

        # Initialize components
        self.engine = GradientEngine(800, 600)
        self.preset_library = PresetLibrary()
        self.export_manager = ExportManager()
        self.history = HistoryManager()
        self.favorites_manager = FavoritesManager()

        # Current state
        self.state = GradientState()
        self.current_image = None
        self.tk_image = None
        self.selected_stop_index = 0
        
        # 添加防抖机制
        self.render_timer = None
        self.render_delay = 100  # 100ms 延迟
        
        # 主题设置
        self.current_theme = 'dark'  # 默认使用深色主题
        self.theme_class = apply_theme(self.root, self.current_theme)
        
        # 预设分辨率
        self.preset_resolutions = [
            ("800x600", 800, 600),
            ("1024x768", 1024, 768),
            ("1280x720 (HD)", 1280, 720),
            ("1920x1080 (FHD)", 1920, 1080),
            ("2560x1440 (2K)", 2560, 1440),
            ("3840x2160 (4K)", 3840, 2160),
            ("1080x1920 (手机竖屏)", 1080, 1920),
            ("1242x2208 (iPhone)", 1242, 2208),
            ("正方形 1080x1080", 1080, 1080),
            ("自定义", 0, 0)
        ]

        # Setup UI
        self._setup_ui()

        # Force initial scrollbar theme
        self._force_scrollbar_theme_update()
        
        # Force theme update for all widgets
        self._force_theme_update()

        # Initial render
        self.render_gradient()
        self.history.add_state(self.state)

    def _setup_ui(self):
        """Setup the user interface."""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel - Gradient Design (280px)
        left_panel = ttk.Frame(main_container, width=280)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        left_panel.pack_propagate(False)

        # Right panel - Output Settings (260px) - 先创建右侧面板
        right_panel = ttk.Frame(main_container, width=260)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(8, 0))
        right_panel.pack_propagate(False)

        # Middle panel - Preview (expandable) - 最后创建中间面板，自动填充剩余空间
        middle_panel = ttk.Frame(main_container)
        middle_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)

        # Setup panels
        self._setup_basic_controls(left_panel)
        self._setup_preview(middle_panel)
        self._setup_advanced_controls(right_panel)

    def _setup_basic_controls(self, parent):
        """Setup gradient control panel (left side)."""
        # Title
        title = ttk.Label(parent, text="渐变设计", font=("Arial", 12, "bold"))
        title.pack(pady=(0, 10))

        # Gradient Type
        type_frame = ttk.LabelFrame(parent, text="渐变类型", padding=8)
        type_frame.pack(fill=tk.X, pady=(0, 8))

        self.gradient_type_var = tk.StringVar(value=GradientType.LINEAR)

        ttk.Radiobutton(type_frame, text="线性渐变", variable=self.gradient_type_var,
                       value=GradientType.LINEAR, command=self.on_type_change).pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="径向渐变", variable=self.gradient_type_var,
                       value=GradientType.RADIAL, command=self.on_type_change).pack(anchor=tk.W)

        # Angle control (for linear gradient)
        self.angle_frame = ttk.LabelFrame(parent, text="角度", padding=8)
        self.angle_frame.pack(fill=tk.X, pady=(0, 8))

        self.angle_var = tk.IntVar(value=90)
        angle_scale = ttk.Scale(self.angle_frame, from_=0, to=360, variable=self.angle_var,
                               orient=tk.HORIZONTAL, command=self.on_angle_change)
        angle_scale.pack(fill=tk.X)

        angle_label = ttk.Label(self.angle_frame, textvariable=self.angle_var)
        angle_label.pack()

        # Color Stops
        stops_frame = ttk.LabelFrame(parent, text="色标编辑", padding=8)
        stops_frame.pack(fill=tk.X, pady=(0, 8))

        # Stop selector
        stop_select_frame = ttk.Frame(stops_frame)
        stop_select_frame.pack(fill=tk.X, pady=(0, 5))

        self.stop_var = tk.StringVar()
        self.stop_combo = ttk.Combobox(stop_select_frame, textvariable=self.stop_var,
                                       state='readonly')
        self.stop_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.stop_combo.bind('<<ComboboxSelected>>', self.on_stop_select)

        # Add/Remove stop buttons
        ttk.Button(stop_select_frame, text="+", width=3,
                  command=self.add_color_stop).pack(side=tk.RIGHT, padx=(2, 0))
        ttk.Button(stop_select_frame, text="-", width=3,
                  command=self.remove_color_stop).pack(side=tk.RIGHT, padx=2)

        # Color picker
        color_frame = ttk.Frame(stops_frame)
        color_frame.pack(fill=tk.X, pady=5)

        ttk.Label(color_frame, text="颜色:").pack(side=tk.LEFT)
        self.color_display = tk.Canvas(color_frame, width=30, height=30, bg="#667EEA", highlightthickness=0)
        self.color_display.pack(side=tk.LEFT, padx=5)

        ttk.Button(color_frame, text="选择",
                  command=self.choose_color).pack(side=tk.LEFT)

        # Hex input
        hex_frame = ttk.Frame(stops_frame)
        hex_frame.pack(fill=tk.X)

        ttk.Label(hex_frame, text="HEX:").pack(side=tk.LEFT)
        self.hex_var = tk.StringVar(value="#667EEA")
        self.hex_entry = ttk.Entry(hex_frame, textvariable=self.hex_var, width=10)
        self.hex_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(hex_frame, text="应用",
                  command=self.apply_hex_color).pack(side=tk.LEFT)

        # Effects
        effects_frame = ttk.LabelFrame(parent, text="效果", padding=8)
        effects_frame.pack(fill=tk.X, pady=(0, 8))

        # Noise
        ttk.Label(effects_frame, text="噪点强度:").pack(anchor=tk.W)
        self.noise_var = tk.DoubleVar(value=0.0)
        noise_scale = ttk.Scale(effects_frame, from_=0, to=0.3, variable=self.noise_var,
                               orient=tk.HORIZONTAL, command=self.on_effect_change)
        noise_scale.pack(fill=tk.X, pady=(0, 5))

        # Vignette
        ttk.Label(effects_frame, text="晕影强度:").pack(anchor=tk.W)
        self.vignette_var = tk.DoubleVar(value=0.0)
        vignette_scale = ttk.Scale(effects_frame, from_=0, to=1.0, variable=self.vignette_var,
                                   orient=tk.HORIZONTAL, command=self.on_effect_change)
        vignette_scale.pack(fill=tk.X)

        # Presets
        presets_frame = ttk.LabelFrame(parent, text="预设", padding=8)
        presets_frame.pack(fill=tk.BOTH, expand=True)

        # Category selector
        category_frame = ttk.Frame(presets_frame)
        category_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(category_frame, text="分类:").pack(side=tk.LEFT)
        self.category_var = tk.StringVar(value="All")
        categories = ["All"] + self.preset_library.get_categories()
        category_combo = ttk.Combobox(category_frame, textvariable=self.category_var,
                                     values=categories, state='readonly', width=12)
        category_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        category_combo.bind('<<ComboboxSelected>>', self.on_category_change)

        # Preset list
        list_frame = ttk.Frame(presets_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.preset_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.preset_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.preset_listbox.bind('<<ListboxSelect>>', self.on_preset_select)

        scrollbar.config(command=self.preset_listbox.yview)
        
        # Apply theme to listbox
        self.theme_class.configure_listbox(self.preset_listbox)

        # Load presets
        self.update_preset_list()

    def _setup_advanced_controls(self, parent):
        """Setup output control panel (right side)."""
        # Use a simple frame without scrolling for the main panel
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Now use main_frame as the parent for all controls
        parent = main_frame

        # Title with padding
        title = ttk.Label(parent, text="输出设置", font=("Arial", 12, "bold"))
        title.pack(pady=(0, 10))

        # Resolution control
        resolution_frame = ttk.LabelFrame(parent, text="分辨率", padding=8)
        resolution_frame.pack(fill=tk.X, pady=(0, 8))

        # Preset resolution selector
        ttk.Label(resolution_frame, text="预设:").pack(anchor=tk.W)
        self.resolution_var = tk.StringVar(value="800x600")
        resolution_values = [res[0] for res in self.preset_resolutions]
        self.resolution_combo = ttk.Combobox(resolution_frame, textvariable=self.resolution_var,
                                           values=resolution_values, state='readonly')
        self.resolution_combo.pack(fill=tk.X, pady=(2, 5))
        self.resolution_combo.bind('<<ComboboxSelected>>', self.on_resolution_preset_change)

        # Custom resolution inputs
        custom_frame = ttk.Frame(resolution_frame)
        custom_frame.pack(fill=tk.X)

        size_frame1 = ttk.Frame(custom_frame)
        size_frame1.pack(fill=tk.X, pady=1)
        ttk.Label(size_frame1, text="宽度:").pack(side=tk.LEFT)
        self.width_var = tk.IntVar(value=800)
        self.width_entry = ttk.Entry(size_frame1, textvariable=self.width_var, width=8)
        self.width_entry.pack(side=tk.RIGHT)
        self.width_entry.bind('<KeyRelease>', self.on_custom_resolution_change)

        size_frame2 = ttk.Frame(custom_frame)
        size_frame2.pack(fill=tk.X, pady=1)
        ttk.Label(size_frame2, text="高度:").pack(side=tk.LEFT)
        self.height_var = tk.IntVar(value=600)
        self.height_entry = ttk.Entry(size_frame2, textvariable=self.height_var, width=8)
        self.height_entry.pack(side=tk.RIGHT)
        self.height_entry.bind('<KeyRelease>', self.on_custom_resolution_change)

        ttk.Button(custom_frame, text="应用", command=self.apply_custom_resolution).pack(pady=(5, 0))

        # Favorites section - 增加高度并添加滚动条
        favorites_frame = ttk.LabelFrame(parent, text="已收藏图片", padding=8)
        favorites_frame.pack(fill=tk.X, pady=(0, 8))

        # Favorites toolbar
        fav_toolbar = ttk.Frame(favorites_frame)
        fav_toolbar.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(fav_toolbar, text="⭐ 收藏", 
                  command=self.add_to_favorites).pack(side=tk.LEFT)
        ttk.Button(fav_toolbar, text="🗑️", 
                  command=self.remove_selected_favorites).pack(side=tk.LEFT, padx=(5, 0))
        ttk.Button(fav_toolbar, text="📤", 
                  command=self.export_selected_favorites).pack(side=tk.RIGHT)

        # Favorites grid - 增加高度到200px并确保滚动条可见
        fav_container = ttk.Frame(favorites_frame)
        fav_container.pack(fill=tk.X, pady=(0, 5))
        
        self.favorites_canvas = tk.Canvas(fav_container, height=250, highlightthickness=0)  # 增加到250px
        self.fav_scrollbar = ttk.Scrollbar(fav_container, orient="vertical", command=self.favorites_canvas.yview)
        self.favorites_scrollable_frame = ttk.Frame(self.favorites_canvas)

        # Apply theme to favorites canvas
        if self.current_theme == 'dark':
            self.favorites_canvas.configure(bg=DarkTheme.COLORS['base_200'])
        else:
            self.favorites_canvas.configure(bg='#f0f0f0')

        # Configure favorites scrolling
        def update_fav_scroll_region(event):
            self.favorites_canvas.configure(scrollregion=self.favorites_canvas.bbox("all"))
        
        self.favorites_scrollable_frame.bind("<Configure>", update_fav_scroll_region)
        
        # Create window for favorites content
        fav_canvas_window = self.favorites_canvas.create_window((0, 0), window=self.favorites_scrollable_frame, anchor="nw")
        
        # Update favorites frame width when canvas resizes
        def update_fav_frame_width(event):
            canvas_width = event.width - 20  # Account for scrollbar width
            self.favorites_canvas.itemconfig(fav_canvas_window, width=canvas_width)
        
        self.favorites_canvas.bind('<Configure>', update_fav_frame_width)
        self.favorites_canvas.configure(yscrollcommand=self.fav_scrollbar.set)

        # Add mouse wheel scrolling to favorites
        def _on_fav_mousewheel(event):
            self.favorites_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.favorites_canvas.bind("<MouseWheel>", _on_fav_mousewheel)
        self.favorites_scrollable_frame.bind("<MouseWheel>", _on_fav_mousewheel)
        
        # Also bind to the favorites frame and container so scrolling works when hovering over the area
        favorites_frame.bind("<MouseWheel>", _on_fav_mousewheel)
        fav_container.bind("<MouseWheel>", _on_fav_mousewheel)

        # Pack favorites canvas and scrollbar
        self.favorites_canvas.pack(side="left", fill="both", expand=True)
        self.fav_scrollbar.pack(side="right", fill="y")

        # Selected favorites tracking
        self.selected_favorites = set()
        self.favorite_widgets = {}

        # Load existing favorites
        self.refresh_favorites_display()

        # Action buttons
        button_frame = ttk.LabelFrame(parent, text="操作", padding=8)
        button_frame.pack(fill=tk.X, pady=(0, 8))

        ttk.Button(button_frame, text="🎲 随机生成",
                  command=self.random_gradient).pack(fill=tk.X, pady=2)
        
        # Export section
        export_label = ttk.Label(button_frame, text="导出图像:", font=("Arial", 9, "bold"))
        export_label.pack(anchor=tk.W, pady=(10, 2))
        
        ttk.Button(button_frame, text="📄 导出 PNG",
                  command=lambda: self.export_image('png')).pack(fill=tk.X, pady=1)
        ttk.Button(button_frame, text="🖼️ 导出 JPG",
                  command=lambda: self.export_image('jpg')).pack(fill=tk.X, pady=1)

        # History section
        history_label = ttk.Label(button_frame, text="历史记录:", font=("Arial", 9, "bold"))
        history_label.pack(anchor=tk.W, pady=(10, 2))
        
        # Undo/Redo buttons
        undo_frame = ttk.Frame(button_frame)
        undo_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(undo_frame, text="↶ 撤销",
                  command=self.undo).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        ttk.Button(undo_frame, text="↷ 重做",
                  command=self.redo).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        # Quick tips
        tips_frame = ttk.LabelFrame(parent, text="快捷键", padding=8)
        tips_frame.pack(fill=tk.X, pady=(0, 8))

        tips_text = """Ctrl+S - 导出PNG
Space/R - 随机生成
Ctrl+Z - 撤销
Ctrl+Y - 重做"""
        
        tips_label = ttk.Label(tips_frame, text=tips_text, font=("Arial", 8), 
                              justify=tk.LEFT)
        tips_label.pack(anchor=tk.W)

        # Theme toggle
        theme_frame = ttk.Frame(parent)
        theme_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.theme_button = ttk.Button(theme_frame, text="🌙 深色" if self.current_theme == 'light' else "☀️ 浅色",
                  command=self.toggle_theme)
        self.theme_button.pack(fill=tk.X)

    def add_to_favorites(self):
        """Add current gradient to favorites."""
        if self.current_image is None:
            messagebox.showwarning("警告", "没有可收藏的图像")
            return

        try:
            favorite_id = self.favorites_manager.add_favorite(self.current_image, self.state)
            self.refresh_favorites_display()
            messagebox.showinfo("成功", "已添加到收藏")
        except Exception as e:
            messagebox.showerror("错误", f"收藏失败: {e}")

    def remove_selected_favorites(self):
        """Remove selected favorites."""
        if not self.selected_favorites:
            messagebox.showwarning("警告", "请先选择要删除的收藏")
            return

        if messagebox.askyesno("确认", f"确定要删除 {len(self.selected_favorites)} 个收藏吗？"):
            for fav_id in list(self.selected_favorites):
                self.favorites_manager.remove_favorite(fav_id)
            
            self.selected_favorites.clear()
            self.refresh_favorites_display()
            messagebox.showinfo("成功", "已删除选中的收藏")

    def export_selected_favorites(self):
        """Export selected favorites."""
        if not self.selected_favorites:
            messagebox.showwarning("警告", "请先选择要导出的收藏")
            return

        # Ask for export directory
        export_dir = filedialog.askdirectory(title="选择导出目录")
        if not export_dir:
            return

        # Ask for format
        format_choice = messagebox.askyesnocancel("选择格式", "选择导出格式:\n是 = PNG\n否 = JPG\n取消 = 取消导出")
        if format_choice is None:
            return
        
        format_type = 'png' if format_choice else 'jpg'

        try:
            exported_files = self.favorites_manager.export_favorites(
                list(self.selected_favorites), export_dir, format_type
            )
            
            if exported_files:
                messagebox.showinfo("成功", f"已导出 {len(exported_files)} 个文件到:\n{export_dir}")
            else:
                messagebox.showwarning("警告", "没有文件被导出")
                
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {e}")

    def refresh_favorites_display(self):
        """Refresh the favorites display grid."""
        # Clear existing widgets
        for widget in self.favorites_scrollable_frame.winfo_children():
            widget.destroy()
        
        self.favorite_widgets.clear()

        favorites = self.favorites_manager.get_favorites()
        if not favorites:
            # Show empty message
            empty_label = ttk.Label(self.favorites_scrollable_frame, 
                                   text="暂无收藏\n点击 ⭐ 收藏当前图片", 
                                   justify=tk.CENTER)
            empty_label.pack(pady=20)
            return

        # Create grid of thumbnails (3 columns)
        cols = 3
        for i, fav in enumerate(favorites):
            row = i // cols
            col = i % cols

            # Create frame for each favorite
            fav_frame = ttk.Frame(self.favorites_scrollable_frame)
            fav_frame.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

            # Load thumbnail
            thumbnail_path = self.favorites_manager.get_thumbnail_path(fav['id'])
            if thumbnail_path and os.path.exists(thumbnail_path):
                try:
                    thumb_image = Image.open(thumbnail_path)
                    thumb_image = thumb_image.resize((60, 60), Image.LANCZOS)
                    thumb_photo = ImageTk.PhotoImage(thumb_image)

                    # Create clickable thumbnail
                    thumb_label = ttk.Label(fav_frame, image=thumb_photo)
                    thumb_label.image = thumb_photo  # Keep reference
                    thumb_label.pack()

                    # Bind click events
                    def on_click(event, fav_id=fav['id']):
                        self.toggle_favorite_selection(fav_id)

                    def on_double_click(event, fav_data=fav):
                        self.load_favorite(fav_data)

                    thumb_label.bind("<Button-1>", on_click)
                    thumb_label.bind("<Double-Button-1>", on_double_click)

                    # Name label
                    name_label = ttk.Label(fav_frame, text=fav['name'][:8] + "..." if len(fav['name']) > 8 else fav['name'], 
                                         font=("Arial", 8))
                    name_label.pack()

                    # Store widget reference
                    self.favorite_widgets[fav['id']] = thumb_label

                except Exception as e:
                    # Show error placeholder
                    error_label = ttk.Label(fav_frame, text="加载失败")
                    error_label.pack()

        # Configure grid weights
        for i in range(cols):
            self.favorites_scrollable_frame.columnconfigure(i, weight=1)

    def toggle_favorite_selection(self, fav_id):
        """Toggle selection of a favorite."""
        if fav_id in self.selected_favorites:
            self.selected_favorites.remove(fav_id)
            # Update visual state - normal border
            if fav_id in self.favorite_widgets:
                self.favorite_widgets[fav_id].config(relief="raised", borderwidth=2)
        else:
            self.selected_favorites.add(fav_id)
            # Update visual state - selected border
            if fav_id in self.favorite_widgets:
                self.favorite_widgets[fav_id].config(relief="solid", borderwidth=3)

    def load_favorite(self, fav_data):
        """Load a favorite gradient into the current state."""
        try:
            # Restore gradient state
            from core.color_utils import Color, ColorStop
            
            self.state.gradient_type = fav_data['gradient_type']
            self.state.angle = fav_data['angle']
            self.state.noise_intensity = fav_data['noise_intensity']
            self.state.vignette_intensity = fav_data['vignette_intensity']
            self.state.width = fav_data['width']
            self.state.height = fav_data['height']
            
            # Restore color stops
            self.state.stops = []
            for pos, hex_color in fav_data['stops']:
                color = Color.from_hex(hex_color)
                self.state.stops.append(ColorStop(pos, color))

            # Update UI
            self.gradient_type_var.set(self.state.gradient_type)
            self.angle_var.set(self.state.angle)
            self.noise_var.set(self.state.noise_intensity)
            self.vignette_var.set(self.state.vignette_intensity)
            self.width_var.set(self.state.width)
            self.height_var.set(self.state.height)
            
            # Update resolution display
            for name, width, height in self.preset_resolutions:
                if width == self.state.width and height == self.state.height:
                    self.resolution_var.set(name)
                    break
            else:
                self.resolution_var.set("自定义")

            self.update_stop_combo()
            self.on_type_change()
            
            # Update engine and render
            self.engine = GradientEngine(self.state.width, self.state.height)
            self.save_state()
            self.render_gradient()
            
            messagebox.showinfo("成功", f"已加载收藏: {fav_data['name']}")
            
        except Exception as e:
            messagebox.showerror("错误", f"加载收藏失败: {e}")

    def _force_theme_update(self):
        """Force theme update for all widgets."""
        def update_widget_theme(widget):
            """Recursively update theme for widget and its children."""
            try:
                # Get widget class name
                widget_class = widget.winfo_class()
                
                if widget_class in ['TEntry', 'Entry']:
                    if self.current_theme == 'dark':
                        widget.configure(
                            bg=DarkTheme.COLORS['base_200'],
                            fg=DarkTheme.COLORS['base_content'],
                            insertbackground=DarkTheme.COLORS['base_content'],
                            selectbackground=DarkTheme.COLORS['primary'],
                            selectforeground=DarkTheme.COLORS['primary_content']
                        )
                elif widget_class in ['TButton', 'Button']:
                    if self.current_theme == 'dark':
                        widget.configure(
                            bg=DarkTheme.COLORS['base_200'],
                            fg=DarkTheme.COLORS['base_content'],
                            activebackground=DarkTheme.COLORS['base_300'],
                            activeforeground=DarkTheme.COLORS['base_content']
                        )
                elif widget_class in ['TCombobox', 'Combobox']:
                    if self.current_theme == 'dark':
                        widget.configure(
                            fieldbackground=DarkTheme.COLORS['base_200'],
                            foreground=DarkTheme.COLORS['base_content'],
                            selectbackground=DarkTheme.COLORS['primary']
                        )
                elif widget_class in ['TLabel', 'Label']:
                    if self.current_theme == 'dark':
                        widget.configure(
                            background=DarkTheme.COLORS['base_100'],
                            foreground=DarkTheme.COLORS['base_content']
                        )
                elif widget_class in ['TFrame', 'Frame']:
                    if self.current_theme == 'dark':
                        widget.configure(background=DarkTheme.COLORS['base_100'])
                
                # Recursively update children
                for child in widget.winfo_children():
                    update_widget_theme(child)
                    
            except Exception as e:
                # Ignore errors for widgets that don't support certain options
                pass
        
        # Update all widgets starting from root
        update_widget_theme(self.root)

    def _force_scrollbar_theme_update(self):
        """Force update scrollbar themes by recreating them."""
        # This is a workaround for Windows where ttk.Scrollbar theming doesn't always work
        try:
            # Force style update
            style = ttk.Style()
            if self.current_theme == 'dark':
                # Apply dark scrollbar colors more aggressively
                style.configure('TScrollbar',
                               background=DarkTheme.COLORS['base_200'],
                               troughcolor=DarkTheme.COLORS['base_100'],
                               borderwidth=1,
                               relief='flat',
                               arrowcolor=DarkTheme.COLORS['base_content'])
                
                # Try to force update existing scrollbars
                for widget in [self.fav_scrollbar]:
                    if hasattr(self, 'fav_scrollbar'):
                        widget.configure(style='TScrollbar')
            else:
                # Reset to default for light theme
                style.configure('TScrollbar')
        except Exception as e:
            print(f"Scrollbar theme update failed: {e}")

    def toggle_theme(self):
        """Toggle between light and dark theme."""
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.theme_class = apply_theme(self.root, self.current_theme)
        
        # Force scrollbar theme update
        self._force_scrollbar_theme_update()
        
        # Force theme update for all widgets
        self._force_theme_update()
        
        # Reapply theme to specific widgets
        self.theme_class.configure_canvas(self.canvas)
        self.theme_class.configure_listbox(self.preset_listbox)
        
        # Update right panel canvas (find it in the right panel)
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):  # main_container
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Frame) and child.winfo_width() == 260:  # right panel
                        for canvas_widget in child.winfo_children():
                            if isinstance(canvas_widget, tk.Canvas) and canvas_widget != self.favorites_canvas:
                                if self.current_theme == 'dark':
                                    canvas_widget.configure(bg=DarkTheme.COLORS['base_100'])
                                else:
                                    canvas_widget.configure(bg='white')
        
        # Update favorites canvas
        if self.current_theme == 'dark':
            self.favorites_canvas.configure(bg=DarkTheme.COLORS['base_200'])
        else:
            self.favorites_canvas.configure(bg='#f0f0f0')
        
        # Update theme button text
        new_text = "🌙 深色" if self.current_theme == 'light' else "☀️ 浅色"
        self.theme_button.configure(text=new_text)

    def _setup_preview(self, parent):
        """Setup preview canvas."""
        preview_frame = ttk.LabelFrame(parent, text="预览", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for image preview
        self.canvas = tk.Canvas(preview_frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Apply theme to canvas
        self.theme_class.configure_canvas(self.canvas)

    def update_stop_combo(self):
        """Update color stop combobox."""
        stop_labels = [f"Stop {i+1} ({s.position:.0%})" for i, s in enumerate(self.state.stops)]
        self.stop_combo['values'] = stop_labels

        if stop_labels:
            self.stop_combo.current(self.selected_stop_index)

    def on_stop_select(self, event):
        """Handle stop selection."""
        self.selected_stop_index = self.stop_combo.current()

        if 0 <= self.selected_stop_index < len(self.state.stops):
            stop = self.state.stops[self.selected_stop_index]
            hex_color = stop.color.to_hex()
            self.hex_var.set(hex_color)
            self.color_display.config(bg=hex_color)

    def add_color_stop(self):
        """Add a new color stop."""
        if len(self.state.stops) >= 20:
            messagebox.showwarning("警告", "最多支持20个色标")
            return

        # Add at middle position
        new_stop = ColorStop(0.5, Color(255, 255, 255))
        self.state.stops.append(new_stop)
        self.state.stops.sort(key=lambda s: s.position)

        self.update_stop_combo()
        self.save_state()
        self.render_gradient()

    def remove_color_stop(self):
        """Remove selected color stop."""
        if len(self.state.stops) <= 2:
            messagebox.showwarning("警告", "至少需要2个色标")
            return

        if 0 <= self.selected_stop_index < len(self.state.stops):
            self.state.stops.pop(self.selected_stop_index)
            self.selected_stop_index = max(0, self.selected_stop_index - 1)

            self.update_stop_combo()
            self.save_state()
            self.render_gradient()

    def choose_color(self):
        """Open color chooser dialog."""
        from tkinter import colorchooser

        current_color = self.state.stops[self.selected_stop_index].color
        initial_color = current_color.to_hex()

        color = colorchooser.askcolor(color=initial_color, title="选择颜色")

        if color[1]:  # If color was selected
            self.hex_var.set(color[1])
            self.apply_hex_color()

    def apply_hex_color(self):
        """Apply hex color to selected stop."""
        try:
            hex_color = self.hex_var.get()
            color = Color.from_hex(hex_color)

            if 0 <= self.selected_stop_index < len(self.state.stops):
                self.state.stops[self.selected_stop_index].color = color
                self.color_display.config(bg=hex_color)

                self.save_state()
                self.render_gradient()
        except ValueError as e:
            messagebox.showerror("错误", f"无效的颜色值: {e}")

    def on_type_change(self):
        """Handle gradient type change."""
        self.state.gradient_type = self.gradient_type_var.get()

        # Show/hide angle control based on type
        if self.state.gradient_type == GradientType.LINEAR:
            self.angle_frame.pack(fill=tk.X, pady=(0, 10), after=self.angle_frame.master.winfo_children()[1])
        else:
            self.angle_frame.pack_forget()

        self.save_state()
        self.render_gradient()

    def on_angle_change(self, value):
        """Handle angle change."""
        self.state.angle = int(float(value))
        self.delayed_render()

    def on_effect_change(self, value):
        """Handle effect parameter change."""
        self.state.noise_intensity = self.noise_var.get()
        self.state.vignette_intensity = self.vignette_var.get()
        self.delayed_render()
        
    def delayed_render(self):
        """延迟渲染，避免频繁更新造成卡顿"""
        # 取消之前的定时器
        if self.render_timer:
            self.root.after_cancel(self.render_timer)
        
        # 设置新的定时器
        self.render_timer = self.root.after(self.render_delay, self.render_gradient)

    def on_resolution_preset_change(self, event):
        """Handle preset resolution change."""
        selected = self.resolution_var.get()
        
        # Find the selected resolution
        for name, width, height in self.preset_resolutions:
            if name == selected:
                if name == "自定义":
                    # Enable custom input fields
                    self.width_entry.config(state='normal')
                    self.height_entry.config(state='normal')
                else:
                    # Set preset values and disable custom inputs
                    self.width_var.set(width)
                    self.height_var.set(height)
                    self.width_entry.config(state='readonly')
                    self.height_entry.config(state='readonly')
                    self.apply_resolution_change()
                break

    def on_custom_resolution_change(self, event):
        """Handle custom resolution input change."""
        if self.resolution_var.get() == "自定义":
            # Only apply if custom is selected
            pass  # Will be applied when user clicks Apply button

    def apply_custom_resolution(self):
        """Apply custom resolution values."""
        try:
            width = self.width_var.get()
            height = self.height_var.get()
            
            if width < 100 or height < 100:
                messagebox.showwarning("警告", "分辨率不能小于100x100")
                return
                
            if width > 8000 or height > 8000:
                messagebox.showwarning("警告", "分辨率不能大于8000x8000")
                return
                
            self.apply_resolution_change()
            
        except tk.TclError:
            messagebox.showerror("错误", "请输入有效的数字")

    def apply_resolution_change(self):
        """Apply resolution change to the gradient engine and state."""
        width = self.width_var.get()
        height = self.height_var.get()
        
        # Update state
        self.state.width = width
        self.state.height = height
        
        # Update engine
        self.engine = GradientEngine(width, height)
        
        # Re-render gradient
        self.save_state()
        self.render_gradient()

    def update_preset_list(self):
        """Update preset listbox."""
        self.preset_listbox.delete(0, tk.END)

        category = self.category_var.get()

        if category == "All":
            presets = self.preset_library.get_presets()
        else:
            presets = self.preset_library.get_presets(category)

        for preset in presets:
            self.preset_listbox.insert(tk.END, preset.name)

    def on_category_change(self, event):
        """Handle category change."""
        self.update_preset_list()

    def on_preset_select(self, event):
        """Handle preset selection."""
        selection = self.preset_listbox.curselection()

        if selection:
            index = selection[0]
            preset_name = self.preset_listbox.get(index)

            preset = self.preset_library.get_preset_by_name(preset_name)

            if preset:
                self.apply_preset(preset)

    def apply_preset(self, preset):
        """Apply a preset to current gradient."""
        self.state.gradient_type = preset.gradient_type
        self.state.angle = preset.angle
        self.state.stops = [ColorStop(s.position, Color(s.color.r, s.color.g, s.color.b))
                           for s in preset.stops]

        # Update UI
        self.gradient_type_var.set(preset.gradient_type)
        self.angle_var.set(preset.angle)
        self.update_stop_combo()

        self.on_type_change()
        self.save_state()
        self.render_gradient()

    def random_gradient(self):
        """Generate random gradient."""
        # Random type
        gradient_types = [GradientType.LINEAR, GradientType.RADIAL]
        self.state.gradient_type = random.choice(gradient_types)

        # Random angle for linear
        if self.state.gradient_type == GradientType.LINEAR:
            self.state.angle = random.choice([0, 45, 90, 135, 180, 225, 270, 315])

        # Random number of stops (2-4)
        num_stops = random.randint(2, 4)
        self.state.stops = []

        for i in range(num_stops):
            position = i / (num_stops - 1)
            color = Color(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            self.state.stops.append(ColorStop(position, color))

        # Update UI
        self.gradient_type_var.set(self.state.gradient_type)
        self.angle_var.set(self.state.angle)
        self.update_stop_combo()

        self.on_type_change()
        self.save_state()
        self.render_gradient()

    def render_gradient(self):
        """Render the current gradient."""
        # Render base gradient
        if self.state.gradient_type == GradientType.LINEAR:
            image = self.engine.render_linear_gradient(
                self.state.stops,
                self.state.angle,
                color_space='rgb'
            )
        elif self.state.gradient_type == GradientType.RADIAL:
            image = self.engine.render_radial_gradient(
                self.state.stops,
                center_x=0.5,
                center_y=0.5,
                radius=0.7,
                color_space='rgb'
            )
        else:
            return

        # Apply effects
        if self.state.noise_intensity > 0:
            image = Effects.apply_noise(image, self.state.noise_intensity)

        if self.state.vignette_intensity > 0:
            image = Effects.apply_vignette(image, self.state.vignette_intensity)

        self.current_image = image

        # Display on canvas
        self.display_image(image)

    def display_image(self, image):
        """Display image on canvas."""
        # 获取canvas的实际大小
        self.canvas.update_idletasks()  # 确保canvas已经渲染
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            # Canvas还没有正确大小，延迟显示
            self.root.after(100, lambda: self.display_image(image))
            return

        img_width, img_height = image.size
        
        # 计算缩放比例，留出更多边距
        margin = 20  # 边距
        available_width = canvas_width - margin * 2
        available_height = canvas_height - margin * 2
        
        scale_x = available_width / img_width
        scale_y = available_height / img_height
        scale = min(scale_x, scale_y, 1.0)  # 不放大，只缩小

        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        # 确保最小尺寸
        if new_width < 100:
            new_width = min(100, available_width)
            new_height = int(new_width * img_height / img_width)
        if new_height < 100:
            new_height = min(100, available_height)
            new_width = int(new_height * img_width / img_height)

        resized = image.resize((new_width, new_height), Image.LANCZOS)

        # Convert to PhotoImage
        self.tk_image = ImageTk.PhotoImage(resized)

        # Clear canvas and display
        self.canvas.delete('all')

        x = canvas_width // 2
        y = canvas_height // 2

        self.canvas.create_image(x, y, image=self.tk_image)
        
        # 添加尺寸信息显示
        info_text = f"{img_width} × {img_height}"
        self.canvas.create_text(x, y + new_height//2 + 15, text=info_text, 
                               fill="white", font=("Arial", 10))

    def export_image(self, format='png'):
        """Export current gradient as image."""
        if self.current_image is None:
            messagebox.showwarning("警告", "没有可导出的图像")
            return

        # Ask for save location
        filetypes = [
            ("PNG files", "*.png") if format == 'png' else ("JPEG files", "*.jpg"),
            ("All files", "*.*")
        ]

        default_name = self.export_manager.get_default_export_path(format)

        filepath = filedialog.asksaveasfilename(
            defaultextension=f".{format}",
            filetypes=filetypes,
            initialfile=default_name
        )

        if filepath:
            try:
                if format == 'png':
                    self.export_manager.export_png(self.current_image, filepath)
                else:
                    self.export_manager.export_jpg(self.current_image, filepath)

                messagebox.showinfo("成功", f"图像已导出到:\n{filepath}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {e}")

    def save_state(self):
        """Save current state to history."""
        self.history.add_state(self.state)

    def undo(self):
        """Undo to previous state."""
        state = self.history.undo()

        if state:
            self.state = state
            self.apply_state()
        else:
            messagebox.showinfo("提示", "没有可撤销的操作")

    def redo(self):
        """Redo to next state."""
        state = self.history.redo()

        if state:
            self.state = state
            self.apply_state()
        else:
            messagebox.showinfo("提示", "没有可重做的操作")

    def apply_state(self):
        """Apply current state to UI."""
        self.gradient_type_var.set(self.state.gradient_type)
        self.angle_var.set(self.state.angle)
        self.noise_var.set(self.state.noise_intensity)
        self.vignette_var.set(self.state.vignette_intensity)

        self.update_stop_combo()
        self.on_type_change()
        self.render_gradient()


def main():
    """Main entry point."""
    root = tk.Tk()
    app = MainWindow(root)

    # Keyboard shortcuts
    root.bind('<Control-z>', lambda e: app.undo())
    root.bind('<Control-y>', lambda e: app.redo())
    root.bind('<Control-s>', lambda e: app.export_image('png'))
    root.bind('<space>', lambda e: app.random_gradient())

    root.mainloop()


if __name__ == "__main__":
    main()
