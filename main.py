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
"""

import tkinter as tk
from tkinter import ttk

class Sketchpad(tk.Canvas):
    def __init__(self, parent, mode='freehand', **kwargs):        
        self.mode = mode
        self.width = 320
        self.height = 320
        self.background = '#ffa'

        self.linecolor = 'black'

        if 'width' in kwargs: self.width = kwargs['width']
        if 'height' in kwargs: self.height = kwargs['height']
        if 'background' in kwargs: self.background = kwargs['background']

        # super().__init__(parent, **kwargs)
        super().__init__(parent, width=self.width, height=self.height, background=self.background)

        self.startx = 0
        self.starty = 0
        self.lastx = 0
        self.lasty = 0
        self.linewidth = 2

        print(f'mode: {self.mode}')

        if self.mode == 'freehand':
            self.bind("<Button-1>", self.set_point)
        else: 
            if self.mode == 'polygon':
                self.bind("<Button-1>", self.draw_line)
                self.bind("<Double-1>", self.connect_line)

        self.bind("<B1-Motion>", self.draw_path)
        

    def save_posn(self, event) -> None:
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
        # event_report = f'event: {event.x}, {event.y}; '
        # pointer_report = f'pointer: {root.winfo_pointerx()}, {root.winfo_pointery()}; '
        # root_report = f'root: {root.winfo_rootx()}, {root.winfo_rooty()}; '
        # reprt = event_report + pointer_report + root_report
        # print(reprt)
        self.lastx, self.lasty = event.x, event.y


    def save_start_posn(self, event) -> None:
        """Save the x-y coordinates of the first left-mouse click."""
        self.startx, self.starty = event.x, event.y
        # print(f'starting: {self.startx},{self.starty}')


    def draw_line(self, event) -> None:
        """If past the starting position, draw a line from last posn to current posn."""
        if (self.startx == 0 and self.starty == 0):
            self.save_start_posn(event)
            self.save_posn(event)
            return
        
        self.create_line(self.lastx, self.lasty, event.x, event.y, fill=self.linecolor, width=self.linewidth)
        self.save_posn(event)


    def set_point(self, event) -> None:
        self.lastx, self.lasty = event.x, event.y


    def connect_line(self, event) -> None:
        """Draw a line from the current position to the starting position."""
        # print('in connect_line')
        # print(f'    drawing from {event.x},{event.y} to {self.startx},{self.starty}')
        self.create_line(event.x, event.y, self.startx, self.starty, fill=self.linecolor, width=self.linewidth)


    def draw_path(self, event) -> None:
        """Draw a path following the cursor."""
        x_threshold = 1
        y_threshold = 1

        if (abs(event.x - self.lastx) >= x_threshold and abs(event.y - self.lasty) >= y_threshold):
            self.create_line(self.lastx, self.lasty, event.x, event.y, fill=self.linecolor, width=self.linewidth)
            self.save_posn(event)



def set_color(ev):
    color_choice = colorbar.gettags('current')
    print(color_choice)
    # index = int(color_choice[5:])
    # print(index)
    # print(f'{ev}, color tag: {color_choice}, color: {colors[index]}')
    


root = tk.Tk()
# default_dims = "350x300"
# root.geometry (default_dims)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

var1 = 100
var2 = 200
# sketch = Sketchpad(root, width=320, height=320, background='#ff0')
sketch = Sketchpad(root)

sketch.configure()


sketch_2 = Sketchpad(root, width=400, height=200, background='#999', mode='polygon')

# display 8 color samples, for user selection of line color
num_colors = 8      # not used yet
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'violet', 'magenta', 'black']
xs = list(range(0, 320, 40))
y1 = 0
y2 = 42
colorbar = tk.Canvas(root, width=320, height=40)
for n, x in enumerate(xs):
    colorbar.create_rectangle(x, y1, x+40, y2, fill=colors[n], tags='color' + str(n))
    
colorbar.bind('<1>', set_color)

btnq = ttk.Button(root,
                  text="Quit",
                  command=root.quit,
                  style="MyButton1.TButton")

sketch.grid(column=0,   row=0)
sketch_2.grid(column=0,    row=1, pady=5)
colorbar.grid(column=0, row=2)
btnq.grid(column=0,     row=3, ipady=20)

# sketch.update()
# print(f'size of sketch: {sketch.winfo_width()}, {sketch.winfo_height()}')
# colorbar.update()
# print(f'size of colorbar: {colorbar.winfo_width()}')

root.mainloop()