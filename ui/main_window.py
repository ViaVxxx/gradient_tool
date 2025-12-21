"""Main application window."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import random

from core.gradient_engine import GradientEngine, GradientType
from core.color_utils import Color, ColorStop
from core.presets import PresetLibrary
from core.effects import Effects
from utils.export import ExportManager
from utils.history import HistoryManager


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
        self.root.geometry("1200x800")

        # Initialize components
        self.engine = GradientEngine(800, 600)
        self.preset_library = PresetLibrary()
        self.export_manager = ExportManager()
        self.history = HistoryManager()

        # Current state
        self.state = GradientState()
        self.current_image = None
        self.tk_image = None
        self.selected_stop_index = 0

        # Setup UI
        self._setup_ui()

        # Initial render
        self.render_gradient()
        self.history.add_state(self.state)

    def _setup_ui(self):
        """Setup the user interface."""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel - Controls
        left_panel = ttk.Frame(main_container, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)

        # Right panel - Preview
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Setup left panel controls
        self._setup_controls(left_panel)

        # Setup preview canvas
        self._setup_preview(right_panel)

    def _setup_controls(self, parent):
        """Setup control panel."""

        # Title
        title = ttk.Label(parent, text="渐变控制", font=("Arial", 14, "bold"))
        title.pack(pady=(0, 10))

        # Gradient Type
        type_frame = ttk.LabelFrame(parent, text="渐变类型", padding=10)
        type_frame.pack(fill=tk.X, pady=(0, 10))

        self.gradient_type_var = tk.StringVar(value=GradientType.LINEAR)

        ttk.Radiobutton(type_frame, text="线性渐变", variable=self.gradient_type_var,
                       value=GradientType.LINEAR, command=self.on_type_change).pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="径向渐变", variable=self.gradient_type_var,
                       value=GradientType.RADIAL, command=self.on_type_change).pack(anchor=tk.W)

        # Angle control (for linear gradient)
        self.angle_frame = ttk.LabelFrame(parent, text="角度", padding=10)
        self.angle_frame.pack(fill=tk.X, pady=(0, 10))

        self.angle_var = tk.IntVar(value=90)
        angle_scale = ttk.Scale(self.angle_frame, from_=0, to=360, variable=self.angle_var,
                               orient=tk.HORIZONTAL, command=self.on_angle_change)
        angle_scale.pack(fill=tk.X)

        angle_label = ttk.Label(self.angle_frame, textvariable=self.angle_var)
        angle_label.pack()

        # Color Stops
        stops_frame = ttk.LabelFrame(parent, text="色标", padding=10)
        stops_frame.pack(fill=tk.X, pady=(0, 10))

        # Stop selector
        stop_select_frame = ttk.Frame(stops_frame)
        stop_select_frame.pack(fill=tk.X, pady=(0, 5))

        self.stop_var = tk.StringVar()
        self.stop_combo = ttk.Combobox(stop_select_frame, textvariable=self.stop_var,
                                       state='readonly', width=15)
        self.stop_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.stop_combo.bind('<<ComboboxSelected>>', self.on_stop_select)

        # Add/Remove stop buttons
        ttk.Button(stop_select_frame, text="+", width=3,
                  command=self.add_color_stop).pack(side=tk.LEFT, padx=2)
        ttk.Button(stop_select_frame, text="-", width=3,
                  command=self.remove_color_stop).pack(side=tk.LEFT)

        # Color picker
        color_frame = ttk.Frame(stops_frame)
        color_frame.pack(fill=tk.X, pady=5)

        ttk.Label(color_frame, text="颜色:").pack(side=tk.LEFT)
        self.color_display = tk.Canvas(color_frame, width=30, height=30, bg="#667EEA")
        self.color_display.pack(side=tk.LEFT, padx=5)

        ttk.Button(color_frame, text="选择颜色",
                  command=self.choose_color).pack(side=tk.LEFT)

        # Hex input
        hex_frame = ttk.Frame(stops_frame)
        hex_frame.pack(fill=tk.X)

        ttk.Label(hex_frame, text="HEX:").pack(side=tk.LEFT)
        self.hex_var = tk.StringVar(value="#667EEA")
        self.hex_entry = ttk.Entry(hex_frame, textvariable=self.hex_var, width=10)
        self.hex_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(hex_frame, text="应用",
                  command=self.apply_hex_color).pack(side=tk.LEFT)

        # Effects
        effects_frame = ttk.LabelFrame(parent, text="效果", padding=10)
        effects_frame.pack(fill=tk.X, pady=(0, 10))

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
        presets_frame = ttk.LabelFrame(parent, text="预设", padding=10)
        presets_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

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

        # Load presets
        self.update_preset_list()

        # Action buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(button_frame, text="随机生成",
                  command=self.random_gradient).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="导出 PNG",
                  command=lambda: self.export_image('png')).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="导出 JPG",
                  command=lambda: self.export_image('jpg')).pack(fill=tk.X, pady=2)

        # Undo/Redo buttons
        undo_frame = ttk.Frame(parent)
        undo_frame.pack(fill=tk.X)

        ttk.Button(undo_frame, text="撤销 (Ctrl+Z)",
                  command=self.undo).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        ttk.Button(undo_frame, text="重做 (Ctrl+Y)",
                  command=self.redo).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

    def _setup_preview(self, parent):
        """Setup preview canvas."""
        preview_frame = ttk.LabelFrame(parent, text="预览", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for image preview
        self.canvas = tk.Canvas(preview_frame, bg='#2b2b2b')
        self.canvas.pack(fill=tk.BOTH, expand=True)

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
        self.render_gradient()

    def on_effect_change(self, value):
        """Handle effect parameter change."""
        self.state.noise_intensity = self.noise_var.get()
        self.state.vignette_intensity = self.vignette_var.get()
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
        # Resize image to fit canvas while maintaining aspect ratio
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            # Canvas not yet sized, use default
            canvas_width = 800
            canvas_height = 600

        img_width, img_height = image.size
        scale = min(canvas_width / img_width, canvas_height / img_height)

        new_width = int(img_width * scale * 0.9)  # 90% to leave margin
        new_height = int(img_height * scale * 0.9)

        resized = image.resize((new_width, new_height), Image.LANCZOS)

        # Convert to PhotoImage
        self.tk_image = ImageTk.PhotoImage(resized)

        # Clear canvas and display
        self.canvas.delete('all')

        x = canvas_width // 2
        y = canvas_height // 2

        self.canvas.create_image(x, y, image=self.tk_image)

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
