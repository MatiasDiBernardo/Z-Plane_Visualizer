import numpy as np

RES = 400  #For easy val2pix mapping, resolution (RES) has to match the width of graph plane.

def e(w, root):
    return (np.exp(1j*w) - root)

def transfer_function(zeros, poles):
    w = np.linspace(-np.pi, np.pi, RES)

    num = np.ones(RES, dtype=complex)
    for zero in zeros:
        num *= e(w, zero)

    den = np.ones(RES, dtype=complex)
    for pole in poles:
        den *= e(w, pole)
    
    H_z = num/den

    mag = np.abs(H_z)
    ang = np.angle(H_z)

    return mag, ang

def values_to_pixels_mag(data_magnitude, x0, y0, H):
    #Linear mapping for y axis (assuming normalize magnitude)
    a = -H
    b = H + y0

    y_vals = a * data_magnitude + b
    mag_pixels = []
    
    for i in range(RES):
        y = round(y_vals[i])
        mag_pixels.append((x0 + i, y))
    
    return mag_pixels

def values_to_pixels_phase(data_phase, x0, y0, H):
    #Linear mapping for y axis (Phase is unwrapp between -pi and pi)
    a = -H/(2*np.pi)
    b = y0 + H/2

    y_vals = a * data_phase + b
    phase_pixels = []

    for i in range(RES):
        y = round(y_vals[i])
        phase_pixels.append((x0 + i, y))
    
    return phase_pixels

def magnitude_values(ceros, poles, x0, y0, H):
    """ Calculates the magnitude spectrum from ceros and poles and maps this values to
    to pixel coordinates to display in the gui.

    Args:
        ceros (list): List with ceros positions.
        poles (list): List with poles positions.
        x0 (int): X position of the graph.
        y0 (int): Y position of the graph.
        H (int): Heigth of the graph.
        symmetry (boolean): If the pole has a symmetry.
    Returns:
        list: List with pixels coordenates.
    """
    mag, phase = transfer_function(ceros, poles)
    mag = np.round(mag, 2)

    mag = mag/np.max(mag)  #Normalize to show always under the same reference.
    mag_pixels = values_to_pixels_mag(mag, x0, y0, H)

    return mag_pixels

def phase_values(ceros, poles, x0, y0, H):
    """ Calculates the phase from ceros and poles and maps this values to
    to pixel coordinates to display in the gui.

    Args:
        ceros (list): List with cero positions.
        poles (list): List with pole positions.
        x0 (int): X position of the graph.
        y0 (int): Y position of the graph.
        H (int): Heigth of the graph.
    Returns:
        list: List with pixels coordenates.
    """
    mag, phase = transfer_function(ceros, poles)
    phase_pixels = values_to_pixels_phase(phase, x0, y0, H)

    return phase_pixels
