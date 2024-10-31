import tkinter as tk
from tkinter import ttk

# class Sketchpad(tk.Canvas):
#     def __init__(self, parent, **kwargs):
#         super().__init__(parent, **kwargs)
#         self.bind("<Button-1>", self.save_posn)
#         self.bind("<B1-Motion>", self.add_line)
        
#     def save_posn(self, event):
#         print(f'mouse: {event.x}, {event.y}')
#         self.lastx, self.lasty = event.x, event.y
#         self.create_line(50, 50, 100,100, fill='red', width=2)

#     def add_line(self, event):
#         # self.create_line((self.lastx, self.lasty, event.x, event.y))
#         self.create_line(self.lastx, self.lasty, event.x, event.y, fill='red', width=2)
#         self.save_posn(event)

root = tk.Tk()
default_dims = "480x500"
root.geometry (default_dims)

# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)

# root.columnconfigure(1, weight=1)
# root.rowconfigure(1, weight=1)

# sketch = Sketchpad(root, width=300, height=300, background='white')
# sketch.grid(column=0, row=0, pady=5, sticky=(tk.N, tk.W, tk.E, tk.S))

canv2 = tk.Canvas(root, width=300, height=200, background='white')

# canv2.grid(column=0, row=0, pady=5)#, sticky=('n', 's', 'e', 'w'))
canv2.pack()
canv2.update()

btnq = ttk.Button(root,
                  text="Quit",
                  command=root.quit,
                  style="MyButton1.TButton")
btnq.pack(side="top", fill='x', padx=10)

root.mainloop()