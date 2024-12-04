# sketch_RF
An interactive drawing application (app)

## DEPENDENCIES
- **tkinter**, may have to be loaded on some linux distributions

## OPERATION
The app implements a class that extends the tkinter Canvas object. There
are two tkinter Canvases of arbitrary size, each of which responds to
various user actions, and demonstrates a different mode of drawing.

### Canvas 1
- **left mouse + drag**: draws a path that follows the cursor.

### Canvas 2
- **left mouse + drag**: draws a path that follows the cursor.
- **left mouse click**: successive clicks define lines between the clicked pixels.
- **left mouse double-click**: defines a line that joins the current point
  to the first point that was single-clicked.

A colorbar allows click-selection of line color, which apply to both Canvases.