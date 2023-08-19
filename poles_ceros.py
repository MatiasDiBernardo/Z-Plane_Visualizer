import pygame
import numpy as np

class Pole():
    def __init__(self, pole_size, position, value_pos, value_pos_sym, symmetry, y_start, plane_size, order=1):
        self.pole_size = pole_size
        self.type = "Pole"
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
    
    def update_values(self, pos, value_pos, value_sym):
        self.position = pos
        self.position_sym = self.pos_symmetry(pos)
        self.value = self.get_value(value_pos)
        self.value_sym = self.get_value(value_sym)
        self.rect = self.get_rect(pos)
        self.rect_sym = self.get_rect(self.position_sym)
 
    def values(self):
        info = {"Position": self.position, 
                "Value": self.value,
                "Rect": self.rect,
                "Symmetry": self.symmetry,
                "Order": self.order}
        
        return info

    def pole_draw(self, win, pos, color):
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
        BUG: En el caso que delta_y = 0 ya que pos == pos_sym. En la parte visual como se superponen no hay problema, el tema es en
        el calculo ya que por la lógica de la parte de graficos me tomaria como si habría dos polos, y en la funcion transferencia 
        es veria representado (en el breve instante en que paso sobre el origen).Osea sería como un polo de segundo order cuando en
        realidad tendría que ser de primer order.

        """
        pos_sym = (pos[0], pos[1] + 2 * delta_y)
        
        return pos_sym
    
    def draw_unassigned(self, win, pos, color):
        #For the selection process when pole is display buy unassigned
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
        #For the selection process when pole is display buy unassigned
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
