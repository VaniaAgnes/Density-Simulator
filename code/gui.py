import tkinter as tk
from tkinter import ttk
from simulation import LiquidAnimation

class DensitySimulatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Density Simulator")
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Canvas for animation
        self.canvas = tk.Canvas(self.main_frame, width=800, height=600, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=2)
        
        # Initialize the animation
        self.liquid_animation = LiquidAnimation(self.canvas, 800, 600)
        self.liquid_animation.animate()
        

if __name__ == "__main__":
    root = tk.Tk()
    app = DensitySimulatorUI(root)
    root.mainloop()