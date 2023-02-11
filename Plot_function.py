########## Imports ###########
import pygame


########### Main functionality ##############


class Plot_function:
    def __init__(self, func, x_range, y_range, window_dim, top_left_corner = (0, 0)) -> None:
        # Function to plot
        self.func = func

        # Axis parameters
        self.x_range = x_range
        self.y_range = y_range
        self.number_of_points = 100

        # Plot color
        self.color = pygame.Color("red")

        # Window information
        self.width = window_dim[0]
        self.height = window_dim[1]
        self.top_left_corner = top_left_corner


    def create_points(self) -> list:
        point_list = []
        x_list = [x * ((self.x_range[1] - self.x_range[0]) / self.number_of_points) + self.x_range[0] for x in range(self.number_of_points) ]
        for x in x_list:
            point = (x, self.func(x))
            point_list.append(point)
        return point_list
    
    def translate_points_to_pixels(self, point_list):
        translated_points = []

        # X axis transformation parameters
        x_scale = self.width / (self.x_range[1] - self.x_range[0])
        
        # Y axis transformation parameters
        y_scale = self.height / (self.y_range[1] - self.y_range[0])

        for point in point_list:

            translated_point = ((point[0] - self.x_range[0]) * x_scale + self.top_left_corner[0], (point[1] - self.y_range[0]) * y_scale + self.top_left_corner[1])

            translated_points.append(translated_point)

        return translated_points

    def scale_to_screen(self):
        pass

    def draw(self, win):
        points_list = self.translate_points_to_pixels(self.create_points())
        pygame.draw.aalines(win, self.color, points = points_list, closed= False)

        origin = [(0,0)]
        pygame.draw.circle(win, pygame.Color("black"), self.translate_points_to_pixels(origin)[0], 4)
