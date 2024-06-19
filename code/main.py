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
        self.liquid_animation = LiquidAnimation(self.canvas_frame.canvas, 800, 600, density=1.0)  # Use 1.0 for default
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
        self.density_label = ttk.Label(self, text="Liquid Density (kg/m^3):")
        self.density_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.density_slider = tk.Scale(self, from_=0.5, to=2.0, resolution=0.01, orient=tk.HORIZONTAL,
                                       command=self.update_density)
        self.density_slider.set(1.0)  # Default density
        self.density_slider.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

        # Object Selection Dropdown
        self.object_label = ttk.Label(self, text="Select Object:")
        self.object_label.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.preset_objects = list(self.object_values.keys())  # Use the keys from object_values
        self.object_combobox = ttk.Combobox(self, values=self.preset_objects, state="readonly")
        self.object_combobox.current(0)  # Default selection
        self.object_combobox.grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        self.object_combobox.bind("<<ComboboxSelected>>", self.update_object)

        # Object Mass Input
        self.obj_mass_label = ttk.Label(self, text="Object Mass (kg):")
        self.obj_mass_label.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        self.obj_mass_entry = ttk.Entry(self)
        self.obj_mass_entry.grid(row=2, column=3, sticky=tk.W, padx=5, pady=5)

        # Object Volume Input
        self.obj_volume_label = ttk.Label(self, text="Object Volume (m^3):")
        self.obj_volume_label.grid(row=1, column=4, sticky=tk.W, padx=10, pady=10)
        self.obj_volume_entry = ttk.Entry(self)
        self.obj_volume_entry.grid(row=2, column=4, sticky=tk.W, padx=10, pady=10)

        # Calculated Density Display
        self.calc_density_label = ttk.Label(self, text="Calculated Density (kg/m^3):")
        self.calc_density_label.grid(row=1, column=5, sticky=tk.W, padx=5, pady=5)
        self.calc_density_value = ttk.Label(self, text="", borderwidth=2, relief="sunken", width=15)
        self.calc_density_value.grid(row=2, column=5, sticky=tk.W, padx=5, pady=5)

        # Update Button
        self.update_button = ttk.Button(self, text="Update Object", command=self.update_object)
        self.update_button.grid(row=2, column=6, sticky=tk.W, padx=5, pady=5)

        # Reset Button
        self.reset_button = ttk.Button(self, text="Reset", command=self.reset)
        self.reset_button.grid(row=2, column=7, sticky=tk.W, padx=5, pady=5)

        # Canvas for animation
        self.canvas = tk.Canvas(self, width=width, height=height, bg="white")
        self.canvas.grid(row=3, column=0, columnspan=8, sticky=(tk.W, tk.E), pady=10)

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
            # Enable the entries for custom object
            self.obj_mass_entry.config(state="normal")
            self.obj_volume_entry.config(state="normal")

            if not self.obj_mass_entry.get() or not self.obj_volume_entry.get():
                messagebox.showerror("Input Error", "Please enter values for both mass and volume.")
                return
            try:
                obj_mass = float(self.obj_mass_entry.get())
                obj_volume = float(self.obj_volume_entry.get())

                # Check if mass is within range
                if obj_mass < 20 or obj_mass > 100:
                    messagebox.showerror("Input Error", "Mass value must be between 20 and 100.")
                    return

            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers for mass and volume.")
                return
        else:
            # Disable the entries for preset objects
            self.obj_mass_entry.config(state="normal")  # Enable temporarily to insert values
            self.obj_volume_entry.config(state="normal")  # Enable temporarily to insert values

            obj_density = self.object_values.get(selected_object, 0)  # Get the density from object_values

            # Use default values for mass and volume
            obj_mass = obj_density * 25  # default mass = density * 25
            obj_volume = 25  # default volume = 25

            # Display the default values in the entry fields
            self.obj_mass_entry.delete(0, tk.END)
            self.obj_mass_entry.insert(0, f"{obj_mass:.2f}")
            self.obj_mass_entry.config(state="disabled")  # Make the entry disabled but visible

            self.obj_volume_entry.delete(0, tk.END)
            self.obj_volume_entry.insert(0, f"{obj_volume:.2f}")
            self.obj_volume_entry.config(state="disabled")  # Make the entry disabled but visible

        obj_density = obj_mass / obj_volume
        self.calc_density_value.config(text=f"{obj_density:.2f} kg/m^3")

        # Show result in message box based on the object's properties
        result = self.check_float_or_sink(obj_density, obj_volume)

        if result == "Sink!":
            # Create cube first
            self.create_cube(obj_density, obj_volume, selected_object)
            # Then animate sinking
            object_animation = ObjectAnimation(self.canvas, self.cube, self.liquid_animation)
            object_animation.sink_cube()
        elif result == "Float!":
            # Create cube first
            self.create_cube(obj_density, obj_volume, selected_object)
            # Then animate floating
            object_animation = ObjectAnimation(self.canvas, self.cube, self.liquid_animation)
            object_animation.float_cube()

    def create_cube(self, obj_density, obj_volume, selected_object):
        # Remove existing cube
        if self.cube:
            self.canvas.delete(self.cube)

        # Get liquid animation parameters
        wave_center = self.liquid_animation.wave_center

        # Calculate cube dimensions based on density and volume
        mass = obj_density * obj_volume
        cube_side_length = math.pow(mass, 1 / 3.0) * 10  # Adjust scale for visibility
        cube_x = 400 - cube_side_length / 2  # Center of the canvas

        # Determine cube_y based on buoyancy
        result = self.check_float_or_sink(obj_density, obj_volume)
        if result == "Float!":
            cube_y = wave_center - 20  # Position just above the liquid
        else:
            cube_y = wave_center + 130  # Position below the liquid

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

    def check_float_or_sink(self, obj_mass, obj_volume):
        liquid_density = self.liquid_animation.density  # Density of the liquid
        buoyant_force = liquid_density * obj_volume * 9.81  # Buoyant force: liquid density * object volume * gravity
        weight = obj_mass * 9.81  # Weight of the object: mass * gravity

        # Compare the weight and buoyant Force to determine if the object floats or sinks
        if buoyant_force >= weight:
            return "Float!"
        else:
            return "Sink!"

    def reset(self):
        # Clear inputs
        self.density_slider.set(1.0)
        self.object_combobox.current(0)
        self.obj_mass_entry.delete(0, tk.END)
        self.obj_volume_entry.delete(0, tk.END)
        self.calc_density_value.config(text="")

        # Remove the cube from the canvas
        if self.cube:
            self.canvas.delete(self.cube)
            self.cube = None

if __name__ == "__main__":
    root = tk.Tk()
    app = DensitySimulatorUI(root)
    root.mainloop()
