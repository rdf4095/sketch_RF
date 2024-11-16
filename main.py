"""
program: main.py

purpose: For project sketch_RF, interactive drawing.

comments: Supports freehand drawing by following cursor movement,
          or polygonal lines by drawing from mouse-click to mouse-click.

author: Russell Folks

history:
-------
10-31-2024  creation
11-04-2024  In draw_line, allow "closing" to the start point.
            Add mouse movement threshold for freehand drawing
11-08-2024  Hide 2nd canvas. Debug draw_line(). Remove old tests and comments.
            Display colorbar for selecting line color (no functionality yet.)
11-11-2024  Add mode attribute to Sketchpad, where 'freehand' draws only when
            mouse button-1 is dragged, and 'polygon' also draws lines
            between clicked points. Add second Sketchpad object.
11-13-2024  Add Frames for a statusbar below each canvas. Finish the
            implementation of the basic colorbar.
11-14-2024  Add pen_up() and pen_down() to handle mouse movement with no
            button pressed. Use the canvas info below each canvas as just a
            Label (without a Frame.)
11-15-2024  Add linewidth parameter to the class, debug the mode setting.
"""

import tkinter as tk
from tkinter import ttk

class Sketchpad(tk.Canvas):
    def __init__(self, parent, **kwargs):        
        self.width = 320
        self.height = 320
        self.mode = 'freehand'
        self.background = '#ffa'
        self.linewidth = 1
        if 'width' in kwargs: self.width = kwargs['width']
        if 'height' in kwargs: self.height = kwargs['height']
        if 'mode' in kwargs: self.mode = kwargs['mode']
        if 'background' in kwargs: self.background = kwargs['background']
        if 'linewidth' in kwargs: self.linewidth = kwargs['linewidth']

        self.linecolor = 'black'
        self.pen = 'move'    # or 'draw'

        # super().__init__(parent, **kwargs)
        super().__init__(parent,
                         width=self.width,
                         height=self.height,
                         background=self.background)

        self.firstx = 0
        self.firsty = 0
        self.startx = 0
        self.starty = 0
        # self.linewidth = 2

        if self.mode == 'freehand':
            self.bind("<Button-1>", self.set_start)
            self.bind("<Double-1>", self.connect_line)
            self.bind("ButtonRelease-1", self.pen_up)
        else: 
            if self.mode == 'lines':
                self.bind("<Button-1>", self.draw_line)
                self.bind("<Double-1>", self.connect_line)
                self.bind("ButtonRelease-1", self.pen_up)

        self.bind("<B1-Motion>", self.draw_path)


    def pen_up(self):
        self.pen = 'move'


    def pen_down(self):
        self.pen = 'draw'


    def set_first_posn(self, event) -> None:
        """Save the x-y coordinates of the first left-mouse click."""
        self.firstx, self.firsty = event.x, event.y


    def set_start(self, event) -> None:
        """
        the mouse cursor position (posn) depends on context:
        .winfo_pointerx,y is the posn of the cursor relative to the screen.
        .winfo_rootx,y is the posn of the root object relative to the screen.
        event.x,y is the posn of cursor relative to the root window.

        Notes: - the OS reserves the top 25 pixels or so for the system menubar,
                 so winfo_rooty=0 corresponds to the next pixel below this.
               - padding used by the geometry manager is not counted, so
                 winfo_pointerx = event.x + winfo_rootx + ipadx + padx.
        """
        if (self.firstx == 0 and self.firsty == 0):
            self.firstx, self.firsty = event.x, event.y

        self.startx, self.starty = event.x, event.y


    def draw_line(self, event) -> None:
        """If past the starting position, draw a line from last posn to current posn."""
        if (self.firstx == 0 and self.firsty == 0):
            self.set_first_posn(event)
            self.set_start(event)
            self.pen_down()
            return
            
        if self.pen == 'draw':
            print(f'drawing from {self.startx},{self.starty} to {event.x},{event.y}')
            self.create_line(self.startx, self.starty, event.x, event.y, fill=self.linecolor, width=self.linewidth)
            self.set_start(event)
        

    def connect_line(self, event) -> None:
        """Draw a line from the current position to the starting position."""
        if self.pen == 'draw':
            # print(f'connecting from {self.startx},{self.starty} to {self.firstx},{self.firsty}')
            self.create_line(self.startx, self.starty, self.firstx, self.firsty, fill=self.linecolor, width=self.linewidth)

            self.firstx, self.firsty = 0, 0


    def draw_path(self, event) -> None:
        """Draw a path following the cursor.
        
        TODO: use modifier key to constrain horizontal / vertical
        """
        x_threshold = 10
        y_threshold = 10

        # both thresholds: simulate jagged lines in both directions
        # if (abs(event.x - self.startx) >= x_threshold and abs(event.y - self.starty) >= y_threshold):

        # y threshold: simulate jagged horizontal lines
        # if abs(event.y - self.starty) >= y_threshold:
        #     self.create_line(self.startx, self.starty, event.x, event.y, fill=self.linecolor, width=self.linewidth)
        #     self.set_start(event)

        # x threshold: simulate jagged vertical lines
        # if abs(event.x - self.startx) >= x_threshold:
        #     self.create_line(self.startx, self.starty, event.x, event.y, fill=self.linecolor, width=self.linewidth)
        #     self.set_start(event)

        # use y threshold value to force horizontal line if path is approximately horizontal
        # yvar = event.y - self.starty
        # if yvar <= y_threshold:
        #     self.create_line(self.startx, self.starty, event.x, event.y - yvar, fill=self.linecolor, width=self.linewidth)

        # use x threshold value to force vertical line if path is approximately vertical
        xvar = event.x - self.startx
        if xvar <= x_threshold:
            self.create_line(self.startx, self.starty, event.x - xvar, event.y, fill=self.linecolor, width=self.linewidth)


        # print(f'{event.x}, {event.y}')

        # self.create_line(self.startx, self.starty, event.x, event.y, fill=self.linecolor, width=self.linewidth)
        # self.set_start(event)



def set_color(ev):
    color_choice = colorbar.gettags('current')
    # print(color_choice)
    sketch.linecolor = color_choice[0]
    sketch_2.linecolor = color_choice[0]
    

root = tk.Tk()
# default_dims = "350x300"
# root.geometry (default_dims)

# root.columnconfigure(0, weight=1)
# root.columnconfigure(1, weight=1)
# root.rowconfigure(1, weight=1)

# sketch = Sketchpad(root, width=320, height=320, background='#ff0')
sketch = Sketchpad(root)

sketch_2 = Sketchpad(root, height=200, background='#999', mode='lines')

# basic color selection for drawing
num_colors = 8      # not used yet
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'violet', 'magenta', 'black']
xs = list(range(0, 320, 40))
y1 = 0
y2 = 42
colorbar = tk.Canvas(root, width=320, height=40)
for n, x in enumerate(xs):
    colorbar.create_rectangle(x, y1, x+40, y2, fill=colors[n], tags=colors[n])# + str(n))
    
colorbar.bind('<1>', set_color)

btnq = ttk.Button(root,
                  text="Quit",
                  command=root.quit,
                  style="MyButton1.TButton")

# For the statusbar Frames, either tk or ttk widgets can be used.
# As examples, I use tk for the first canvas and ttk for the second.
# notes:
#   'relief' could be used for either tk or ttk
#   'padding' is only for ttk and is internal to the Frame
#   'highlightthickness' and 'highlightbackground' are only for tk
sketch1_status = tk.Frame(root, highlightthickness=1, highlightbackground='darkgrey')
# modetext1 = 'mode: ' + sketch.mode
status1 = ttk.Label(root, padding=2, text='mode: ' + sketch.mode)
# status1.pack(side='left', pady=2)

sketch2_status = ttk.Frame(root, padding=2, relief='groove')
status2 = ttk.Label(root, text='mode: ' + sketch_2.mode)
# status2.pack(side='left', pady=2)


sketch.grid(column=0,         row=0)
# sketch1_status.grid(column=0, row=1, sticky='ew')
status1.grid(column=0,        row=1)#, sticky='ew')
spacer = tk.Frame(root, height=10)
spacer.grid(column=0,         row=2)

sketch_2.grid(column=0,       row=3)
# sketch2_status.grid(column=0, row=4, sticky='ew')
status2.grid(column=0,        row=4)#, sticky='ew')
colorbar.grid(column=0,       row=5, pady=10)
btnq.grid(column=0,           row=6, ipady=20)

# root.grid_columnconfigure(0, weight=1)

sketch.update()

# print(f'size of sketch: {sketch.winfo_width()}, {sketch.winfo_height()}')
# colorbar.update()
# print(f'size of colorbar: {colorbar.winfo_width()}')

root.mainloop()