        # Liquid Density Slider
        self.density_label = ttk.Label(self, text="Liquid Density:")
        self.density_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        self.density_slider = tk.Scale(self, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL,
                                       command=self.update_density)
        self.density_slider.set(0.5)  # Default density
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