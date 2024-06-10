# main.py
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
        self.canvas_frame.grid(row=1, column=0, columnspan=2)

        # Initialize the animation with default density
        self.liquid_animation = LiquidAnimation(self.canvas_frame.canvas, 800, 600, density=0.5)
        self.canvas_frame.set_liquid_animation(self.liquid_animation)
        self.liquid_animation.animate()


class CanvasFrame(tk.Frame):
    def __init__(self, parent, width, height):
        super().__init__(parent)

        # Title Label
        self.title_label = ttk.Label(self, text="Density Simulator", font=("Helvetica", 16))
        self.title_label.grid(row=0, column=0, columnspan=7, pady=10)

        # Initial values for objects
        self.object_values = {
            "Custom": 1.0,  # Default value for custom objects
            "Paper": 0.8,
            "Ice": 0.92,
            "Brick": 2.4,
            "Silicon": 2.33,
            "Aluminum": 2.7,
            "Titanium": 4.5,
            "Iron": 7.87,
            "Tin Bronze": 8.8
        }

        # Liquid Density Slider
        self.density_label = ttk.Label(self, text="Liquid Density:")
        self.density_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        self.density_slider = tk.Scale(self, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL,
                                       command=self.update_density)
        self.density_slider.set(17)  # Default density
        self.density_slider.grid(row=1, column=0, columnspan=2, sticky=tk.W)

        # Object Selection Dropdown
        self.object_label = ttk.Label(self, text="Select Object:")
        self.object_label.grid(row=2, column=0, columnspan=2, sticky=tk.W)
        self.preset_objects = ["Custom", "Paper", "Ice", "Brick", "Silicon", "Aluminum", "Titanium", "Iron", "Tin Bronze"]
        self.object_combobox = ttk.Combobox(self, values=self.preset_objects, state="readonly")
        self.object_combobox.current(0)  # Default selection
        self.object_combobox.grid(row=3, column=0, columnspan=2, sticky=tk.W)
        self.object_combobox.bind("<<ComboboxSelected>>", self.update_object)

        # Object Density Input
        self.obj_density_label = ttk.Label(self, text="Object Density:")
        self.obj_density_label.grid(row=4, column=0, columnspan=2, sticky=tk.W)
        self.obj_density_entry = ttk.Entry(self)
        self.obj_density_entry.grid(row=5, column=0, columnspan=2, sticky=tk.W)

        # Object Volume Input
        self.obj_volume_label = ttk.Label(self, text="Object Volume:")
        self.obj_volume_label.grid(row=6, column=0, columnspan=2, sticky=tk.W)
        self.obj_volume_entry = ttk.Entry(self)
        self.obj_volume_entry.grid(row=7, column=0, columnspan=2, sticky=tk.W)

        # Update Button
        self.update_button = ttk.Button(self, text="Update Object", command=self.update_object)
        self.update_button.grid(row=8, column=0, columnspan=2, sticky=tk.W)

        # Canvas for animation
        self.canvas = tk.Canvas(self, width=width, height=height, bg="white")
        self.canvas.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E))

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
            obj_density = float(self.obj_density_entry.get())
            obj_volume = float(self.obj_volume_entry.get())
        else:
            obj_density, obj_volume = self.get_preset_object_properties(selected_object)
            # Update entries with preset values for clarity
            self.obj_density_entry.delete(0, tk.END)
            self.obj_density_entry.insert(0, obj_density)
            self.obj_volume_entry.delete(0, tk.END)
            self.obj_volume_entry.insert(0, obj_volume)

        self.create_cube(obj_density, obj_volume, selected_object)

    def get_preset_object_properties(self, obj_name):
        # Define densities and volumes for preset objects
        properties = {
            "Paper": (0.8, 17),
            "Ice": (0.92, 17),
            "Brick": (2.4, 17),
            "Silicon": (2.33, 17),
            "Aluminum": (2.7, 17),
            "Titanium": (4.5, 17),
            "Iron": (7.87, 17),
            "Tin Bronze": (8.8, 17)
        }
        return properties.get(obj_name, (17, 17))

    def create_cube(self, obj_density, obj_volume, selected_object):
        # Remove existing cube
        if self.cube:
            self.canvas.delete(self.cube)

        # Get liquid animation parameters
        wave_center = self.liquid_animation.wave_center

        # Calculate cube dimensions based on density and volume
        mass = obj_density * obj_volume
        # Assuming the cube shape, calculate its side length
        cube_side_length = math.pow(mass, 1/3.0) * 17  # Adjust scale for visibility
        cube_x = 400 - cube_side_length / 2  # Center of the canvas
        cube_y = wave_center - cube_side_length  # Position just above the liquid

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
        if selected_object == "Silicon":
            self.cube = self.canvas.create_rectangle(cube_x, cube_y, cube_x + cube_side_length, cube_y + cube_side_length,
                                                     fill=cube_color, outline=outline_color)
        else:
            self.cube = self.canvas.create_rectangle(cube_x, cube_y, cube_x + cube_side_length, cube_y + cube_side_length,
                                                     fill=cube_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = DensitySimulatorUI(root)
    root.mainloop()
