############### Imports ################

import pygame
from Buttons import *
from Ball import *
from pygame.event import Event
from Plot_function import *
import math

############### Variable Declaration ###########

# --------------- Constants -----------------

# Window Size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450
DISPLAY_DIM = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Creating Window
WIN = pygame.display.set_mode(DISPLAY_DIM)
pygame.display.set_caption('Algorithm Demo')

# Frames per second
FPS = 60
CLOCK = pygame.time.Clock()


# --------------- Global Variables ------------

# Initialize global project variables
pygame.init()

# Program Context
ProgramContext = {"Mode_dot_create":True,
                  "Mode_dot_remove": False}

# Object list
dot_list = []

########## Auxiliary functions ##########

# Adds dot
def add_dot(coordinates: tuple, color: "string" ) -> None:
    dot = Ball(coordinates[0], coordinates[1], color)
    dot_list.append(dot)

# Removes dot
def rm_dot(dot: Ball):
    dot_list.remove(dot)

# Removes last dot
def rm_dot_last():
    if dot_list != []:
        del dot_list[-1]

# Handles mouse clicks (Adding and removing dots)
def click_handling(event: Event, mouse_pos : tuple, ProgramContext : ProgramContext) -> None:
    if event.button == 1 and ProgramContext["Mode_dot_create"]:
        add_dot(mouse_pos, "red")

    if event.button == 1 and ProgramContext["Mode_dot_remove"]:
        rm_dot_last()

    if event.button == 3 and ProgramContext["Mode_dot_create"]:
        add_dot(mouse_pos, "blue")

# Handles key presses (Mode changes)
def key_handling(event: Event, ProgramContext: ProgramContext) -> None:
    
    # Set dot add mode
    if event.key == pygame.K_a:
        ProgramContext["Mode_dot_create"] = True
        ProgramContext["Mode_dot_remove"] = False

    # Set dot remove mode
    if event.key == pygame.K_d:
        ProgramContext["Mode_dot_create"] = False
        ProgramContext["Mode_dot_remove"] = True

# Displays FPS
def display_fps():
    "Data that will be rendered and blitted in _display"
    def render(fnt, what, color, where):
        "Renders the fonts as passed from display_fps"
        text_to_show = fnt.render(what, 1, pygame.Color(color))
        WIN.blit(text_to_show, where)

    # Renders the FPS count at the corner of the screen
    render(
        pygame.font.SysFont("Arial", 20),
        what  = str(int(CLOCK.get_fps())),
        color = "green",
        where = (WINDOW_WIDTH - 50, 0))

# Function plot object

a = 0
def test_function(x):
    return math.sin(x + a)

plot = Plot_function(test_function, [-10, 10], [-10, 10], DISPLAY_DIM)
plot.number_of_points = 1000


########## Main ##########
def main():
    global a

    # Setting FPS
    CLOCK.tick(FPS)

    # Getting Mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Handling events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_handling(event, mouse_pos, ProgramContext)

        if event.type == pygame.KEYDOWN:
            key_handling(event, ProgramContext)

    if pygame.key.get_pressed()[pygame.K_m]:
        a += 0.1
    if pygame.key.get_pressed()[pygame.K_n]:
        a -= 0.1

    ######### Rendering ###########
    WIN.fill(pygame.Color("white"))

    # Rendering dots
    for dot in dot_list:
        dot.draw(WIN)

    # Plotting Function
    plot.draw(WIN)


    def dyn_function(x):
        
        return math.sin(x * 12 + a) * math.sin(x + a / 3)*4
    plot.func = dyn_function

    # Display FPS
    display_fps()

    # Update display
    pygame.display.update()




if __name__ == "__main__":
    while True:
        status = main()

        # Handling app status
        if status == "quit":
            break

    pygame.quit()