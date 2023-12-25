import pygame
import numpy as np

class Pole():
    """This class represents a pole. It contains all the math for the value calculations and
    functionality for interacting with the pole itself.

    Args:
        position (tuple(x,y)): Is the position in pixels of the Pole.
        value_pos (tuple(x,y)): Is the value on the complex plane corresponding to the
        pixel position. 
        value_pos_sym (tuple(x,y)): Is the complex conjugate of value_pos. 
        rect (pygame.rect): Is the entity used to handle mouse detection and collision.

    """
    def __init__(self, pole_size, position, value_pos, value_pos_sym, symmetry, y_start, plane_size, order=1):
        # Constant values
        self.pole_size = pole_size  # Dimension of the pole in pixels
        self.type = "Pole"
        self.y_start = y_start  # Starting point of the z plane in pixels
        self.plane_size = plane_size  # Width of the z plane in pixels
        self.symmetry = symmetry  # Boolean that indicats if the pole is symetric or not.
        self.order = order  # Order of the pole
        self.moved = False

        # Update values
        self.position = position
        self.position_sym = self.pos_symmetry(position)
        self.value = self.get_value(value_pos)
        self.value_sym = np.conjugate(self.value)  #Use one value as reference to avoid numerical error
        self.rect = self.get_rect(position)
        self.rect_sym = self.get_rect(self.position_sym)
    
    def update_values(self, new_pos, new_value_pos, new_value_sym):
        self.position = new_pos
        self.position_sym = self.pos_symmetry(new_pos)
        self.value = self.get_value(new_value_pos)
        self.value_sym = np.conjugate(self.value)
        self.rect = self.get_rect(new_pos)
        self.rect_sym = self.get_rect(self.position_sym)
 
    def values(self):
        info = {"Position": self.position, 
                "Value": self.value,
                "Rect": self.rect,
                "Symmetry": self.symmetry,
                "Order": self.order}
        
        return info

    def pole_draw(self, win, pos, color):
        # Draws and X on the plane at the position (pos)
        delta = self.pole_size // 2
        l1 = (pos[0] - delta, pos[1] - delta)
        l2 = (pos[0] + delta, pos[1] + delta)
        pygame.draw.line(win, color, l1, l2, width=1)
        
        l3 = (pos[0] - delta, pos[1] + delta)
        l4 = (pos[0] + delta, pos[1] - delta)
        pygame.draw.line(win, color, l3, l4, width=1)
    
    def pos_symmetry(self, pos):
        y_mid = self.y_start + self.plane_size//2  #Origin in Y coordinate
        delta_y = y_mid - pos[1]
        """
        Small bug: In the case where delta_y = 0 then pos == pos.sym. With the current logic this creates two poles
        in the origin an it should be just one. This it is going to be reflected on the transfer function as a 
        pole of second order (in the short time that the pole pass trougth the origin).
        
        I leave it like this because is really picky edge case and the solutions that I tried lead to more issues but 
        it could be improved. 
        
        """
        pos_sym = (pos[0], pos[1] + 2 * delta_y)
        
        return pos_sym
    
    def draw_unassigned(self, win, pos, color):
        #For the selection process when pole is display but unassigned
        if self.symmetry:
            pos_sym = self.pos_symmetry(pos)
            self.pole_draw(win, pos, color)
            self.pole_draw(win, pos_sym, color)
        else:
            self.pole_draw(win, pos, color)

    def draw(self, win, color):
        if self.symmetry:
            self.pole_draw(win, self.position, color)
            self.pole_draw(win, self.position_sym, color)
        else:
            self.pole_draw(win, self.position, color)

    def get_value(self, value_pos):
        #From x, y coordinates to imaginary value
        x, y = value_pos

        if (x != None) and (y != None):  #Checks if is a valid value
            val = x + 1j*y
        else:
            val = None

        return val

    def get_rect(self, pos):
        #Create rect entity (size of the pole) for collision detection
        delta = self.pole_size // 2
        x1 = pos[0] - delta
        y1 = pos[1] - delta
        return pygame.Rect(x1, y1, self.pole_size, self.pole_size)

class Cero(Pole):
    def __init__(self, pole_size, position, value_pos, value_pos_sym, symmetry, y_start, plane_size, order=1):
        super().__init__(pole_size, position, value_pos, value_pos_sym, symmetry, y_start, plane_size, order)
        self.pole_size = pole_size
        self.type = "Cero"
        self.y_start = y_start
        self.plane_size = plane_size
        self.symmetry = symmetry
        self.order = order
        self.moved = False

        self.position = position
        self.position_sym = self.pos_symmetry(position)
        self.value = self.get_value(value_pos)
        self.value_sym = self.get_value(value_pos_sym)
        self.rect = self.get_rect(position)
        self.rect_sym = self.get_rect(self.position_sym)

    def cero_draw(self, win, pos, color):
        pygame.draw.circle(win, color, pos, self.pole_size - 1, width=1)

    def draw_unassigned(self, win, pos, color):
        #For the selection process when pole is display but unassigned
        if self.symmetry:
            pos_sym = self.pos_symmetry(pos)
            self.cero_draw(win, pos, color)
            self.cero_draw(win, pos_sym, color)
        else:
            self.cero_draw(win, pos, color)

    def draw(self, win, color):
        if self.symmetry:
            self.cero_draw(win, self.position, color)
            self.cero_draw(win, self.position_sym, color)
        else:
            self.cero_draw(win, self.position, color)
