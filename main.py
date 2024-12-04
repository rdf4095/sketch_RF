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
"""
import tkinter as tk
from tkinter import ttk

class Sketchpad(tk.Canvas):
    def __init__(self, parent, **kwargs):
        self.width = 320
        self.height = 320
        self.mode = 'freehand'    # or 'lines'
        self.background = '#ffa'
        self.linewidth = 1
        if 'width' in kwargs: self.width = kwargs['width']
        if 'height' in kwargs: self.height = kwargs['height']
        if 'mode' in kwargs: self.mode = kwargs['mode']
        if 'background' in kwargs: self.background = kwargs['background']
        if 'linewidth' in kwargs: self.linewidth = kwargs['linewidth']

        self.linecolor = 'black'

        super().__init__(parent,
                         width=self.width,
                         height=self.height,
                         background=self.background)

        self.firstx = 0
        self.firsty = 0
        self.startx = 0
        self.starty = 0
        self.previousx = 0
        self.previousy = 0

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
                # self.bind('ButtonRelease-1>', self.pen_up)


        self.bind("<Motion>", self.report_posn)
        self.bind("<Leave>", self.clear_posn)
        self.bind("<B1-Motion>", self.draw_path)

    # type Point = dict[int, int]
    # def add_point(self, xval: int, yval: int) -> Point:
    #     return {'x': xval, 'y': yval}
        def point_init(self, xval: int, yval: int):
            self.xval = xval
            self.yval = yval

        self.Point = type('Point', (), {"__init__": point_init})

    def set_start(self, event) -> None:
        # TODO: break this into two functions: only lines mode needs to append point.
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
        if self.firstx == 0 and self.firsty == 0:
            self.firstx, self.firsty = event.x, event.y
            print(f'set first: {self.firstx}, {self.firsty}')

        self.previousx, self.previousy = self.startx, self.starty
        self.startx, self.starty = event.x, event.y

        if self.mode != 'freehand':
            self.points.append(self.Point(event.x, event.y))
            print(f'point added: {self.points[-1].xval},{self.points[-1].yval}')


    def draw_line(self, event) -> None:
        """If past the starting position, draw a line from last posn to current posn."""
        if self.firstx == 0 and self.firsty == 0:
            self.set_start(event)
            return

        # print(f'    drawing from {self.startx},{self.starty} to {event.x},{event.y}')
        line_number = len(self.points)
        tagname = 'line' + str(line_number)
        self.create_line(self.startx, self.starty,
                         event.x, event.y,
                         fill=self.linecolor,
                         width=self.linewidth,
                         tags=tagname)

        self.linetags.append(tagname)
        self.set_start(event)

    def undo_line(self, event) -> None:
        print(f'last point: {self.points[-1].xval},{self.points[-1].yval}')
        print(f'last tagname: {self.linetags[-1]}')
        self.delete(self.linetags[-1])
        self.linetags.pop()
        self.points.pop()
        print(f'    last point: {self.points[-1].xval},{self.points[-1].yval}')
        print(f'    last tagname: {self.linetags[-1]}')

        self.startx, self.starty = self.previousx, self.previousy


    def double_click(self, event) -> None:
        """Draw a line from the current position to the starting position."""
        print(f'    connecting from {event.x},{event.y} to {self.firstx},{self.firsty}')
        self.create_line(event.x, event.y, self.firstx, self.firsty, fill=self.linecolor, width=self.linewidth)

        self.firstx, self.firsty = 0, 0


    def clear_posn(self, event) -> None:
        """Remove displayed cursor position."""
        self.delete('text1')


    def report_posn(self, event) -> None:
        """Display cursor position in lower right of canvas."""
        self.delete('text1')
        self.create_text(self.width - 24,
                         self.height - 10,
                         fill='blue',
                         text=str(event.x) + ',' + str(event.y),
                         tags='text1')


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



def set_color(ev):
    color_choice = colorbar.gettags('current')
    sketch.linecolor = color_choice[0]
    sketch_2.linecolor = color_choice[0]
    

def set_linewidth_1():
    # direct set:
    # sketch.linewidth = adj_linewidth.get()
    # use associated Int variable:
    sketch.linewidth = line_w1.get()


def set_linewidth_2():
    sketch_2.linewidth = line_w2.get()


root = tk.Tk()

sketch = Sketchpad(root)

sketch_2 = Sketchpad(root, height=200, background='#ccc', mode='lines')

# basic color selection for drawing
num_colors = 8      # not used yet
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'magenta', 'black']
xs = list(range(0, 320, 40))
y1 = 0
y2 = 42
colorbar = tk.Canvas(root, width=320, height=40)
for n, x in enumerate(xs):
    colorbar.create_rectangle(x, y1, x+40, y2, fill=colors[n], tags=colors[n])# + str(n))
    
colorbar.bind('<1>', set_color)


# For the sketch statusbar Frames that contain control widgets, I use tk
# widgets for the first canvas and ttk for the second.
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
lw1.pack(side='left', padx=5)

line_w1 = tk.IntVar(value=1)
adj_linewidth1 = ttk.Spinbox(controls_1,
                            width=3,
                            from_=1,
                            to=10,
                            values=linewidths,
                            wrap=True,
                            foreground='blue',
                            textvariable=line_w1,
                            command=set_linewidth_1)
adj_linewidth1.pack(side='left')
# --------- END controls 1


# controls for sketch 2 ----------
controls_2 = ttk.Frame(root, padding=2, relief='groove')

status2 = ttk.Label(controls_2, text='mode:')
status2.pack(side='left')

status2_value = ttk.Label(controls_2, foreground='blue', text=sketch_2.mode)
status2_value.pack(side='left')

cursor_posn2 = tk.Text(background='#ff0')

lw2 = ttk.Label(controls_2, text='line width:')
lw2.pack(side='left', padx=5)

line_w2 = tk.IntVar(value=1)
adj_linewidth2 = ttk.Spinbox(controls_2,
                            width=3,
                            from_=1,
                            to=10,
                            values=linewidths,
                            wrap=True,
                            foreground='blue',
                            textvariable=line_w2,
                            command=set_linewidth_2)
adj_linewidth2.pack(side='left')
# ---------- END controls 2


btnq = ttk.Button(root,
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

btnq.grid(column=0,           row=6, ipady=20)

# sketch.update()
# print(f'size of sketch: {sketch.winfo_width()}, {sketch.winfo_height()}')

# colorbar.update()
# print(f'size of colorbar: {colorbar.winfo_width()}')

if __name__ == '__main__':
    root.mainloop()
