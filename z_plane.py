import pygame
import numpy as np
from poles_ceros import Pole, Cero

class ZPlane():
    def __init__(self, x_start, y_start, font):
        self.x_start = x_start  #Starting position (upper left)
        self.y_start = y_start
        self.plane_size = 400  #Size of the Z Plane
        self.poles_size = 10  #Dimension of poles in pixels (same for ceros)
        self.font = font
        self.background_color = (15, 15, 15)  #For the Z plane
        self.withe = (255, 255, 255)

        self.zoom = 3  #Starting zoom index value
        self.symmetry = False
        self.center_plane = (x_start + self.plane_size // 2, y_start + self.plane_size // 2) 

        self.items = []  #List with pole or cero objetcs
        self.clicked = False  #To catch and keep track of different actions (button functionality)
        self.emptyPole = Pole(self.poles_size, (0,0), (0,0), (0,0), False, y_start, self.plane_size)  #For unassigned display
        self.emptyCero = Cero(self.poles_size, (0,0), (0,0), (0,0), False, y_start, self.plane_size)

    def default_background(self, win):
        #Background
        pygame.draw.rect(win, self.background_color, (self.x_start, self.y_start, self.plane_size,self.plane_size))

        #Unit circle
        zoom_values = [150, 100, 50, 20, 10, 2]  #List of different zoom values
        self.margin = zoom_values[self.zoom]  #Zoom effect is control with the margin length in pixels

        radius = self.plane_size//2 - self.margin
        pygame.draw.circle(win, self.withe, self.center_plane, radius, width=1)

        #XY Lines
        color_lines = (99, 99, 99)
        x1 = self.x_start + self.margin
        y1 = self.y_start + self.plane_size // 2
        x2 = self.x_start + self.plane_size - self.margin
        pygame.draw.line(win, color_lines, (x1, y1), (x2, y1))
        x3 = self.x_start + self.plane_size // 2
        y3 = self.y_start + self.margin
        y4 = self.y_start + self.plane_size - self.margin
        pygame.draw.line(win, color_lines, (x3, y3), (x3, y4))
    
    def zoom_plane_in(self):
        zoom_values = [150, 100, 50, 20, 10, 2]
        if self.zoom < len(zoom_values) - 1:
            self.zoom += 1

    def zoom_plane_out(self):
        if self.zoom > 0:
            self.zoom -= 1

    def clear_zplane(self):
        self.items = []
    
    def graph_cero(self, win, pos, color):
        self.emptyCero.draw_unassigned(win, pos, color)
    
    def graph_pole(self, win, pos, color):
        self.emptyPole.draw_unassigned(win, pos, color)
    
    def pos_in_plane(self, pos):
        #Checks if the position of the mouse is inside the Z Plane boundries.
        x_cor = False
        if pos[0] > self.x_start and pos[0] < (self.x_start + self.plane_size):
            x_cor = True 
        y_cor = False
        if pos[1] > self.y_start and pos[1] < (self.y_start + self.plane_size):
            y_cor = True
        
        if x_cor and y_cor:
            return True
        else:
            return False

    def poles_and_ceros_display(self, win):
        for item in self.items:
            item.draw(win, self.withe)
    
    def detect_collition(self, item, pos):
        mouse_collition = False
        if item.symmetry:
            if item.rect.collidepoint(pos) or item.rect_sym.collidepoint(pos):
                mouse_collition = True
        else:
            if item.rect.collidepoint(pos):
                mouse_collition = True
        
        return mouse_collition
    
    def change_color_when_over(self, win, item, color_change):
        # Draws unassing pole or cero over the item
        if item.symmetry:
            if item.type == "Pole":
                self.graph_pole(win, item.position, color_change)
                self.graph_pole(win, item.position_sym, color_change)
            if item.type == "Cero":
                self.graph_cero(win, item.position, color_change)
                self.graph_cero(win, item.position_sym, color_change)
        
        else:
            if item.type == "Pole":
                self.graph_pole(win, item.position, color_change)
            if item.type == "Cero":
                self.graph_cero(win, item.position, color_change)

    def click_objects(self, win):
        pos = pygame.mouse.get_pos()
        moving = False
        color_change = (180, 17, 17)

        #Iterates over all objetcs created and looks for collitions
        for i, item in enumerate(self.items):
            if self.detect_collition(item, pos):
                #Change color when the mouse is over item
                self.change_color_when_over(win, item, color_change)
                
                #Remove pole with left click and leaves
                if pygame.mouse.get_pressed()[2] == 1:
                    self.items.remove(item)
                    break
                    
                #If the user rigth clicks on item the moving state (global) change to true
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.items[i].moved= True  #Change the state of clicked item to moving
                    moving = True
                    self.clicked = True
                    #When a pole is clicked there is no need to check for other collision
                    break

                #Assures to check the condition only on the first press mouse event 
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False

        return moving

    def move_item(self, win):
        keep_moving = False  #Global variable that controls moving in main while
        pos = pygame.mouse.get_pos()
        value_pos = self.z_plane_position(pos)
        self.display_value_on_screen(win, value_pos)

        #Iterate to find the moving objetc
        for i in range(len(self.items)):
            if self.items[i].moved:
                idx_moving = i

        #While pressing right click the user can move an item
        if pygame.mouse.get_pressed()[0] and self.pos_in_plane(pos):
            self.change_color_when_over(win, self.items[idx_moving], (0,255,0))
            keep_moving = True
            value_sym = self.z_plane_position(self.items[idx_moving].position_sym)
            self.items[idx_moving].update_values(pos, value_pos, value_sym)  #Adjust all the values of the moving item
        else:
            keep_moving = False
            self.items[idx_moving].moved = False
        
        return keep_moving

    def z_plane_position(self, pos):
        #Math to map between pixels and zplane values

        x = None
        w_min = self.x_start
        w_max = self.x_start + self.plane_size
        w1 = self.x_start + self.margin  #Point where unit circle = -1
        w2 = self.x_start + self.plane_size - self.margin  #Point where unit circle = 1
        a1 = 2/(w2-w1)
        b1 = 1 - a1*w2
        if pos[0] > w_min and pos[0] < w_max:
            x = a1 * pos[0] + b1
        
        y = None
        h_min = self.y_start
        h_max = self.y_start + self.plane_size
        h1 = self.y_start + self.margin
        h2 = self.y_start + self.plane_size - self.margin
        a2 = 2/(h1 - h2)
        b2 = 1 - a2 * h1
        if pos[1] > h_min and pos[1] < h_max:
            y = a2 * pos[1] + b2

        return (x, y)
    
    def display_value_on_screen(self, win, value_pos):
        if (value_pos[0] != None) and (value_pos[1] != None):
            x_vals = np.round(value_pos[0], 2)
            y_vals = np.round(value_pos[1], 2)
            values_text = self.font.render(f"{x_vals} ; {y_vals}i", True, (255, 255, 255))
            # Display the values of the pole on the screen
            win.blit(values_text, (110, 525))
    
    def display_item_unassigned(self, win, pos, type, color):
        if self.symmetry:
            if type == "Pole":
                pos_sym = self.emptyPole.pos_symmetry(pos)
                self.emptyPole.draw_unassigned(win, pos, color)
                self.emptyPole.draw_unassigned(win, pos_sym, color)
            if type == "Cero":
                pos_sym = self.emptyPole.pos_symmetry(pos)
                self.emptyCero.draw_unassigned(win, pos, color)
                self.emptyCero.draw_unassigned(win, pos_sym, color)
        else:
            if type == "Pole":
                self.emptyPole.draw_unassigned(win, pos, color)
            if type == "Cero":
                self.emptyCero.draw_unassigned(win, pos, color)

    
    def select_pole_or_cero(self, win, type):
        #In the selection process the transfer function is not updated

        action = False  #Click control on global scope (main while)
        pos = pygame.mouse.get_pos()
        value_pos = self.z_plane_position(pos)

        #Display pole or cero unassigned
        self.display_item_unassigned(win, pos, type, self.withe)
        #Display pole or cero position on screen
        self.display_value_on_screen(win, value_pos)

        #With right click leaves the poles selection menu
        if pygame.mouse.get_pressed()[2] == 1 and self.clicked == False:
            action = True

        #With left click chooses the spot for the pole
        if pygame.mouse.get_pressed()[0] == 1 and self.pos_in_plane(pos) and self.clicked == False:
            if type == "Pole":
                value_pos_sym = self.z_plane_position(self.emptyPole.pos_symmetry(pos))
                self.items.append(Pole(self.poles_size, pos, value_pos, value_pos_sym, self.symmetry, self.y_start, self.plane_size))

            if type == "Cero":
                value_pos_sym = self.z_plane_position(self.emptyPole.pos_symmetry(pos))
                self.items.append(Cero(self.poles_size, pos, value_pos, value_pos_sym, self.symmetry, self.y_start, self.plane_size))
                
            action = True
            self.clicked = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        return not action
    