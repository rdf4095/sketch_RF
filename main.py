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
03-31-2025  Add canvas parameter to set_linewidth().
06-12-2025  Use utilities/tool_classes.py for widget classes.
"""
"""
TODO
    1. ? should be a separate colorbar for each canvas.
"""
import tkinter as tk
from tkinter import ttk

from importlib.machinery import SourceFileLoader

cnv = SourceFileLoader("cnv_classes", "../canvas/canvas_classes.py").load_module()
tc = SourceFileLoader("tools", "../utilities/tool_classes.py").load_module()

def set_color(event, canv, cb):
    """Set color for lines drawn on canvases.

    Parameters:
        event: widget event bound to this function
        cb : colorbar object
        canv : canvas object
    """
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


def set_linewidth(canv, var):
    """Set line width for lines or shapes on a canvas.

    parameter:
        var : line width, from the IntVar in adj_linewidth.
    """
    canv.linewidth = var.get()


root = tk.Tk()

sketch = cnv.DrawCanvas(root, mode='freehand', background='#ffc')
# works for introspection:
# print(f'for sketch: {sketch.widgetName=}, {sketch._name=}')

sketch_2 = cnv.DrawCanvas(root, mode='lines', height=300, background='#ccc')

linewidths = [str(i) for i in list(range(1,11))]

num_colors = 8      # not used yet
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'magenta', 'black']
xs = list(range(0, 320, 40))
y1 = 0
y2 = 42
colorbar = tk.Canvas(root, width=320, height=40)
for n, x in enumerate(xs):
    colorbar.create_rectangle(x, y1, x+40, y2, fill=colors[n], tags=colors[n])# + str(n))
    
colorbar.bind('<1>', lambda ev, canv=sketch, cb=colorbar: set_color(ev, canv, cb))


# controls for sketch 1 ---------
controls_1 = tk.Frame(root, border=1, relief='raised')

status_frame1 = tk.Frame(controls_1)
status1 = ttk.Label(status_frame1, text='mode:')
status1.grid(column=0, row=0, sticky='w')

status1_value = ttk.Label(status_frame1, foreground='blue', text=sketch.mode)
status1_value.grid(column=1, row=0)

line_w1 = tk.IntVar(value=1)
lw1 = tc.SpinboxFrame(controls_1,
                      sb_values=linewidths,
                      display_name='Line width:',
                      var=line_w1,
                      callb=lambda canv=sketch, var=line_w1: set_linewidth(canv, var),
                      posn=[1, 0],
                      stick='e'
                      )

controls_1.grid(column=0, row=1, sticky='ew')
controls_1.columnconfigure(0, weight=1)
controls_1.columnconfigure(1, weight=1)

status_frame1.grid(column=0, row=0, sticky='w')

# --------- END controls 1

# controls for sketch 2 ----------
controls_2 = ttk.Frame(root, padding=2, relief='groove')

status_frame2 = ttk.Frame(controls_2)
status2 = ttk.Label(status_frame2, text='mode:')
status2.grid(column=0, row=3, sticky='w')

status2_value = ttk.Label(status_frame2, foreground='blue', text=sketch_2.mode)
status2_value.grid(column=1, row=3)

cursor_posn2 = tk.Text(background='#ff0')

line_w2 = tk.IntVar(value=1)
lw2 = tc.SpinboxFrame(controls_2,
                      sb_values=linewidths,
                      display_name='Line width:',
                      var=line_w2,
                      callb=lambda canv=sketch_2, var=line_w2: set_linewidth(canv, var),
                      posn=[1, 0],
                      stick='e'
                      )

controls_2.grid(column=0, row=4, sticky='ew')
controls_2.columnconfigure(0, weight=1)
controls_2.columnconfigure(1, weight=1)

status_frame2.grid(column=0, row=0, sticky='w')

# ---------- END controls 2

quit_fr = ttk.Frame(root)
btnq = ttk.Button(quit_fr,
                  text="Quit",
                  command=root.quit,
                  style="MyButton1.TButton")

sketch.grid(column=0,         row=0)
spacer = tk.Frame(root, height=10)
spacer.grid(column=0,         row=2)

sketch_2.grid(column=0,       row=3)

colorbar.grid(column=0,       row=5, pady=10)

# why not use .grid?
# btnq.grid(column=0,           row=6, ipady=10)
btnq.pack()

quit_fr.grid(column=0, row=6, pady=10)

if __name__ == '__main__':
    root.mainloop()
