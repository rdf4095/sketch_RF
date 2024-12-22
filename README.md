# sketch_RF
An interactive drawing application

## DEPENDENCIES
- **tkinter**, may have to be loaded on some linux distributions

## OPERATION
Two drawing canvases are presented, in which you can draw with the mouse. In
the upper canvas, drawing is freehand, following mouse moves with L-button drag.
In the lower canvas, drawing is based on L-mouse clicks. Clicking successive points draws 
lines between them, a R-click removes the last line drawn, and double-L-click draws a 
line back to the first point clicked, "closing" a shape. 

### Canvas 1
- **left mouse + drag**: draws a path that follows the cursor.

### Canvas 2
- **left mouse click**: successive clicks define lines between the clicked pixels.
- **left mouse double-click**: defines a line that joins the current point
  to the first point that was single-clicked.

A colorbar allows click-selection of line color, which apply to both Canvases.

## BACKGROUND
The app implements a class that extends the tkinter Canvas object. There
are two tkinter Canvases of arbitrary size, which demonstrate different modes of 
drawing.
