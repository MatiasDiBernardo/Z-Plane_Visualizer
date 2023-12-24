import pygame
from math_calc import magnitude_values, phase_values

class GraphPlotting():
    def __init__(self, x_start, y_start, width, height, font):
        self.x_start = x_start
        self.y_start = y_start
        self.width = width
        self.heigth = height
        self.font = font
        self.background_color = (15, 15, 15)
        self.color_lines = (99, 99, 99)

    def plot_background(self, win, type_plot):
        pygame.draw.rect(win, self.background_color, (self.x_start, self.y_start, self.width, self.heigth))
        minus_pi = self.font.render("-π", True, (148, 148, 148))
        plus_pi = self.font.render("π", True, (148, 148, 148))
        win.blit(minus_pi, (self.x_start, self.y_start + self.heigth))
        win.blit(plus_pi, (self.x_start + self.width - 10, self.y_start + self.heigth))

        if type_plot == "Mag":
            pygame.draw.line(win, self.color_lines, (self.x_start + self.width//2, self.y_start), 
            (self.x_start + self.width//2, self.y_start + self.heigth))
            pygame.draw.line(win, self.color_lines, (self.x_start, self.y_start + self.heigth), 
                            (self.x_start + self.width, self.y_start + self.heigth))
            
        
        if type_plot == "Phase":
            pygame.draw.line(win, self.color_lines, (self.x_start + self.width//2, self.y_start), 
            (self.x_start + self.width//2, self.y_start + self.heigth))
            pygame.draw.line(win, self.color_lines, (self.x_start, self.y_start + self.heigth//2), 
                            (self.x_start + self.width, self.y_start + self.heigth//2))
        
    def get_poles_and_ceros(self, items):
        poles_values = []
        ceros_values = []
        
        for item in items:
            for _ in range(item.order):
                #Define if is a symmetry case or not
                if item.symmetry:
                    #Defines the type of item
                    if item.type == "Pole":
                        poles_values.append(item.value)
                        poles_values.append(item.value_sym)
                    if item.type == "Cero":
                        ceros_values.append(item.value)
                        ceros_values.append(item.value_sym)
                else:
                    if item.type == "Pole":
                        poles_values.append(item.value)
                    if item.type == "Cero":
                        ceros_values.append(item.value)

        return poles_values, ceros_values 
    
    def plot_magnitude(self, win, zplane):
        items = zplane.items  #Contains all poles and cero objects
        poles_val, ceros_val = self.get_poles_and_ceros(items)
        
        pixels_mag = magnitude_values(ceros_val, poles_val, self.x_start, self.y_start, self.heigth)
        pygame.draw.lines(win, (255, 255, 255), False, pixels_mag)
        
    def plot_phase(self, win, zplane):
        items = zplane.items  #Contains all poles and cero objects
        poles_val, ceros_val = self.get_poles_and_ceros(items)
        pixels_phase = phase_values(ceros_val, poles_val, self.x_start, self.y_start, self.heigth)
        pygame.draw.lines(win, (255, 255, 255), False, pixels_phase)
