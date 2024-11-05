"""
program: main.py

purpose: For projecct sketch_RF.
         Interactive drawing.

comments: Supports freehand drawing by following cursor movement,
          or polygonal lines by drawing from mouse-click to mouse-click.

author: Russell Folks

history:
-------
10-31-2024  creation
11-04-2024  In draw_line, allow "closing" to the start point.
            Add mouse movement threshold for freehand drawing
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
        self.bind("<Double-1>", self.end_line)
        self.bind("<B1-Motion>", self.draw_path)
        
    def save_posn(self, event):
        """
        the mouse cursor position (posn) attributes depend on context:
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


    def save_start_posn(self, event):
        # pass
        self.startx, self.starty = event.x, event.y
        print(f'starting: {self.startx},{self.starty}')


    def draw_line(self, event) -> None:
        if (self.startx == 0 and self.starty == 0):
            # print('    no startx, saving it')
            self.save_start_posn(event)
            return
        
        if (self.lastx == 0 and self.lasty == 0):
            # print('    no lastx, saving it')
            self.save_posn(event)
            self.create_line(self.startx, self.starty, event.x, event.y, fill='red', width=self.linewidth)
            return

        # print('    drawing line')
        self.create_line(self.lastx, self.lasty, event.x, event.y, fill='red', width=self.linewidth)
        self.save_posn(event)


    def end_line(self, event):
        # print('in end_line')
        # print(f'    drawing from {event.x},{event.y} to {self.startx},{self.starty}')
        self.create_line(event.x, event.y, self.startx, self.starty, fill='blue', width=self.linewidth)


    def draw_path(self, event):
        threshold = 4
        # print('    drawing path:')
        # print(f'    {self.lastx},{self.lasty} to {event.x},{event.y}')
        if (abs(event.x - self.lastx) > threshold and abs(event.y - self.lasty) > threshold):
            self.create_line(self.lastx, self.lasty, event.x, event.y, fill='red', width=self.linewidth)
            self.save_posn(event)


root = tk.Tk()
# default_dims = "350x300"
# root.geometry (default_dims)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

sketch = Sketchpad(root, width=300, height=300, background='#ff0')
# 'sticky' expands the canvas to size of parent
# sketch.grid(column=0, row=0, pady=5, sticky=(tk.N, tk.W, tk.E, tk.S))
sketch.grid(column=0, row=0, pady=5)

# canv2 = tk.Canvas(root, width=300, height=200, background='#fa0')
# there is a default size
canv2 = tk.Canvas(root, background='#fa0')

# 'sticky' expands the canvas to size of parent
canv2.grid(column=0, row=1, pady=5, sticky=('n', 's', 'e', 'w'))
# canv2.grid(column=0, row=1, pady=5)

# canv2.grid(column=0, row=1, padx=5, pady=5)

# canv2.update()

btnq = ttk.Button(root,
                  text="Quit",
                  command=root.quit,
                  style="MyButton1.TButton")
btnq.grid(column=0, row=2, ipady=20)

root.mainloop()