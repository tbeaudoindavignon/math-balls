import pygame
import pygame.gfxdraw
from container import Container

class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.colliders = []
        self.width = screen.get_width()
        self.height = screen.get_height()

    def add_object(self, obj):
        self.objects.append(obj)

    def add_collider(self, collider):
        self.colliders.append(collider)

    def add_container(self, container):
        self.add_collider(container)

    def remove_object(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    def remove_collider(self, collider):
        if collider in self.colliders:
            self.colliders.remove(collider)

    def get_objects(self):
        return self.objects
    
    def update(self):
        for collider in self.colliders:
            collider.draw(self.screen)

        for ball in self.objects:
            ball.velocity[1] += ball.gravity
            
            ball.position[0] += ball.velocity[0]
            ball.position[1] += ball.velocity[1]
            
            ball.container = None
            for collider in self.colliders:
                if isinstance(collider, Container) and collider.contains_ball(ball):
                    ball.container = collider
                    break
            
            collision_count = 0
            for collider in self.colliders:
                if hasattr(collider, 'resolve_collision'):
                    if collider.resolve_collision(ball):
                        collision_count += 1
            
            if ball.container is None:
                if ball.position[0] - ball.radius <= 0:
                    ball.position[0] = ball.radius
                    ball.velocity[0] = abs(ball.velocity[0])
                    
                elif ball.position[0] + ball.radius >= self.width:
                    ball.position[0] = self.width - ball.radius
                    ball.velocity[0] = -abs(ball.velocity[0])
                
                if ball.position[1] - ball.radius <= 0:
                    ball.position[1] = ball.radius
                    ball.velocity[1] = abs(ball.velocity[1])
                    
                elif ball.position[1] + ball.radius >= self.height:
                    ball.position[1] = self.height - ball.radius
                    ball.velocity[1] = -abs(ball.velocity[1])

            pygame.gfxdraw.filled_circle(
                self.screen,
                int(ball.position[0]),
                int(ball.position[1]),
                ball.radius,
                ball.color
            )
            pygame.gfxdraw.aacircle(
                self.screen,
                int(ball.position[0]),
                int(ball.position[1]),
                ball.radius,
                ball.color
            )

            for i in range(4):
                pygame.gfxdraw.aacircle(
                    self.screen,
                    int(ball.position[0]),
                    int(ball.position[1]),
                    ball.radius + i,
                    (0, 0, 0)
                )

            if hasattr(ball, 'draw_icon'):
                ball.draw_icon(self.screen)