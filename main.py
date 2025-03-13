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
11-20-2024  Add option to change line width for either canvas. Change each 
            sketchpad's statusbar to a Frame to report mode and linewidth.
            Display cursor position at lower right of each canvas.
            Remove some commented-out code.
11-30-2024  Fix minor Pycharm-detected formatting problems. Update README file.
12-02-2024  Debug double-click function(s).
12-04-2024  Add lists of lines & points clicked. For line mode, add undo_line()
            to delete the last line added.
12-14-2024  Put quit button in Frame, update some function docstrings.
12-17-2024  Edit .gitignore, update function docstrings. Define Sketchpad class
            with explicit parameters. (Move **kwargs code to notes.txt.) Add
            docstrings for Class and Class __init__ (incomplete).
12-19-2024  Pass textvariable to set_linewidth functions.
12-21-2024  Debug "undo" for line mode: can undo each line drawn, until the
            shape is closed, then the line list is reset. Add class attribute
            "line_count" for generating unique tag names.
03-11-2025  Use canvas/canvas_classes module for canvas classes.
"""
import tkinter as tk
from tkinter import ttk

from importlib.machinery import SourceFileLoader

cnv = SourceFileLoader("cnv_classes", "../canvas/canvas_classes.py").load_module()

def set_color(event, cb, canv):
    """Set color for lines drawn on canvases.

    Parameters:
        event: widget event bound to this function
        cb : colorbar object
        canv : canvas object
    """
    # print(f'handling event {event}')
    # print(f' set_color on canv: {canv.name}')
    color_choice = cb.gettags('current')[0]

    canv.linecolor = color_choice
    report_color(canv, color_choice)


def report_color(canv, textstr) -> None:
    """Display line color in lower left of canvas."""
    canv.delete('color_text')
    canv.create_text(10,
                     canv.height - 10,
                     fill=textstr,
                     text=textstr,
                     anchor='w',
                     tags='color_text')


def set_linewidth(var):
    """Set line width for lines or shapes on a canvas.

    parameter:
        var : line width, from the IntVar in adj_linewidth.
    """
    mydrawcanvas.linewidth = var.get()


root = tk.Tk()

# sketch = Sketchpad(root)
# works:
# print(f'widgetName, _name: {sketch.widgetName}, {sketch._name}')
sketch = cnv.DrawCanvas(root, mode='freehand', background='#ffc')

# sketch_2 = Sketchpad(root, height=200, background='#ccc', mode='lines')
sketch_2 = cnv.DrawCanvas(root, mode='lines', height=300, background='#ccc')

num_colors = 8      # not used yet
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'magenta', 'black']
xs = list(range(0, 320, 40))
y1 = 0
y2 = 42
colorbar = tk.Canvas(root, width=320, height=40)
for n, x in enumerate(xs):
    colorbar.create_rectangle(x, y1, x+40, y2, fill=colors[n], tags=colors[n])# + str(n))
    
colorbar.bind('<1>', lambda ev, cb=colorbar, canv=sketch: set_color(ev, cb, canv))

linewidths = [str(i) for i in list(range(1,11))]

# controls for sketch 1 ---------
controls_1 = tk.Frame(root, border=1, relief='ridge')

status1 = ttk.Label(controls_1, text='mode:')
status1.pack(side='left')

status1_value = ttk.Label(controls_1, foreground='blue', text=sketch.mode)
status1_value.pack(side='left')

lw1 = ttk.Label(controls_1, text='line width:')

line_w1 = tk.IntVar(value=1)
adj_linewidth1 = ttk.Spinbox(controls_1,
                            width=3,
                            from_=1,
                            to=10,
                            values=linewidths,
                            wrap=True,
                            foreground='blue',
                            textvariable=line_w1,
                            command=lambda var=line_w1: set_linewidth_1(var))
adj_linewidth1.pack(side='right', pady=5)
lw1.pack(side='right', padx=5)
# --------- END controls 1


# controls for sketch 2 ----------
controls_2 = ttk.Frame(root, padding=2, relief='groove')

status2 = ttk.Label(controls_2, text='mode:')
status2.pack(side='left')

status2_value = ttk.Label(controls_2, foreground='blue', text=sketch_2.mode)
status2_value.pack(side='left')

cursor_posn2 = tk.Text(background='#ff0')

lw2 = ttk.Label(controls_2, text='line width:')

line_w2 = tk.IntVar(value=1)
adj_linewidth2 = ttk.Spinbox(controls_2,
                            width=3,
                            from_=1,
                            to=10,
                            values=linewidths,
                            wrap=True,
                            foreground='blue',
                            textvariable=line_w2,
                            command=lambda var=line_w2: set_linewidth_2(var))
adj_linewidth2.pack(side='right', pady=5)
lw2.pack(side='right', padx=5)
# ---------- END controls 2

quit_fr = ttk.Frame(root)
btnq = ttk.Button(quit_fr,
                  text="Quit",
                  command=root.quit,
                  style="MyButton1.TButton")

sketch.grid(column=0,         row=0)
controls_1.grid(column=0,     row=1, sticky='ew')
spacer = tk.Frame(root, height=10)
spacer.grid(column=0,         row=2)

sketch_2.grid(column=0,       row=3)
controls_2.grid(column=0,     row=4, sticky='ew')
colorbar.grid(column=0,       row=5, pady=10)

# btnq.grid(column=0,           row=6, ipady=10)
btnq.pack()
quit_fr.grid(column=0, row=6, pady=10)


# sketch.update()
# print(f'size of sketch: {sketch.winfo_width()}, {sketch.winfo_height()}')

# colorbar.update()
# print(f'size of colorbar: {colorbar.winfo_width()}')

if __name__ == '__main__':
    root.mainloop()
