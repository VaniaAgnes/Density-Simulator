import tkinter as tk
import math
import time

class LiquidAnimation:
    def __init__(self, canvas, width, height, density=17):
        self.canvas = canvas
        self.width = 1400
        self.height = height
        self.wave_center = height - 150  # Adjust this value to change the position of the water lines
        self.amplitude = 17
        self.period = 50
        self.offset = 0
        self.density = density  # Liquid density
        self.water_polygon = None
        self.create_water()

    def create_water(self):
        water_coords = [(0, self.height)]
        for x in range(0, self.width + 1, 17):  # Ensure it covers the full width
            y = self.wave_center + self.amplitude * math.sin((x + self.offset) / self.period)
        water_coords.append((x, y))
        water_coords.append((self.width, self.height))
        water_coords_flat = [coord for point in water_coords for coord in point]  # Flatten the list
        self.water_polygon = self.canvas.create_polygon(tuple(water_coords_flat), fill=self.get_color(), outline="")

    def animate(self):
        self.offset += 1
        water_coords = [(0, self.height)]
        for x in range(0, self.width + 1, 17):  # Ensure it covers the full width
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
        if self.density < 1000:
            return "#5cb5e1"  # Blue (Water)
        elif self.density < 1100:
            return "#b39eb5"  # Purple (Combination of Water and Oil)
        elif self.density < 1300:
            return "#FFEE8C"  # Yellow (Oil)
        elif self.density < 1600:
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

class ObjectAnimation:
    def __init__(self, canvas, cube_id, liquid_animation):
        self.canvas = canvas
        self.cube_id = cube_id
        self.liquid_animation = liquid_animation

    def sink_cube(self):
        # Get the wave center and position below the liquid
        wave_center = self.liquid_animation.wave_center
        cube_y = wave_center + 100  # Adjust this value as needed

        # Get current cube coordinates
        x1, y1, x2, y2 = self.canvas.coords(self.cube_id)

        # Calculate the movement distance for sinking
        distance = cube_y - y1

        # Animate cube movement
        self.animate_move(0, 30, distance)   # Change 20 to the number of frames you want for the animation

    def float_cube(self):
        wave_center = self.liquid_animation.wave_center
        cube_side_length = 50  # Adjust as needed
        max_float_height = wave_center - cube_side_length

        # Get current cube coordinates
        x1, y1, x2, y2 = self.canvas.coords(self.cube_id)

        # Calculate movement distance
        distance = max_float_height - y1

        # Animate cube movement
        self.animate_move(0, 40, distance)  # Adjust total_frames for a slower animation

    def animate_move(self, current_frame, total_frames, distance):
        if current_frame < total_frames:
            # Calculate the increment for movement
            increment = distance / total_frames

            # Move the cube incrementally
            self.canvas.move(self.cube_id, 0, increment)

            # Schedule the next frame with a delay of 50 milliseconds (adjust as needed)
            self.canvas.after(50, self.animate_move, current_frame + 1, total_frames, distance)
