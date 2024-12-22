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
"""
import tkinter as tk
from tkinter import ttk

class Sketchpad(tk.Canvas):
    """
    Sketchpad : Defines a Canvas for interactive drawing.

    Extends: tk.Canvas

    Attributes
    ----------

    Methods
    -------
    method_1:
        text
    """
    def __init__(self, parent,
                       width=320,
                       height=320,
                       mode='freehand',
                       background='#ffa',
                       linewidth=1
                 ):
        """
        Inits a Sketchpad object.

        Parameters
        ----------
        width : Int
            Canvas width.
        height : Int
            Canvas height.

        Methods
        -------
        point_init:
            Defines a Point object for x-y Canvas position.
        """

        self.width = width
        self.height = height
        self.mode = mode
        self.background = background
        self.linewidth = linewidth

        super().__init__(parent,
                         width=self.width,
                         height=self.height,
                         background=self.background)

        self.linecolor = 'black'
        self.firstx = 0
        self.firsty = 0
        self.startx = 0
        self.starty = 0
        self.previousx = 0
        self.previousy = 0
        self.line_count = 0
        self.points = []
        self.linetags = []

        if self.mode == 'freehand':
            self.bind('<Button-1>', self.set_start)
            # self.bind('<Double-1>', self.double_click)
            # self.bind('<ButtonRelease-1>', self.pen_up)
        else:
            if self.mode == 'lines':
                self.bind('<Button-1>', self.draw_line)
                self.bind('<Double-1>', self.double_click)
                self.bind('<Button-3>', self.undo_line)

        self.bind("<Motion>", self.report_posn)
        self.bind("<Leave>", self.clear_posn)
        self.bind("<B1-Motion>", self.draw_path)

        def point_init(thispoint, xval: int, yval: int):
            thispoint.xval = xval
            thispoint.yval = yval

        self.Point = type('Point', (), {"__init__": point_init})

    def set_start(self, event) -> None:
        """Handler for L-mouse click in freehand mode: save initial cursor
        position (firstx,y) and next position clicked after closing a figure in
        line mode (startx,y). Also used in line mode to reset the start posn.
        """
        if self.firstx == 0 and self.firsty == 0:
            self.firstx, self.firsty = event.x, event.y
        else:
            self.previousx, self.previousy = self.startx, self.starty

        self.startx, self.starty = event.x, event.y

        if self.mode == 'lines':
            self.points.append(self.Point(event.x, event.y))
            # print(f'point added: {self.points[-1].xval},{self.points[-1].yval}')


    def draw_line(self, event) -> None:
        """Handler for L-mouse click in line mode. If past the starting position,
        draw a line from last posn to current posn.
        """
        if self.firstx == 0 and self.firsty == 0:
            self.set_start(event)
            return

        self.line_count += 1
        # line_number = self.line_count + 1#len(self.points)
        tagname = 'line' + str(self.line_count)
        self.create_line(self.startx, self.starty,
                         event.x, event.y,
                         fill=self.linecolor,
                         width=self.linewidth,
                         tags=tagname)

        self.linetags.append(tagname)
        self.set_start(event)


    def double_click(self, event) -> None:
        """Handler for L mouse double-click, in line mode. First, the single-click
        handler draws a line from the current position to the start posn. Then,
        this handler draws a line from the current to the previous position.
        """
        # print(f'    connecting from {event.x},{event.y} to {self.firstx},{self.firsty}')
        self.line_count += 1
        # line_number = self.line_count + 1#len(self.points)
        tagname = 'line' + str(self.line_count)
        self.create_line(event.x, event.y,
                         self.firstx, self.firsty,
                         fill=self.linecolor,
                         width=self.linewidth,
                         tags=tagname)
        self.linetags.append(tagname)
        print(f'linetags: {self.linetags}')

        # try (don't think this is necessary)
        # self.startx, self.starty = self.previousx, self.previousy

        self.firstx, self.firsty = 0, 0

        # the current shape is closed, forget its points and lines
        self.points = []
        self.linetags = []


    def undo_line(self, event) -> None:
        """Handler for R-mouse click. In line mode, remove last line and make
        previous cursor position the current position for connecting new lines.
        """
        if (self.firstx, self.firsty) == (0, 0):
            return

        if len(self.linetags) > 0:
            # print(f'linetags: {self.linetags}')
            self.delete(self.linetags[-1])
            self.linetags.pop()
        if len(self.points) > 0:
            # print(f'points: {self.points}')
            self.points.pop()
            if len(self.points) >= 1:
                self.startx, self.starty = self.points[-1].xval, self.points[-1].yval


    def clear_posn(self, event) -> None:
        """Remove displayed cursor position from the canvas."""
        self.delete('text1')


    def report_posn(self, event) -> None:
        """Display cursor position in lower right of canvas."""
        self.delete('text1')
        self.create_text(self.width - 24,
                         self.height - 10,
                         fill='blue',
                         text=str(event.x) + ',' + str(event.y),
                         tags='text1')


    def report_color(self, textstr) -> None:
        """Display cursor position in lower right of canvas."""
        self.delete('text2')
        self.create_text(24,
                         self.height - 10,
                         fill=str,
                         text=textstr,
                         tags='text2')


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
        # xvar = event.x - self.startx
        # if xvar <= x_threshold:
        #     self.create_line(self.startx, self.starty, event.x - xvar, event.y, fill=self.linecolor, width=self.linewidth)

        # print(f'{event.x}, {event.y}')

        # no x or y change threshold
        self.create_line(self.startx, self.starty, event.x, event.y, fill=self.linecolor, width=self.linewidth)
        self.report_posn(event)
        self.set_start(event)

# END Class Sketchpad ==========


def set_color(event):
    """Set drawing color for both canvases."""
    color_choice = colorbar.gettags('current')
    print(f'color: {color_choice}')
    sketch.linecolor = color_choice[0]
    sketch_2.linecolor = color_choice[0]

    sketch.report_color(color_choice[0])
    

def set_linewidth_1(var):
    """Set line width for canvas 1 (freehand)."""
    sketch.linewidth = var.get()


def set_linewidth_2(var):
    """Set line width for canvas 2 (lines)."""
    sketch_2.linewidth = var.get()


root = tk.Tk()

sketch = Sketchpad(root)
# works:
# print(f'widgetName, _name: {sketch.widgetName}, {sketch._name}')

sketch_2 = Sketchpad(root, height=200, background='#ccc', mode='lines')

num_colors = 8      # not used yet
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'magenta', 'black']
xs = list(range(0, 320, 40))
y1 = 0
y2 = 42
colorbar = tk.Canvas(root, width=320, height=40)
for n, x in enumerate(xs):
    colorbar.create_rectangle(x, y1, x+40, y2, fill=colors[n], tags=colors[n])# + str(n))
    
colorbar.bind('<1>', set_color)


# For the sketch statusbars that contain control widgets, I use tk
# widgets for the first canvas and ttk for the second, just to demonstrate.
#   for tk Frames:
#       - For a visible border, use 'relief' and 'border' attributes
#       - can use 'highlightthickness' and 'highlightbackground' attributes
#   for ttk Frames:
#       - For a visible border, use 'relief' and 'padding' attributes
#       - 'padding' is internal to the Frame

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
