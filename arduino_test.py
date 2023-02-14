############### Imports ################

import pygame
from Buttons import *
from Ball import *
from pygame.event import Event
from Plot_function import *
import math
import random
import serial
from Joystick import Joystick

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
FPS = 200
CLOCK = pygame.time.Clock()


# --------------- Global Variables ------------

# Initialize global project variables
pygame.init()

# Program Context
ProgramContext = {"Mode_dot_create":True,
                  "Mode_dot_remove": False}

# Object list
ball_list = []

########## Auxiliary functions ##########

# Adds dot
def add_ball(coordinates: tuple, color: "string" ) -> None:
    ball = Ball(coordinates[0], coordinates[1], color)
    ball.radius = 30
    ball.v_x = (random.random() * 2 - 1) * 100
    ball.v_y = (random.random() * 2 - 1) * 100

    ball_list.append(ball)

# Removes dot
def rm_ball(ball_list: list, Ball: Ball):
    ball_list.remove(Ball)

# Removes last dot
def rm_ball_last(ball_list: list):
    if ball_list != []:
        del ball_list[-1]

def distance(ball_1, ball_2):
    return ((ball_1.x - ball_2.x)**2 + (ball_1.y - ball_2.y)**2)**(1/2)

# Handles mouse clicks (Adding and removing dots)
def click_handling(event: Event, mouse_pos : tuple, ProgramContext : ProgramContext) -> None:
    if event.button == 1 and ProgramContext["Mode_dot_create"]:
        add_ball(mouse_pos, "red")

    if event.button == 1 and ProgramContext["Mode_dot_remove"]:
        rm_ball_last(ball_list)

    if event.button == 3 and ProgramContext["Mode_dot_create"]:
        add_ball(mouse_pos, "blue")

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

# Physics Functions
def ground_collision(ball_list, dt):
    for ball in ball_list:
        
        position_prediction = (ball.x + ball.v_x * dt + 0.5 * ball.a_x * dt ** 2, ball.y + ball.v_y * dt + 0.5 * ball.a_y * dt ** 2)
        
        # Floor
        if (position_prediction[0]) > DISPLAY_DIM[0] - 30:
            ball.v_x *= -1 
            ball.a_x = 0

        # Ceiling
        if (position_prediction[0]) < 30:
            ball.v_x *= -1
            ball.a_x = 0

        # Right Wall
        if (position_prediction[1]) > DISPLAY_DIM[1] - 30:
            ball.v_y *= -1
            ball.a_y = 0

        # Left Wall
        if (position_prediction[1]) < 30:
            ball.v_y *= -1
            ball.a_y = 0

def ball_collision(ball_list):

    for ball in ball_list:
        collision = False
        for ball_2 in ball_list:
            if ball != ball_2:
                if distance(ball, ball_2) <= (ball.radius + ball_2.radius):
                    collision = True
        
        if collision:
            ball.color = pygame.Color("Blue")
        else:
            ball.color = pygame.Color("Red")





# ser = serial.Serial('COM5', 9600, timeout=1)
def get_joystick():
    result = ser.readline()
    print(result)
    result = result[:-2]
    result = result.decode()
    out = result.split(";")
 

    if len(out) < 3:
        return [0 , 0 , 0]

    else:
        out[0] = int(out[0]) / 1024 * 2 -1
        out[1] = int(out[1]) / 1024 * 2 -1
        out[2] = int(out[2])
        out[2] ^= 1
        # print(out)
        return out
    
            




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



########## Main ##########
def main():


    # Running
    running = True

    ### Initializing aux variables
    getTicksLastFrame = pygame.time.get_ticks()
    
    
    add_ball((0,0), "red")
    joystick_clicked = False
    
    joystick = Joystick()

    while running:
        # Setting FPS
        CLOCK.tick(FPS)
            # Delta t
        t = pygame.time.get_ticks()
        # deltaTime in seconds.
        dt = (t - getTicksLastFrame) / 1000.0
        getTicksLastFrame = t

        # Getting Mouse position
        joystick_state = joystick.get_joystick()

        # Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            

        # Handling joystick event
        for ball in ball_list:
            # ball.x = (joystick_state[0] * 100 + 500)
            # ball.y = (-joystick_state[1] * 100 + 200)

            ball.v_x = (joystick_state[0] * 100)
            ball.v_y = (-joystick_state[1] * 100)

        for ball in ball_list:
            if joystick_state[2] and not joystick_clicked:
                ball.color = pygame.Color("blue")
                joystick_clicked = True
            elif not joystick_state[2] and joystick_clicked:
                joystick_clicked = False
                ball.color = pygame.Color("red")
        


        ######### Simulating and Rendering ###########
        ### Steping through object dynamics




        ### Rendering objects
        WIN.fill(pygame.Color("white"))

        # Steping balls
        for dot in ball_list:
            dot.step(dt)

        # Rendering balls
        for dot in ball_list:
            dot.draw(WIN)

        # Display FPS
        display_fps()

        # Update display
        pygame.display.update()




if __name__ == "__main__":
    main()
    pygame.quit()