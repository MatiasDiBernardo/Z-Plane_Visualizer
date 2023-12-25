# Z-Plane Visualizer

The Z-Plane Visualizer is a GUI where the user can move poles and zeros in the Z Plane and observe the corresponding transfer function (magnitude and phase) for the current pole/cero distribution in real time. This project is designed as education material, offering students a practical tool to develop a profound understanding of pole/zero interactions in the Z plane. It is not created as a filter designing tool.

![](https://github.com/MatiasDiBernardo/Z-Plane_Visualizer/blob/main/images/demo.gif)

## Functionality

- Display and move poles/ceros: The user can select and choose the position of zero or pole in the Z plane. With the symmetry option active, all the poles and zeros selected or moved are attached to their symmetric par with respect to the imaginary axes.
- Order: The order of the poles/ceros can be modify with the mouse wheel up to increse or down to decrese. It supports up to order 4. The color of the cero/pole change with the order.
- Information: Holding the cursor over a pole or cero displays the information of position, symmetry and order.
- Zoom: With the plus and minus symbols, the user can zoom in and out of the Z plane. 
- Delete: The trash bin symbol clears all the poles and zeros from the plane, and the user can also delete specific poles or zeros pressing right click over it.
- Magnitude Graph: The magnitude spectrum display in the app is normalize, this decision helps to keep the focus on the shape of the magnitude and it makes sure that the graph is visually meaningful for the user. The downside is that the difference in values of the magnitude is not captured.
- Phase Graph: The phase is display unwrapped between -&\pi& and &\pi&. 

## Installation

First clone this repo and install the dependencies (Tested on Python 3.11.0).
```
git clone https://github.com/MatiasDiBernardo/Z-Plane_Visualizer
pip install -r requirements.txt
```
To execute the program.
```
python main.py
```

## Improvements 
- Add impulse response graph
- Add values and reference for the magnitude and phase plot
