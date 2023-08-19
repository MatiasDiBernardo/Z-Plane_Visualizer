import pygame
import interactive
from z_plane import ZPlane
from graph import GraphPlotting
pygame.font.init()

#Intial config
WIDTH = 925
HEIGTH = 550
WIN = pygame.display.set_mode((WIDTH, HEIGTH))

clock = pygame.time.Clock()
icon = pygame.image.load('images/icon.png').convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption("")

#Load assets
pole_image = pygame.image.load('images/pole.png').convert_alpha()
pole_image_press = pygame.image.load('images/pole_press.png').convert_alpha()
cero_image = pygame.image.load('images/cero.png').convert_alpha()
cero_image_press = pygame.image.load('images/cero_press.png').convert_alpha()
plus = pygame.image.load('images/plus.png').convert_alpha()
plus_press = pygame.image.load('images/plus_press.png').convert_alpha()
minus = pygame.image.load('images/minus.png').convert_alpha()
minus_press = pygame.image.load('images/minus_press.png').convert_alpha()
clear = pygame.image.load('images/trash_bin.png').convert_alpha()
clear_press = pygame.image.load('images/trash_bin_press.png').convert_alpha()
cb_tick = pygame.image.load('images/checkbox_ticked.png').convert_alpha()
cb_tick_press = pygame.image.load('images/checkbox_ticked_press.png').convert_alpha()
cb_untick = pygame.image.load('images/checkbox_untick.png').convert_alpha()
cb_untick_press = pygame.image.load('images/checkbox_untick_press.png').convert_alpha()

#Objects init
font = pygame.font.Font('images/AldotheApache.ttf', 20)
font2 = pygame.font.Font('images/AldotheApache.ttf', 30)
font3 = pygame.font.Font('images/Arial Unicode MS Font.ttf', 15)
zplane = ZPlane(25, 95, font) 
mag_grap = GraphPlotting(500, 90, 400, 180, font3)
phase_grap = GraphPlotting(500, 335, 400, 180, font3)
POLE_BUTTON = interactive.Button(83, 47, pole_image, pole_image_press, 1, 0)
CERO_BUTTON = interactive.Button(237, 44, cero_image, cero_image_press, 1, 0)
ZOOM_PLUS_BUTTON = interactive.Button(333, 501, plus, plus_press, 1, 0)
ZOOM_MINUS_BUTTON = interactive.Button(288, 500, minus, minus_press, 1, 0)
CLEAR_BUTTON = interactive.Button(378, 497, clear, clear_press, 1, 0)
SYM_CHECKBOX = interactive.CheckBox(396, 48, cb_untick, cb_untick_press, cb_tick, cb_tick_press, 0.9)

# Main game loop
def main():

    #Scope variables
    run = True
    font_color = (255, 255, 255)
    pole_selection = False
    cero_selection = False
    item_moving = False

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        #Static background
        WIN.fill((0,0,0))
        title = font2.render("Z-Plane Visualizer", True, font_color)
        WIN.blit(title, (10,10))
        pole_text = font.render("Add Pole", True, font_color)
        WIN.blit(pole_text, (10,60))
        cero_text = font.render("Add cero", True, font_color)
        WIN.blit(cero_text, (160,60))
        symmetry_text = font.render("Symmetry", True, font_color)
        WIN.blit(symmetry_text, (310, 60))
        transfer_text = font2.render("Transfer Function", True, font_color)
        WIN.blit(transfer_text, (500,10))
        mag_text = font.render("Magnitude", True, font_color)
        WIN.blit(mag_text, (500,60))
        phase_text = font.render("Phase", True, font_color)
        WIN.blit(phase_text, (500, 306))
        position_text = font.render("Position: ", True, font_color)
        WIN.blit(position_text, (25, 515))

        #Display z plane
        zplane.default_background(WIN)
        zplane.poles_and_ceros_display(WIN)
        mag_grap.plot_background(WIN, "Mag")
        phase_grap.plot_background(WIN, "Phase")

        #Display Pole
        if POLE_BUTTON.draw(WIN):
            pole_selection = True
        
        if pole_selection:
            pole_selection = zplane.select_pole_or_cero(WIN, "Pole")

        #Display Cero
        if CERO_BUTTON.draw(WIN):
            cero_selection = True
        
        if cero_selection:
            cero_selection = zplane.select_pole_or_cero(WIN, "Cero")
        
        #Allows to move poles and ceros
        if not pole_selection and not cero_selection:
            if zplane.click_objects(WIN) and item_moving == False:          
                item_moving = True

        if item_moving:
            item_moving = zplane.move_item(WIN)
        
        #Zoom buttons
        if ZOOM_PLUS_BUTTON.draw(WIN):
            zplane.zoom_plane_in()
        
        if ZOOM_MINUS_BUTTON.draw(WIN):
            zplane.zoom_plane_out()
        
        #Clear the plane
        if CLEAR_BUTTON.draw(WIN):
            zplane.clear_zplane()
        
        #Symmetry
        if SYM_CHECKBOX.draw(WIN):
            zplane.symmetry = True
        else:
            zplane.symmetry = False

        #Show magnitude spectrum
        mag_grap.plot_magnitude(WIN, zplane)
        phase_grap.plot_phase(WIN, zplane)

        #Debug
        items = zplane.items
        if len(items) != 0:
            ver = items[0].values()
            print(ver)

        pygame.display.update()

    pygame.quit()

main()
