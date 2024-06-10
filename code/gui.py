# gui.py
import tkinter as tk
from tkinter import ttk
from simulation import LiquidAnimation  # Import LiquidAnimation class

class DensitySimulatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Density Simulator")
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create custom widget containing canvas and slider
        self.canvas_frame = CanvasFrame(self.main_frame, width=800, height=600)
        self.canvas_frame.grid(row=0, column=0, columnspan=2)

        # Initialize the animation with default density
        self.liquid_animation = LiquidAnimation(self.canvas_frame.canvas, 800, 600, density=1.0)
        self.canvas_frame.set_liquid_animation(self.liquid_animation)
        self.liquid_animation.animate()

class CanvasFrame(tk.Frame):
    def __init__(self, parent, width, height):
        super().__init__(parent)

        # Liquid Density Slider
        self.density_label = ttk.Label(self, text="Liquid Density:")
        self.density_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        self.density_slider = tk.Scale(self, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.update_density)
        self.density_slider.set(1.0)  # Default density
        self.density_slider.grid(row=1, column=0, columnspan=2, sticky=tk.W)

        # Object Selection Dropdown
        self.object_label = ttk.Label(self, text="Select Object:")
        self.object_label.grid(row=2, column=0, columnspan=2, sticky=tk.W)

        # Define preset objects with densities
        self.preset_objects = {
            "Paper": 0.8,
            "Ice": 0.92,
            "Brick": 2.4,
            "Silicon": 2.33,
            "Aluminum": 2.7,
            "Titanium": 4.5,
            "Iron": 7.87,
            "Tin Bronze": 8.7
        }

        self.object_combobox = ttk.Combobox(self, values=list(self.preset_objects.keys()), state="readonly")
        self.object_combobox.current(0)  # Default selection
        self.object_combobox.grid(row=3, column=0, columnspan=2, sticky=tk.W)
        self.object_combobox.bind("<<ComboboxSelected>>", self.update_object)

        # Canvas for animation
        self.canvas = tk.Canvas(self, width=width, height=height, bg="white")
        self.canvas.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.liquid_animation = None
        self.cube = None  # Add the cube attribute here
        self.cube_properties = {}  # Add cube properties dictionary

    def set_liquid_animation(self, liquid_animation):
        self.liquid_animation = liquid_animation

    def update_density(self, value):
        density = float(value)
        if self.liquid_animation:
            self.liquid_animation.set_density(density)

    def update_object(self, event):
        selected_object = self.object_combobox.get()
        self.create_cube(selected_object)

    def create_cube(self, selected_object):
        # Remove existing cube
        if self.cube:
            self.canvas.delete(self.cube)

        # Get liquid animation parameters
        wave_center = self.liquid_animation.wave_center

        # Calculate cube dimensions and position
        cube_width = 100
        cube_height = 100
        cube_x = 400 - cube_width / 2  # Center of the canvas
        cube_y = wave_center - cube_height  # Just above the liquid

        # Create cube with color based on selected object
        cube_color = self.get_cube_color(selected_object)

        # Define cube properties
        volume = cube_width * cube_height * cube_height  # Volume in cubic units (assuming cube)
        density = self.preset_objects[selected_object]  # Density from preset
        mass = density * volume

        self.cube_properties = {
            'density': density,
            'volume': volume,
            'mass': mass,
            'color': cube_color
        }

        # Draw cube
        self.cube = self.canvas.create_rectangle(cube_x, cube_y, cube_x + cube_width, cube_y + cube_height, fill=cube_color)

        # Update cube position based on buoyancy
        self.update_cube_position()

    def get_cube_color(self, selected_object):
        cube_colors = {
            "Paper": "white",
            "Ice": "light blue",
            "Brick": "red",
            "Silicon": "grey",
            "Aluminum": "silver",
            "Titanium": "gray",
            "Iron": "dark gray",
            "Tin Bronze": "brown"
        }
        return cube_colors.get(selected_object, "black")

    def update_cube_position(self):
        if not self.cube:
            return

        liquid_density = self.liquid_animation.density
        cube_density = self.cube_properties['density']
        volume = self.cube_properties['volume']

        # Calculate the weight of the cube (force due to gravity)
        weight = cube_density * volume * 9.81  # Assuming gravity = 9.81 m/s^2

        # Calculate the buoyant force
        buoyant_force = liquid_density * volume * 9.81  # Assuming gravity = 9.81 m/s^2

        # Calculate the net force (difference between weight and buoyant force)
        net_force = buoyant_force - weight

        # If the net force is positive, the block floats; if negative, it sinks
        if net_force >= 0:
            # Calculate the acceleration due to the net force (F = ma)
            acceleration = net_force / (cube_density * volume)

            # Update the position of the cube based on acceleration
            self.canvas.move(self.cube, 0, -acceleration * 0.025)  # Move the cube upward
