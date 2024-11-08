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
"""

import tkinter as tk
from tkinter import ttk

class Sketchpad(tk.Canvas):
    def __init__(self, parent, **kwargs):
        self.startx = 0
        self.starty = 0
        self.lastx = 0
        self.lasty = 0

        self.linewidth = 2

        super().__init__(parent, **kwargs)
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
        print(f'starting: {self.startx},{self.starty}')


    def draw_line(self, event) -> None:
        """If past the starting position, draw a line from last posn to current posn."""
        if (self.startx == 0 and self.starty == 0):
            self.save_start_posn(event)
            self.save_posn(event)
            return
        
        self.create_line(self.lastx, self.lasty, event.x, event.y, fill='red', width=self.linewidth)
        self.save_posn(event)


    def connect_line(self, event) -> None:
        """Draw a line from the current position to the starting position."""
        # print('in end_line')
        # print(f'    drawing from {event.x},{event.y} to {self.startx},{self.starty}')
        self.create_line(event.x, event.y, self.startx, self.starty, fill='blue', width=self.linewidth)


    def draw_path(self, event) -> None:
        x_threshold = 1
        y_threshold = 1

        # draw with threshold for the amount of cursor movement
        if (abs(event.x - self.lastx) >= x_threshold and abs(event.y - self.lasty) >= y_threshold):
            self.create_line(self.lastx, self.lasty, event.x, event.y, fill='red', width=self.linewidth)
            self.save_posn(event)

        # always draw
        # if (abs(event.x - self.lastx) < threshold and abs(event.y - self.lasty) < threshold):
        #     self.create_line(self.lastx, self.lasty, event.x, event.y, fill='red', width=self.linewidth)
        #     self.save_posn(event)



root = tk.Tk()
# default_dims = "350x300"
# root.geometry (default_dims)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

sketch = Sketchpad(root, width=320, height=320, background='#ff0')
sketch.grid(column=0, row=0)

# canv2 = tk.Canvas(root, width=300, height=200, background='#fa0')
# there is a default canvas size
# canv2 = tk.Canvas(root, )#, background='#fa0')
# canv2.grid(column=0, row=1, pady=5)

colorbar = tk.Canvas(root, height=40)
colorbar.grid(column=0, row=1, sticky='ew')
colorbar.update()
# works:
# print(f'size of colorbar: {colorbar.winfo_width()}')

# fill canvas with 8 color samples
num_colors = 8      # not used yet
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'violet', 'magenta', 'black']
xs = list(range(0, 320, 40))
y1 = 0
y2 = 42
for n, x in enumerate(xs):
    colorbar.create_rectangle(x, y1, x+40, y2, fill=colors[n])

btnq = ttk.Button(root,
                  text="Quit",
                  command=root.quit,
                  style="MyButton1.TButton")
btnq.grid(column=0, row=2, ipady=20)

root.mainloop()