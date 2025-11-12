import math
import pygame

class Collider:
    def __init__(self, x, y, width, height, color=(150, 150, 150), outline_thickness=2, outline_color=(0,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.outline_thickness = outline_thickness
        self.outline_color = outline_color
        self.on_collision = None
        
    def set_collision_handler(self, callback):
        self.on_collision = callback
    
    def get_bounds(self):
        return {
            'left': self.x,
            'right': self.x + self.width,
            'top': self.y,
            'bottom': self.y + self.height
        }
    
    def point_to_rect_collision(self, px, py, radius):
        bounds = self.get_bounds()
        
        closest_x = max(bounds['left'], min(px, bounds['right']))
        closest_y = max(bounds['top'], min(py, bounds['right']))
        
        dx = px - closest_x
        dy = py - closest_y
        distance_sq = dx * dx + dy * dy
        
        return distance_sq < (radius * radius), closest_x, closest_y, dx, dy
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), self.outline_thickness)