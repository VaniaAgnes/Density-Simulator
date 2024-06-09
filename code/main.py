import tkinter as tk
from gui import DensitySimulatorUI

def main():
    root = tk.Tk()
    app = DensitySimulatorUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()