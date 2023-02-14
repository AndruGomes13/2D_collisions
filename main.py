############### Imports ################

import pygame
from Buttons import *
from Ball import *
from pygame.event import Event
from Plot_function import *
import math
import random
import numpy as np

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
FPS = 150
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
    ball.radius = 10
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

def detect_collision(ball_list):

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

def ball_collision(ball_1, ball_2):
    r1 = np.array([ball_1.x, ball_1.y])
    v1 = np.array([ball_1.v_x, ball_1.v_y])
    m1 = ball_1.mass

    r2 = np.array([ball_2.x, ball_2.y]) 
    v2 = np.array([ball_2.v_x, ball_2.v_y])
    m2 = ball_2.mass
    
    v1_f = v1 - (2*m2 / (m1 + m2)) * np.dot((v1 -v2), (r1 - r2)) / (np.linalg.norm(r1 - r2) ** 2) * (r1 - r2)
    v2_f = v2 - (2*m1 / (m1 + m2)) * np.dot((v2 -v1), (r2 - r1)) / (np.linalg.norm(r2 - r1) ** 2) * (r2 - r1)

    return v1_f.tolist(), v2_f.tolist()

def handle_collision(ball_list_original):
    # ball_list = ball_list_original.copy()
    # for ball in ball_list:
    #     ball_list.remove(ball)
    #     for ball_2 in ball_list:
    #         if ball != ball_2:
    #             if distance(ball, ball_2) <= (ball.radius + ball_2.radius):
    #                 (v1, v2) = ball_collision(ball, ball_2)
    #                 ball.v_x = v1[0]
    #                 ball.v_y = v1[1]
    #                 ball_2.v_x = v2[0]
    #                 ball_2.v_y = v2[1]
    #                 print("colide")
    #                 ball_list.remove(ball_2)

    index_table = [[i,i + j + 1] for i in range(len(ball_list)) for j in range(len(ball_list) - i - 1)]
    for i, j in index_table:
        ball = ball_list[i]
        ball_2 = ball_list[j]
        if distance(ball, ball_2) <= (ball.radius + ball_2.radius):
                (v1, v2) = ball_collision(ball, ball_2)
                ball.v_x = v1[0]
                ball.v_y = v1[1]
                ball_2.v_x = v2[0]
                ball_2.v_y = v2[1]




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
    
    for i in range(20):
        add_ball((random.random()*500 + 100, random.random()*300 + 100), "red")


    a = 0
    while running:
        
        # Setting FPS
        CLOCK.tick(FPS)

        # Getting Mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_handling(event, mouse_pos, ProgramContext)

            if event.type == pygame.KEYDOWN:
                key_handling(event, ProgramContext)

        if pygame.key.get_pressed()[pygame.K_m]:
            a += 0.1
        if pygame.key.get_pressed()[pygame.K_n]:
            a -= 0.1


        ######### Simulating and Rendering ###########
        ### Steping through object dynamics

        # Delta t
        t = pygame.time.get_ticks()
        # deltaTime in seconds.
        dt = (t - getTicksLastFrame) / 1000.0
        getTicksLastFrame = t


        # Check ground and wall collisions
        ground_collision(ball_list, dt)

        # Check ball collisions
        handle_collision(ball_list)
  
        # Applying force
        for ball in ball_list:
            force = (0, 4)
            ball.apply_force(force)


        # Steping objects
        for ball in ball_list:
            ball.step(dt)


        ### Rendering objects
        WIN.fill(pygame.Color("white"))

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