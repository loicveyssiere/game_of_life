
import tkinter as tk
from tkinter import ttk
import engine
import utils
import time

debug = False

# ==============================================================================
# FRAMES
# ==============================================================================
class MainFrame(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):

        # Invoke super
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller_owner = self
        self.controller = Controller(self)
        self.engine = engine.EnginePythonV2()

        # Panel construction
        self.controllerFrame = ControllerFrame(self)
        if debug: self.controllerFrame.configure(background="red")
        self.boardFrame = BoardFrame(self)
        if debug: self.boardFrame.configure(background="blue")

        # Data Binding
        self.controller_owner.bind('<<data.last_board_manipulation>>', self.on_last_board_manipulation, add="+")

        # Geometry organization
        self.organize()

    def on_last_board_manipulation(self, event):
        nx = self.controller.get("board_nx")
        ny = self.controller.get("board_ny")
        print("on_last_board_manipulation")
        self.engine.fit(nx, ny)

    def organize(self):
        self.controllerFrame.pack(expand=False, fill=tk.X)
        self.boardFrame.pack(expand=True, fill=tk.BOTH)

class BoardFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        # Invoke super
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller_owner = self.parent.controller_owner
        self.controller = self.parent.controller

        # Panel construction
        self.canvas = LifeCanvas(self, borderwidth=0, highlightthickness=0)
        if debug: self.canvas.configure(background="green")

        # Geometry organization
        self.organize()

    def organize(self):
        margin = {
            "ipadx": 10,
            "ipady": 10,
            "padx": 10,
            "pady": 10
        }
        self.canvas.pack(expand=True, fill=tk.BOTH, **margin)

class ControllerFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        # Invoke super
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller_owner = self.parent.controller_owner
        self.controller = self.parent.controller
        
        # Panel construction
        self.label = tk.Label(self, text="Game Of Life")
        self.start_stop_button = ttk.Button(self, command=self.on_click_start_stop_button)
        self.one_step_button = ttk.Button(self, text='(->) One Step', command=self.on_click_one_step_button)
        self.clear_button = ttk.Button(self, text="Clear")
        self.counter_label = tk.Label(self)
        if debug: self.counter_label.configure(background="yellow")

        # Data Binding
        self.controller_owner.bind('<<data.counter>>', self.increment_counter_label, add="+")
        self.controller_owner.bind('<<data.simulation_started>>', self.toggle_start_stop_label, add="+")

        # Data init
        self.controller.set("counter", 0)
        self.controller.set("simulation_started", 0)

        # Geometry organization
        self.organize()
    
    # Actions
    def on_click_one_step_button(self):
        self.controller.set("counter", self.controller.get("counter") + 1)
    
    def on_click_start_stop_button(self):
        value = (self.controller.get("simulation_started") + 1) % 2
        self.controller.set("simulation_started", value)

    # Events
    def increment_counter_label(self, event):
        self.counter_label.configure(text=self.controller.get("counter"))

    def toggle_start_stop_label(self, event):
        value = self.controller.get("simulation_started")
        if value != 0: # Simulation is running
            self.start_stop_button["text"] = "Stop"
        else: # Simulation is stopped
            self.start_stop_button["text"] = "Start"

    def organize(self):
        nrow = 1
        ncol = 5
        for i in range(nrow):
            for j in range(ncol):
                self.columnconfigure(j, weight=1, uniform='{}'.format(i))

        grid_margin = {
            "ipadx": 5,
            "ipady": 5,
            "padx": 5,
            "pady": 10
        }

        self.label.grid(column=0, row=0, **grid_margin, sticky="ew")
        self.start_stop_button.grid(column=1, row=0, **grid_margin, sticky="ew")
        self.one_step_button.grid(column=2, row=0, **grid_margin, sticky="ew")
        self.clear_button.grid(column=3, row=0, **grid_margin, sticky="ew")
        self.counter_label.grid(column=4, row=0, **grid_margin, sticky="ew")
        
# ==============================================================================
# WIDGETS
# ==============================================================================
class LifeCanvas(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        # Super instruction
        tk.Canvas.__init__(self, parent, *args, **kwargs)

        # Resize feature
        self.bind('<Configure>', self.on_resize)
        
        # Data
        self.parent = parent
        self.controller_owner = self.parent.controller_owner
        self.controller = self.parent.controller
        self._after_id = None # For good resizing process
        self.width = self.winfo_width()
        self.height = self.winfo_height()

        # Panel construction
        self.size = 8
        self.cells = []

        # Event Binding
        self.controller_owner.bind("<<data.counter>>", self.one_step_simulation, add="+")
        self.controller_owner.bind("<<data.last_click_on_cell>>", self.on_last_click_on_cell, add="+")
        self.controller_owner.bind('<<data.simulation_started>>', self.start_stop_simulation_wrapper, add="+")

        # Drawing
        self.text = self.create_text(50, 50, fill="darkblue",font="Times 20 italic bold", text="")

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        if self._after_id:
            self.after_cancel(self._after_id)
        self._after_id = self.after(200, self.draw)

    def one_step_simulation(self, event):
        a = time.time()
        self.controller_owner.engine.one_step_simulation()
        b = time.time()
        self.update()
        c = time.time()
        print("engine {:.3f}ms | display {:.3f}ms".format((b - a) * 100, (c - b) * 100))

    def start_stop_simulation_wrapper(self, event):

        status = self.controller.get("simulation_started")
        if (status != 1): # stop me
            print("stop simulation")
            self.stop_simulation()
        else: # start me
            print("start simulation")
            self.start_simulation()

    def start_simulation(self):
        self.controller.set("counter",self.controller.get("counter") + 1)
        self.simulation_id = self.after(10, self.start_simulation)

    def stop_simulation(self):
        self.after_cancel(self.simulation_id)

    def on_last_click_on_cell(self, event):
        coord = self.controller.get("last_click_on_cell")
        value = (self.controller.get("last_click_on_cell_value") + 1) % 2
        print(coord)
        
        # Set engine and board
        self.controller_owner.engine.set(coord, value)
        self.cells[coord[0]][coord[1]].set_alive(value)

        self.cells[coord[0]][coord[1]].update()

    def update(self):
        
        # Draw cells
        for index in self.indices:
            cell = self.cells[index[0]][index[1]]
            value = self.controller_owner.engine.get(index)
            if value != cell.alive:
                cell.set_alive(value)
                cell.update()

    def draw(self):
        print("draw")
        self.delete('all')
        self.itemconfig(self.text, text="({}, {})".format(self.width, self.height))
        self.nx = self.width // self.size
        self.ny = self.height // self.size

        # Store variables
        self.controller.set("board_nx", self.nx, skip_event_binding=True)
        self.controller.set("board_ny", self.ny, skip_event_binding=True)
        self.controller.set("last_board_manipulation", utils.now())

        # Create cells
        self.indices = [(x, y) for x in range(self.nx) for y in range(self.ny)]
        self.cells = [[Cell(x, y) for y in range(self.ny)] for x in range(self.nx)]
 
        # Draw cells
        for index in self.indices:
            self.cells[index[0]][index[1]].draw(self, self.size).clickable()

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = 0
        self.color = "white"
        self.parent = None
        self.rectangle = None

    def set_alive(self, value):
        if value == 0:
            self.color = "white"
            self.alive = 0
        else:
            self.color = "black"
            self.alive = 1

    def toggle_alive(self):
        if self.alive == 0:
            self.color = "black"
            self.alive = 1
        else: 
            self.color = "white"
            self.alive = 0

    def update(self):
        self.parent.itemconfig(self.rectangle, fill=self.color)

    def draw(self, parent, size):
        self.parent = parent
        self.rectangle = parent.create_rectangle(self.x * size, self.y * size, (self.x+1) * size, (self.y+1) * size, fill="white")
        return self

    def clickable(self):
        self.parent.tag_bind(self.rectangle, '<Button-1>', self.on_click)
        return self

    def on_click(self, event):
        print("x: {}, y: {}".format(self.x, self.y))
        #self.toggle_alive()
        self.parent.controller.set("last_click_on_cell_value", self.alive, skip_event_binding=True)
        self.parent.controller.set("last_click_on_cell", (self.x, self.y))

class Button(ttk.Button):
    def __init__(self, parent, *args, **kwargs):
        ttk.Button.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.text = kwargs["text"]
        if "command" in kwargs:
            self.command = kwargs["command"]
        else:
            self.command = None
        self.toggle = 0
        self.configure(command=self.on_click)
        
    def on_click(self):

        self.toggle = (self.toggle+1) % 2 # Change mode now

        if self.command:
            self.command(self)
        else:
            print("on_click no implemented")

# ==============================================================================
# DATA
# ==============================================================================
class Controller():

    def __init__(self, frame):

        # initialise with empty structure
        self.structure = {}
        self.frame = frame

    def get(self, key):
        return self.structure[key]

    def set(self, key, value, skip_event_binding=False):
        self.structure[key] = value
        
        # Emit event on the key
        if not skip_event_binding:
            self.frame.event_generate("<<{}.{}>>".format("data", key))