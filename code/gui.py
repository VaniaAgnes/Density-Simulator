import tkinter as tk
from tkinter import ttk
from main import CanvasFrame
from simulation import LiquidAnimation # Import LiquidAnimation class
import tkinter.messagebox as messagebox

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
        self.liquid_animation = LiquidAnimation(self.canvas_frame.canvas, 800, 600, density=17)
        self.canvas_frame.set_liquid_animation(self.liquid_animation)
        self.liquid_animation.animate()
