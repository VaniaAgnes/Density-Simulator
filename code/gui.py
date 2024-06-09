import tkinter as tk
from tkinter import ttk
import math
from collections import OrderedDict

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

        # Canvas for animation
        self.canvas = tk.Canvas(self, width=width, height=height, bg="white")
        self.canvas.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.liquid_animation = None

    def set_liquid_animation(self, liquid_animation):
        self.liquid_animation = liquid_animation

    def update_density(self, value):
        density = float(value)
        if self.liquid_animation:
            self.liquid_animation.set_density(density)

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
        self.create_water()

    def create_water(self):
        water_coords = [(0, self.height)]
        for x in range(0, self.width, 10):
            y = self.wave_center + self.amplitude * math.sin((x + self.offset) / self.period)
            water_coords.append((x, y))
        water_coords.append((self.width, self.height))
        water_coords_flat = [coord for point in water_coords for coord in point]  # Flatten the list
        self.water_polygon = self.canvas.create_polygon(tuple(water_coords_flat), fill=self.get_color(), outline="")

    def animate(self):
        self.offset += 1
        water_coords = [(0, self.height)]
        for x in range(0, self.width, 10):
            y = self.wave_center + self.amplitude * math.sin((x + self.offset) / self.period)
            water_coords.append((x, y))
        water_coords.append((self.width, self.height))
        water_coords_flat = [coord for point in water_coords for coord in point]  # Flatten the list
        self.canvas.coords(self.water_polygon, tuple(water_coords_flat))
        self.canvas.itemconfig(self.water_polygon, fill=self.get_color())

        self.canvas.after(25, self.animate)

