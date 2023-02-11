############ Imports ############

import pygame

######## Base Dot Class ##########

class Ball:
    def __init__(self, x : int, y : int, color : tuple = pygame.Color("black")) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.color_border = pygame.Color("black")
        self.radius = 10
        self.border_width= 2
    
    def coords(self):
        return (self.x, self.y)
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(win, self.color_border, (self.x, self.y), self.radius, width=self.border_width)
