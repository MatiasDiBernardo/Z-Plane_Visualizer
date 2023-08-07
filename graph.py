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

    def plot_magnitude(self, win, zplane):
        ceros = zplane.val_ceros
        poles = zplane.val_poles
        mov = zplane.moving_element

        if len(ceros) != 0 or len(poles) != 0 or mov != None:
            #Draw dynamic plot
            if mov != None:
                #Adds moving pole or cero to list
                if mov[1] == "Pole":
                    poles.append(mov[0])
                if mov[1] == "Pole Symmetric":
                    poles.append(mov[0])
                    poles.append(mov[2])
                if mov[1] == "Cero":
                    ceros.append(mov[0])
                if mov[1] == "Cero Symmetric":
                    ceros.append(mov[0])
                    ceros.append(mov[2])

                pixels_mag = magnitude_values(ceros, poles, self.x_start, self.y_start, self.heigth)
                pygame.draw.lines(win, (255, 255, 255), False, pixels_mag)

                #Removes pole or creo from list
                if mov[1] == "Pole":
                    poles.pop()
                if mov[1] == "Pole Symmetric":
                    poles.pop()
                    poles.pop()
                if mov[1] == "Cero":
                    ceros.pop()
                if mov[1] == "Cero Symmetric":
                    ceros.pop()
                    ceros.pop()
            
            #Draw static plot
            else:
                pixels_mag = magnitude_values(ceros, poles, self.x_start, self.y_start, self.heigth)
                pygame.draw.lines(win, (255, 255, 255), False, pixels_mag)
        
    def plot_phase(self, win, zplane):
        ceros = zplane.val_ceros
        poles = zplane.val_poles
        mov = zplane.moving_element

        if len(ceros) != 0 or len(poles) != 0 or mov != None:
            #Draw dynamic plot
            if mov != None:
                #Adds moving pole or cero to list
                if mov[1] == "Pole":
                    poles.append(mov[0])
                if mov[1] == "Pole Symmetric":
                    poles.append(mov[0])
                    poles.append(mov[2])
                if mov[1] == "Cero":
                    ceros.append(mov[0])
                if mov[1] == "Cero Symmetric":
                    ceros.append(mov[0])
                    ceros.append(mov[2])

                pixels_phase = phase_values(ceros, poles, self.x_start, self.y_start, self.heigth)
                pygame.draw.lines(win, (255, 255, 255), False, pixels_phase)

                #Removes pole or creo from list
                if mov[1] == "Pole":
                    poles.pop()
                if mov[1] == "Pole Symmetric":
                    poles.pop()
                    poles.pop()
                if mov[1] == "Cero":
                    ceros.pop()
                if mov[1] == "Cero Symmetric":
                    ceros.pop()
                    ceros.pop()
            
            #Draw static plot
            else:
                pixels_phase = phase_values(ceros, poles, self.x_start, self.y_start, self.heigth)
                pygame.draw.lines(win, (255, 255, 255), False, pixels_phase)
                