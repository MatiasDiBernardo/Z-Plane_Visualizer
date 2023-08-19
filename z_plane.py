import pygame
import numpy as np

class ZPlane():
    def __init__(self, x_start, y_start, font):
        self.x_start = x_start  #Starting position (upper left)
        self.y_start = y_start
        self.font = font
        self.plane_size = 400  #Size of the Z Plane
        self.background_color = (15, 15, 15)  #For the Z plane
        self.withe = (255, 255, 255)
        self.poles_size = 10  #Dimension of poles in pixels (same for ceros)
        self.position_poles = []  #Positions of poles in pixels
        self.position_ceros = []
        self.rect_poles = []  #Entities used for collition detection
        self.rect_ceros = []
        self.val_poles = []  #Real values of poles
        self.val_ceros = []
        self.moving_element = None  #Keeps track of moving poles or ceros
        self.zoom = 4  #Starting zoom index value
        self.symmetry = False
        self.center_plane = (x_start + self.plane_size // 2, y_start + self.plane_size // 2) 

    def default_background(self, win):
        #Background
        pygame.draw.rect(win, self.background_color, (
            self.x_start, self.y_start, self.plane_size,self.plane_size,
        ))

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
        self.position_poles = []  
        self.position_ceros = []
        self.rect_poles = []  
        self.rect_ceros = []
        self.val_poles = []  
        self.val_ceros = []
    
    def graph_cero(self, win, pos, color):
        pygame.draw.circle(win, color, pos, self.poles_size - 1, width=1)
    
    def graph_pole(self, win, pos, color):
        delta = self.poles_size // 2
        l1 = (pos[0] - delta, pos[1] - delta)
        l2 = (pos[0] + delta, pos[1] + delta)
        pygame.draw.line(win, color, l1, l2, width=1)
        
        l3 = (pos[0] - delta, pos[1] + delta)
        l4 = (pos[0] + delta, pos[1] - delta)
        pygame.draw.line(win, color, l3, l4, width=1)
    
    def create_rect(self, pos):
        delta = self.poles_size // 2
        x1 = pos[0] - delta
        y1 = pos[1] - delta
        return pygame.Rect(x1, y1, self.poles_size, self.poles_size)

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
        for p in self.position_poles:
            self.graph_pole(win, p, self.withe)
        
        for c in self.position_ceros:
            self.graph_cero(win, c, self.withe)
    
    def click_poles(self, win, frame_delay):
        pos = pygame.mouse.get_pos()
        moving = False
        color_change = (140, 17, 17)
        assert len(self.position_poles) == len(self.rect_poles)

        #Loops for colision in all poles
        for i in range(len(self.rect_poles)):
            if self.rect_poles[i].collidepoint(pos):
                #Change color when the mouse is over pole
                self.graph_pole(win, self.position_poles[i], color_change)

                #Remove pole with left click
                if pygame.mouse.get_pressed()[2] == 1 and not self.symmetry:
                    self.position_poles.pop(i)
                    self.rect_poles.pop(i)
                    self.val_poles.pop(i)
                    break
                    
                #If the user clicks on pole change the state (moving) to true and deletes the static pole
                if frame_delay > 8:
                    if pygame.mouse.get_pressed()[0] == 1 and moving == False:
                        self.position_poles.pop(i)
                        self.rect_poles.pop(i)
                        self.val_poles.pop(i)

                        #Removes symmetry
                        if self.symmetry and len(self.position_poles) != 0:
                            self.position_poles.pop(i)
                            self.rect_poles.pop(i)
                            self.val_poles.pop(i)

                        moving = True
                        #When a pole is clicked there is no need to check for other collision
                        break
        return moving

    def click_ceros(self, win, frame_delay):
        pos = pygame.mouse.get_pos()
        moving = False
        color_change = (140, 17, 17)
        assert len(self.position_ceros) == len(self.rect_ceros)

        #Loops for colision in all ceros
        for i in range(len(self.rect_ceros)):
            if self.rect_ceros[i].collidepoint(pos):
                #Change color when the mouse is over pole
                self.graph_cero(win, self.position_ceros[i], color_change)

                #Remove cero with left click
                if pygame.mouse.get_pressed()[2] == 1 and not self.symmetry:
                    self.position_ceros.pop(i)
                    self.rect_ceros.pop(i)
                    self.val_ceros.pop(i)
                    break
                    
                #If the user clicks on cero change the state (moving) to true
                if frame_delay > 8:
                    if pygame.mouse.get_pressed()[0] == 1 and moving == False:
                        self.position_ceros.pop(i)
                        self.rect_ceros.pop(i)
                        self.val_ceros.pop(i)

                        #Removes cero symmetry (assumes picks the first selected cero)
                        if self.symmetry and len(self.position_ceros) != 0:
                            self.position_ceros.pop(i)
                            self.rect_ceros.pop(i)
                            self.val_ceros.pop(i)

                        moving = True
                        #When a pole is clicked  there is no need to check for other collisions
                        break
        return moving

    def move_pole(self, win):
        keep_moving = False
        pos = pygame.mouse.get_pos()

        #Display the real value of moving pole on screen
        real_values = self.z_plane_position(pos)
        if (real_values[0] != None) and (real_values[1] != None):
            x_vals = np.round(real_values[0], 2)
            y_vals = np.round(real_values[1], 2)
            values_text = self.font.render(f"{x_vals} ; {y_vals}i", True, (255, 255, 255))
            win.blit(values_text, (100, 515))

        #While pressing right click the user can move a pole
        if pygame.mouse.get_pressed()[0] and self.pos_in_plane(pos):
            keep_moving = True
            self.graph_pole(win, pos, self.withe)
            #if self.pos_in_plane(pos):
            self.moving_element = [self.pix2val(pos), "Pole"]

        #When the user stop pressing this poles is saved
        else:
            keep_moving = False
            self.moving_element = None
            if self.pos_in_plane(pos):
                self.position_poles.append(pos)
                entity = self.create_rect(pos)
                self.rect_poles.append(entity)
                self.val_poles.append(self.pix2val(pos))
     
        #Moving Pole for Symmetry 
        y_mid = self.y_start + self.plane_size//2  #Origin in Y coordinate
        delta_y = y_mid - pos[1]
        if self.symmetry and delta_y != 0:
            pos_sym = (pos[0], pos[1] + 2 * delta_y)
            #While pressing right click the user can move a pole
            if pygame.mouse.get_pressed()[0]:
                self.graph_pole(win, pos_sym, self.withe)
                if self.pos_in_plane(pos_sym):
                    self.moving_element = [self.pix2val(pos), "Pole Symmetric", self.pix2val(pos_sym)]

            #When the user stop pressing this poles is saved
            else:
                self.moving_element = None
                self.position_poles.append(pos_sym)
                entity = self.create_rect(pos_sym)
                self.rect_poles.append(entity)
                if self.pos_in_plane(pos_sym):
                    self.val_poles.append(self.pix2val(pos_sym))

        return keep_moving

    def move_cero(self, win):
        keep_moving = False
        pos = pygame.mouse.get_pos()

        #Display the real value of the moving cero on screen
        real_values = self.z_plane_position(pos)
        if (real_values[0] != None) and (real_values[1] != None):
            x_vals = np.round(real_values[0], 2)
            y_vals = np.round(real_values[1], 2)
            values_text = self.font.render(f"{x_vals} ; {y_vals}i", True, (255, 255, 255))
            win.blit(values_text, (100, 515))

        #While pressing right click the user can move a pole
        if pygame.mouse.get_pressed()[0]:
            keep_moving = True
            self.graph_cero(win, pos, self.withe)
            if self.pos_in_plane(pos):
                self.moving_element = [self.pix2val(pos), "Cero"]
        
        #When the user stop pressing this poles is saved
        else:
            keep_moving = False
            self.moving_element = None
            if self.pos_in_plane(pos):
                self.position_ceros.append(pos)
                entity = self.create_rect(pos)
                self.rect_ceros.append(entity)
                self.val_ceros.append(self.pix2val(pos))
        
        #Moving cero for symmetry
        y_mid = self.y_start + self.plane_size//2  #Origin in Y coordinate
        delta_y = y_mid - pos[1]
        if self.symmetry and delta_y != 0:
            pos_sym = (pos[0], pos[1] + 2 * delta_y)
            #While pressing right click the user can move a pole
            if pygame.mouse.get_pressed()[0]:
                self.graph_cero(win, pos_sym, self.withe)
                if self.pos_in_plane(pos_sym):
                    self.moving_element = [self.pix2val(pos), "Cero Symmetric", self.pix2val(pos_sym)]

            #When the user stop pressing this poles is saved
            else:
                self.moving_element = None
                self.position_ceros.append(pos_sym)
                entity = self.create_rect(pos_sym)
                self.rect_ceros.append(entity)
                if self.pos_in_plane(pos_sym):
                    self.val_ceros.append(self.pix2val(pos_sym))

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
    
    def pix2val(self, pos):
        x, y = self.z_plane_position(pos)
        val = x + 1j*y
        return val
    
    def select_pole_or_cero(self, win, frame_delay, type):
        #In the selection process the transfer function is not updated
        clicked = False
        pos = pygame.mouse.get_pos()

        if type == "Pole":
            self.graph_pole(win, pos, self.withe)
        if type == "Cero":
            self.graph_cero(win, pos, self.withe)

        #Display pole or cero position on screen
        real_values = self.z_plane_position(pos)
        if (real_values[0] != None) and (real_values[1] != None):
            x_vals = np.round(real_values[0], 2)
            y_vals = np.round(real_values[1], 2)
            values_text = self.font.render(f"{x_vals} ; {y_vals}i", True, (255, 255, 255))
            win.blit(values_text, (100, 510))

        #Frames delay to avoid collitions in input response
        if frame_delay > 8:
            #With right click leaves the poles selection menu
            if pygame.mouse.get_pressed()[2] == 1 and clicked == False:
                clicked = True

            #With left click chooses the spot for the pole
            if pygame.mouse.get_pressed()[0] == 1 and self.pos_in_plane(pos):
                if type == "Pole":
                    self.position_poles.append(pos)
                    entity = self.create_rect(pos)
                    self.rect_poles.append(entity)
                    if self.pos_in_plane(pos):
                        self.val_poles.append(self.pix2val(pos))
                if type == "Cero":
                    self.position_ceros.append(pos)
                    entity = self.create_rect(pos)
                    self.rect_ceros.append(entity)
                    if self.pos_in_plane(pos):
                        self.val_ceros.append(self.pix2val(pos))
                clicked = True
        
        #Lazy impplementation, activate symmetry in selection, new imp with classes to check sym
        y_mid = self.y_start + self.plane_size//2  #Origin in Y coordinate
        delta_y = y_mid - pos[1]
        if self.symmetry and delta_y != 0:
            pos_sym = (pos[0], pos[1] + 2 * delta_y)
            
            if type == "Pole":
                self.graph_pole(win, pos_sym, self.withe)
            if type == "Cero":
                self.graph_cero(win, pos_sym, self.withe)


            #Frames margin to avoid delay in input response
            if frame_delay > 8:
                #With left click chooses the spot for the pole
                if pygame.mouse.get_pressed()[0] == 1 and self.pos_in_plane(pos_sym):
                    if type == "Pole":
                        self.position_poles.append(pos_sym)
                        entity = self.create_rect(pos_sym)
                        self.rect_poles.append(entity)
                        if self.pos_in_plane(pos_sym):
                            self.val_poles.append(self.pix2val(pos_sym))
                    if type == "Cero":
                        self.position_ceros.append(pos_sym)
                        entity = self.create_rect(pos_sym)
                        self.rect_ceros.append(entity)
                        if self.pos_in_plane(pos_sym):
                            self.val_ceros.append(self.pix2val(pos_sym))
        
        return not clicked
    