import tkinter as tk
import math

class LiquidAnimation:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.wave_center = height - 150  # Adjust this value to change the position of the water lines
        self.amplitude = 10
        self.period = 50
        self.offset = 0
        self.water_polygon = None
        self.create_water()

    def create_water(self):
        water_coords = [(0, self.height)]
        for x in range(0, self.width, 10):
            y = self.wave_center + self.amplitude * math.sin((x + self.offset) / self.period)
            water_coords.append((x, y))
        water_coords.append((self.width, self.height))
        water_coords_flat = [coord for point in water_coords for coord in point]  # Flatten the list
        self.water_polygon = self.canvas.create_polygon(tuple(water_coords_flat), fill="blue", outline="")

    def animate(self):
        self.offset += 1
        water_coords = [(0, self.height)]
        for x in range(0, self.width, 10):
            y = self.wave_center + self.amplitude * math.sin((x + self.offset) / self.period)
            water_coords.append((x, y))
        water_coords.append((self.width, self.height))
        water_coords_flat = [coord for point in water_coords for coord in point]  # Flatten the list
        self.canvas.coords(self.water_polygon, tuple(water_coords_flat))

        self.canvas.after(25, self.animate)