# Z-Plane Visualizer

The Z-Plane Visualizer is a GUI where the user can move poles and zeros in the Z Plane and observe the corresponding transfer function and phase for the current pole/cero distribution in real time. The objective of this project is to serve as an educational tool for students looking for a program that helps you to develop intuition about the pole/zero interaction in the Z plane. It is not created as a filter designing tool.

![](https://github.com/MatiasDiBernardo/Z-Plane_Visualizer/blob/main/images/readme_gif.gif)

## Functionality

The user can select and choose the position of zero or pole in the Z plane. With the symmetry option active, all the poles and zeros selected or moved are attached to his symmetric par respect to the imaginary axes.
With the plus and minus symbols, the user can zoom in and out of the Z plane. The trash bin symbol clears all the poles and zeros from the plane, and the user can also delete specific poles or zeros pressing right click over it. 
The magnitude spectrum display in the app is normalize, this decision helps to keep the focus on the shape of the magnitude and it makes sure that the graph is visually meaningful for the user. The downside is that the difference in values of the magnitude is not captured.
The phase is display unwrapped between -&\pi& and &\pi&. 

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
Limitations of the current implementation, improvements and bugs.
- Add double pole or zero feature
- Add impulse response graph
- Add values and reference for the magnitude and phase plot
- Fix bug (check and uncheck symmetry error)
- Improve GUI
- Refactor
