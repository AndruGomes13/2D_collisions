############ Imports ############

import pygame

######## Base Dot Class ##########

class Ball:
    def __init__(self, x : int, y : int, color : tuple = pygame.Color("black")) -> None:
        ### Physics Parameters
        # Position
        self.x = x
        self.y = y
        
        # Velocity
        self.v_x = 0
        self.v_y = 0

        # Acceleration
        self.a_x = 0
        self.a_y = 0

        # Internal Characteristics
        self.mass = 1
        self.c_elasticity = 1
        self.radius = 10

        ### Cosmetic Parameters 
        self.color = color
        self.color_border = pygame.Color("black")
        self.border_width= 2
    
    def coords(self):
        return (self.x, self.y)

    def apply_force(self, Force: tuple):
        self.a_x = Force[0] / self.mass
        self.a_y = Force[1] / self.mass

        self.v_x += Force[0] / self.mass
        self.v_y += Force[1] / self.mass

    def step(self, dt):
        
        # Position update
        self.x += self.v_x * dt + 0.5 * self.a_x * dt ** 2
        self.y += self.v_y * dt + 0.5 * self.a_y * dt ** 2

        # Velocity update
        self.v_x += self.a_x * dt
        self.v_y += self.a_y * dt
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(win, self.color_border, (self.x, self.y), self.radius, width=self.border_width)

