# Z-Plane Visualizer

The Z-Plane Visualizer is a GUI where the user can move poles and zeros in the Z Plane and observe the corresponding transfer function (magnitude and phase) for the current pole/zero distribution in real time.

This project is designed as educational material, offering students a practical tool to develop a profound understanding of pole/zero interactions in the Z plane. It is not created as a filter designing tool.

![](https://github.com/MatiasDiBernardo/Z-Plane_Visualizer/blob/main/images/demo.gif)

## Functionality

- Display and move poles/zeros: The user can select and choose the position of zero or pole in the Z plane. With the symmetry option active, all the poles and zeros selected or moved are attached to their symmetric par with respect to the imaginary axes.

- Order: The order of the poles/zeros can be modified with the mouse wheel up to increse or down to decrease. It supports up to order 4. The color of the zero/pole change with the order.

- Information: Holding the cursor over a pole or zero displays information about the position, symmetry and order.

- Zoom: With the plus and minus symbols, the user can zoom in and out of the Z plane. 

- Delete: The trash bin symbol clears all the poles and zeros from the plane, and the user can also delete specific poles or zeros by pressing right click on them.

- Magnitude Graph: The magnitude spectrum displayed in the app is normalized. This decision helps to keep the focus on the shape of the magnitude and it makes sure that the graph is visually meaningful for the user. The downside is that the difference in peak values is not captured.

- Phase Graph: The phase is displayed unwrapped between -pi and pi. 

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

## To do
- Add impulse response graph
  
- Add values and reference for the magnitude and phase plot
