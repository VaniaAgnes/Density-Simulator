import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from simulation import LiquidAnimation, ObjectAnimation
import math

class DensitySimulatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Density Simulator")

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="17")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create custom widget containing canvas and slider
        self.canvas_frame = CanvasFrame(self.main_frame, width=800, height=600)
        self.canvas_frame.grid(row=0, column=0, columnspan=2)

        # Initialize the animation with default density
        self.liquid_animation = LiquidAnimation(self.canvas_frame.canvas, 800, 600, density=0.5)
        self.canvas_frame.set_liquid_animation(self.liquid_animation)
        self.liquid_animation.animate()


class CanvasFrame(tk.Frame):
    def __init__(self, parent, width, height):
        super().__init__(parent)

        # Liquid Density Slider
        self.density_label = ttk.Label(self, text="Liquid Density:")
        self.density_label.grid(row=0, column=0, sticky=tk.W)
        self.density_slider = tk.Scale(self, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL,
                                       command=self.update_density)
        self.density_slider.set(0.5)  # Default density
        self.density_slider.grid(row=1, column=0, sticky=tk.W)

        # Object Selection Dropdown
        self.object_label = ttk.Label(self, text="Select Object:")
        self.object_label.grid(row=0, column=1, sticky=tk.W)
        self.preset_objects = ["Custom", "Paper", "Ice", "Brick", "Silicon", "Aluminum", "Titanium", "Iron", "Tin Bronze"]
        self.object_combobox = ttk.Combobox(self, values=self.preset_objects, state="readonly")
        self.object_combobox.current(0)  # Default selection
        self.object_combobox.grid(row=1, column=1, sticky=tk.W)
        self.object_combobox.bind("<<ComboboxSelected>>", self.update_object)

        # Object Density Input
        self.obj_density_label = ttk.Label(self, text="Object Density:")
        self.obj_density_label.grid(row=0, column=2, sticky=tk.W)
        self.obj_density_entry = ttk.Entry(self)
        self.obj_density_entry.grid(row=1, column=2, sticky=tk.W)

        # Object Volume Input
        self.obj_volume_label = ttk.Label(self, text="Object Volume:")
        self.obj_volume_label.grid(row=0, column=3, sticky=tk.W)
        self.obj_volume_entry = ttk.Entry(self)
        self.obj_volume_entry.grid(row=1, column=3, sticky=tk.W)

        # Update Button
        self.update_button = ttk.Button(self, text="Update Object", command=self.update_object)
        self.update_button.grid(row=1, column=4, sticky=tk.W)

        # Canvas for animation
        self.canvas = tk.Canvas(self, width=width, height=height, bg="white")
        self.canvas.grid(row=2, column=0, columnspan=5, sticky=(tk.W, tk.E))

        self.liquid_animation = None
        self.cube = None

    def set_liquid_animation(self, liquid_animation):
        self.liquid_animation = liquid_animation

    def update_density(self, value):
        density = float(value)
        if self.liquid_animation:
            self.liquid_animation.set_density(density)

    def update_object(self, event=None):
        selected_object = self.object_combobox.get()

        if selected_object == "Custom":
            if not self.obj_density_entry.get() or not self.obj_volume_entry.get():
                messagebox.showerror("Input Error", "Please enter values for both density and volume.")
                return
            try:
                obj_density = float(self.obj_density_entry.get())
                obj_volume = float(self.obj_volume_entry.get())
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers for density and volume.")
                return
        else:
            obj_density, _ = self.get_preset_object_properties(selected_object)
            try:
                obj_volume = float(
                    self.obj_volume_entry.get()) if self.obj_volume_entry.get() else messagebox.showerror("Input Error",
                                                                                                          "Please enter a valid number for volume.")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid number for volume.")
                return

            # Update density entry with preset value for clarity
            self.obj_density_entry.delete(0, tk.END)
            self.obj_density_entry.insert(0, obj_density)

        # Create cube
        self.create_cube(obj_density, obj_volume, selected_object)

        # Show result in message box based on the object's properties
        result = self.check_float_or_sink(obj_density, obj_volume)

        if result == "Sink!":
            object_animation = ObjectAnimation(self.canvas, self.cube, self.liquid_animation)
            object_animation.sink_cube()
        elif result == "Float!":
            object_animation = ObjectAnimation(self.canvas, self.cube, self.liquid_animation)
            object_animation.float_cube()

        messagebox.showinfo("Float or Sink", result)

    def get_preset_object_properties(self, obj_name):
        # Define densities for preset objects
        properties = {
            "Paper": 0.8,
            "Ice": 0.92,
            "Brick": 2.4,
            "Silicon": 2.33,
            "Aluminum": 2.7,
            "Titanium": 4.5,
            "Iron": 7.87,
            "Tin Bronze": 8.8
        }
        return properties.get(obj_name, 17), 17

    def create_cube(self, obj_density, obj_volume, selected_object):
        # Remove existing cube
        if self.cube:
            self.canvas.delete(self.cube)

        # Get liquid animation parameters
        wave_center = self.liquid_animation.wave_center

        # Calculate cube dimensions based on density and volume
        # Volume = mass / density
        mass = obj_density * obj_volume
        # Assuming the cube shape, calculate its side length
        cube_side_length = math.pow(mass, 1 / 3.0) * 10  # Adjust scale for visibility
        cube_x = 400 - cube_side_length / 2  # Center of the canvas

        # Determine cube_y based on buoyancy
        result = self.check_float_or_sink(obj_density, obj_volume)
        if result == "Float!":
            cube_y = wave_center - cube_side_length  # Position just above the liquid
        else:
            cube_y = wave_center + 100  # Position below the liquid

        # Determine color based on selected object
        colors = {
            "Paper": "white",
            "Ice": "light blue",
            "Brick": "#bc4a3c",  # Red brown
            "Silicon": "#9599a5",
            "Aluminum": "#848789",
            "Titanium": "#878681",
            "Iron": "#d4d7d9",
            "Tin Bronze": "#cd7f32",
            "Custom": "black"
        }
        cube_color = colors.get(selected_object, "black")

        # Draw cube
        self.cube = self.canvas.create_rectangle(cube_x, cube_y, cube_x + cube_side_length, cube_y + cube_side_length,
                                                 fill=cube_color, outline="")

    def check_float_or_sink(self, obj_density, obj_volume):
        liquid_density = self.liquid_animation.density
        buoyant_force = liquid_density * obj_volume * 9.81  # Assuming gravity = 9.81 m/s^2
        weight = obj_density * obj_volume * 9.81  # Assuming gravity = 9.81 m/s^2

        # Compare the weight and buoyant force to determine if the object floats or sinks
        if buoyant_force >= weight:
            return "Float!"
        else:
            return "Sink!"

if __name__ == "__main__":
    root = tk.Tk()
    app = DensitySimulatorUI(root)
    root.mainloop()

