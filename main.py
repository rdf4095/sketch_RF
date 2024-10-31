"""
program: main.py

purpose: For projecct sketch_RF.
         Interactive drawing application.

comments: 

author: Russell Folks

history:
-------
10-31-2024  creation
"""

import tkinter as tk
from tkinter import ttk

class Sketchpad(tk.Canvas):
    def __init__(self, parent, **kwargs):
        self.startx = 0
        self.starty = 0
        self.lastx = 0
        self.lasty = 0

        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.draw_line)
        self.bind("<Double-1>", self.end_line)
        self.bind("<B1-Motion>", self.draw_path)
        
    def save_posn(self, event):
        """
        the mouse cursor position attributes depends on context:
        .winfo_pointerx,y is the position of cursor relative to the screen.
        .winfo_rootx,y is the position of root relative to the screen.
        event.x,y is the position of cursor relative to the root window.

        Notes: - the OS reserves the top 25 pixels or so for the "permanent" app menubar,
                 so y=0 corresponds to the next pixel below this.
               - root.winfo_rootx,y does not include padding used by the geometry manager.
                 So, winfo_pointerx = event.x + winfo_rootx + ipadx + padx.
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


    def draw_line(self, event):
        print()
        # if hasattr(self, 'lastx'):
        if (self.lastx != 0 and self.lasty != 0):
            print(f'start, last: ')
            self.create_line(self.lastx, self.lasty, event.x, event.y, fill='red', width=2)
            self.save_posn(event)
            self.save_start_posn(event)
        else:
            print('no lastx')
            self.save_posn(event)


    def end_line(self, event):
        print('in end_line')
        self.create_line(event.x, event.y, self.startx, self.starty, fill='blue', width=1)


    def draw_path(self, event):
        print(f'start, last: ')
        self.create_line(self.lastx, self.lasty, event.x, event.y, fill='red', width=2)
        self.save_posn(event)


root = tk.Tk()
# default_dims = "350x300"
# root.geometry (default_dims)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

sketch = Sketchpad(root, width=300, height=300, background='#ff0')
sketch.grid(column=0, row=0, pady=5)#, sticky=(tk.N, tk.W, tk.E, tk.S))

canv2 = tk.Canvas(root, width=300, height=200, background='#fa0')

# canv2.grid(column=0, row=0, pady=5)#, sticky=('n', 's', 'e', 'w'))
# canv2.pack(padx=10, pady=10)
canv2.grid(column=0, row=1, padx=5, pady=5)
# canv2.update()

btnq = ttk.Button(root,
                  text="Quit",
                  command=root.quit,
                  style="MyButton1.TButton")
# btnq.pack(side="top", fill='x', padx=10)
btnq.grid(column=0, row=2, ipady=20)
root.mainloop()