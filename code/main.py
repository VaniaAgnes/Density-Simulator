import tkinter as tk
from tkinter import ttk
import math

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

        self.density_slider = tk.Scale(self, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL,
                                       command=self.update_density)
        self.density_slider.set(1.0)  # Default density
        self.density_slider.grid(row=1, column=0, columnspan=2, sticky=tk.W)

        # Object Selection Dropdown
        self.object_label = ttk.Label(self, text="Select Object:")
        self.object_label.grid(row=2, column=0, columnspan=2, sticky=tk.W)

        # Define preset objects
        self.preset_objects = ["Paper", "Ice", "Brick", "Silicon", "Aluminum", "Titanium", "Iron", "Tin Bronze"]

        self.object_combobox = ttk.Combobox(self, values=self.preset_objects, state="readonly")
        self.object_combobox.current(0)  # Default selection
        self.object_combobox.grid(row=3, column=0, columnspan=2, sticky=tk.W)
        self.object_combobox.bind("<<ComboboxSelected>>", self.update_object)

        # Canvas for animation
        self.canvas = tk.Canvas(self, width=width, height=height, bg="white")
        self.canvas.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.liquid_animation = None
        self.cube = None  # Add the cube attribute here

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
        if selected_object == "Paper":
            cube_color = "white"
        elif selected_object == "Ice":
            cube_color = "light blue"
        elif selected_object == "Brick":
            cube_color = "red"
        elif selected_object == "Silicon":
            cube_color = "grey"
        elif selected_object == "Aluminum":
            cube_color = "silver"
        elif selected_object == "Titanium":
            cube_color = "gray"
        elif selected_object == "Iron":
            cube_color = "dark gray"
        elif selected_object == "Tin Bronze":
            cube_color = "brown"
        else:
            cube_color = "black"

        # Draw cube
        self.cube = self.canvas.create_rectangle(cube_x, cube_y, cube_x + cube_width, cube_y + cube_height,
                                                 fill=cube_color)


class LiquidAnimation:
    def __init__(self, canvas, width, height, density=1.0):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.wave_center = height - 150  # Adjust this value to change the position of the water lines
        self.amplitude = 10
        self.period = 50
        self.offset = 0
        self.density = density  # Liquid density
        self.water_polygon = None
        self.color = self.get_color()  # Initial color
        self.create_water()

    def create_water(self):
        water_coords = [(0, self.height)]
        for x in range(0, self.width, 10):
            y = self.wave_center + self.amplitude * math.sin((x + self.offset) / self.period)
            water_coords.append((x, y))
        water_coords.append((self.width, self.height))
        water_coords_flat = [coord for point in water_coords for coord in point]  # Flatten the list
        self.water_polygon = self.canvas.create_polygon(tuple(water_coords_flat), fill=self.color, outline="")

    def animate(self):
        self.offset += 1
        water_coords = [(0, self.height)]
        for x in range(0, self.width, 10):
            y = self.wave_center + self.amplitude * math.sin((x + self.offset) / self.period)
            water_coords.append((x, y))
        water_coords.append((self.width, self.height))
        water_coords_flat = [coord for point in water_coords for coord in point]  # Flatten the list
        self.canvas.coords(self.water_polygon, tuple(water_coords_flat))

        # Update color based on density
        new_color = self.get_color()
        self.transition_color(new_color)

        self.canvas.after(25, self.animate)

    def set_density(self, density):
        self.density = density

    def get_color(self):
        # Determine the color based on density
        if self.density < 0.9:
            return "#5cb5e1"  # Blue (Water)
        elif self.density < 1.1:
            return "#b39eb5"  # Purple (Combination of Water and Oil)
        elif self.density < 1.3:
            return "#FFEE8C"  # Yellow (Oil)
        elif self.density < 1.6:
            return "#FFD1DC"  # Pink (Soap)
        else:
            return "#BC9337" # Dark Orange (Honey)
 
    def transition_color(self, new_color):
        # Smoothly transition the color
        current_color = self.canvas.itemcget(self.water_polygon, "fill")
        current_rgb = self.hex_to_rgb(current_color)
        new_rgb = self.hex_to_rgb(new_color)
        step = 0.05

        # Interpolate between the current color and the new color
        interpolated_rgb = [
            int(current_rgb[i] + (new_rgb[i] - current_rgb[i]) * step)
            for i in range(3)
        ]

        interpolated_color = self.rgb_to_hex(interpolated_rgb)

        # Update the color of the polygon
        self.canvas.itemconfig(self.water_polygon, fill=interpolated_color)

    def hex_to_rgb(self, hex_color):
        return [int(hex_color[i:i + 2], 16) for i in range(1, 7, 2)]

    def rgb_to_hex(self, rgb_color):
        return f'#{rgb_color[0]:02x}{rgb_color[1]:02x}{rgb_color[2]:02x}'

if __name__ == "__main__":
    root = tk.Tk()
    app = DensitySimulatorUI(root)
    root.mainloop()
