import json
import random
import tkinter as tk
from tkinter import filedialog, colorchooser

# Define objects with descriptive names
OBJECTS = {
    0: 'Empty Space',
    1: 'Grass Top Corner',
    2: 'Grass Body',
    3: 'Grass Top',
    4: 'Grass Left',
    5: 'Tree',
    6: 'Stone1',
    7: 'Waterfall',
    8: 'Top Left',
    9: 'Top Right',
    10: 'Middle Left',
    11: 'Middle Right',
    12: 'Bottom Left',
    13: 'Bottom Right',
    14: 'Stone Top',
    15: 'Stone Bottom',
    16: 'Well',
    17: 'Dark Green Grass',
    18: 'Dark Green Stone',
    19: 'Dark Green Well',
    20: 'npc1',
    21: 'npc2',
    22: 'Map Bottom',
    23: 'left',
    24: 'Map bottom left'
}

# Define colors for each object
OBJECT_COLORS = {
    0: 'white',          # Empty Space
    1: 'green',          # Grass Top Corner
    2: 'blue',           # Grass Body
    3: 'red',            # Grass Top
    4: 'yellow',         # Grass Left
    5: 'brown',          # Tree
    6: 'teal',           # Stone1
    7: 'navy',           # Waterfall
    8: 'orange',         # Top Left
    9: 'purple',         # Top Right
    10: 'pink',          # Middle Left
    11: 'cyan',          # Middle Right
    12: 'magenta',       # Bottom Left
    13: 'lime',          # Bottom Right
    14: 'cyan',          # Stone Top
    15: 'red',           # Stone Bottom
    16: 'white',         # Well
    17: 'green',         # dark grass
    18: 'yellow',        # dark stone
    19: 'grey',          # dark well
    20: 'black',         # npc1
    21: 'black',         # npc2
    22: 'black',         # Map Left
    23: 'red',           # Map Bottom
    24: 'cyan'            # Map bottom left
}

class MapEditor:
    def __init__(self, map_width, map_height, cell_size):
        self.map_width = map_width
        self.map_height = map_height
        self.cell_size = cell_size
        self.map_data = [[0] * map_width for _ in range(map_height)]  # Initialize map data (0 for walkable)
        self.current_object = 1  # Default object is grass top corner
        self.current_color = 'green'  # Default color
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.map_width * self.cell_size, height=self.map_height * self.cell_size, bg='white')
        self.create_menu()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Randomize Map", command=self.randomize_map)
        file_menu.add_command(label="Save Map", command=self.save_to_json)
        file_menu.add_command(label="Load Map", command=self.load_from_json)
        file_menu.add_command(label="Quit", command=self.quit)
        
        object_menu = tk.Menu(menu)
        menu.add_cascade(label="Objects", menu=object_menu)
        for obj_type, obj_name in OBJECTS.items():
            object_menu.add_command(label=obj_name, command=lambda b=obj_type: self.select_object(b))
        
        menu.add_command(label="Choose Color", command=self.choose_color)
        menu.add_command(label="Set All Blocks to Grass Body", command=self.set_all_to_same_object)

    def run(self):
        self.canvas.grid(row=1, columnspan=len(OBJECTS), padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.place_object)
        self.canvas.bind("<Button-3>", self.remove_object)
        self.root.mainloop()

    def select_object(self, obj_type):
        self.current_object = obj_type

    def place_object(self, event):
        x, y = event.x // self.cell_size, event.y // self.cell_size
        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            self.map_data[y][x] = self.current_object
            self.draw_map()

    def remove_object(self, event):
        x, y = event.x // self.cell_size, event.y // self.cell_size
        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            self.map_data[y][x] = 0
            self.draw_map()

    def draw_map(self):
        self.canvas.delete("all")
        for y in range(self.map_height):
            for x in range(self.map_width):
                obj_type = self.map_data[y][x]
                if obj_type != 0:
                    color = OBJECT_COLORS[obj_type]
                    self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                                 (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                                 fill=color, outline="black")

    def choose_color(self):
        obj_type = self.current_object
        color = colorchooser.askcolor(title=f"Choose Color for {OBJECTS[obj_type]}")
        if color[1]:  # Check if a color was selected
            OBJECT_COLORS[obj_type] = color[1]
            self.current_color = color[1]

    def set_all_to_same_object(self):
        for y in range(self.map_height):
            for x in range(self.map_width):
                self.map_data[y][x] = self.current_object
        self.draw_map()

    def randomize_map(self):
        for y in range(self.map_height):
            for x in range(self.map_width):
                self.map_data[y][x] = random.choice(list(OBJECTS.keys()))
        self.draw_map()

    def save_to_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json")
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.map_data, f)  # Serialize map data to JSON
            print("Map saved successfully.")

    def load_from_json(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'r') as f:
                self.map_data = json.load(f)  # Deserialize map data from JSON
            print("Map loaded successfully.")
            self.draw_map()

    def quit(self):
        self.root.quit()

if __name__ == '__main__':
    editor = MapEditor(50, 50, 18)  # Map size: 50x50, Cell size: 18 pixels
    editor.run()
