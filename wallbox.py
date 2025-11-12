from collider import Collider
import pygame
import math

class WallBox(Collider):
    def __init__(self, x, y, width, height, color=(200, 100, 100), health=10, outline_thickness=3, outline_color=(0,0,0)):
        super().__init__(x, y, width, height, color, outline_thickness, outline_color)
        self.health = health
        self.max_health = health
        self.original_color = color
        self.ball_color = None
        self.hit_count = 0

    def apply_ball_tint(self, ball_color):
        if self.ball_color is None:
            self.ball_color = ball_color
        
        damage_ratio = 1 - (self.health / self.max_health)
        
        self.color = tuple(
            int(self.original_color[i] * (1 - damage_ratio) + ball_color[i] * damage_ratio)
            for i in range(3)
        )

    def resolve_collision(self, ball):
        bx, by = ball.position[0], ball.position[1]
        r = ball.radius
        
        closest_x = max(self.x, min(bx, self.x + self.width))
        closest_y = max(self.y, min(by, self.y + self.height))
        
        dx = bx - closest_x
        dy = by - closest_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance < r:
            if distance > 0.01:
                nx = dx / distance
                ny = dy / distance
            else:
                if abs(ball.velocity[0]) > abs(ball.velocity[1]):
                    nx = 1 if ball.velocity[0] > 0 else -1
                    ny = 0
                else:
                    nx = 0
                    ny = 1 if ball.velocity[1] > 0 else -1
            
            penetration = r - distance
            
            buffer = 0.5
            ball.position[0] += nx * (penetration + buffer)
            ball.position[1] += ny * (penetration + buffer)
            
            dot_product = ball.velocity[0] * nx + ball.velocity[1] * ny
            
            if dot_product < 0:
                ball.velocity[0] = (ball.velocity[0] - 2 * dot_product * nx)
                ball.velocity[1] = (ball.velocity[1] - 2 * dot_product * ny)
            
            if self.on_collision:
                self.on_collision(self, ball, [closest_x, closest_y])
            
            return True
            
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.outline_color, (self.x, self.y, self.width, self.height), self.outline_thickness)
        
        font = pygame.font.Font(None, 48)
        text = font.render(str(max(0, int(self.health))), True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x + self.width/2, self.y + self.height/2))
        screen.blit(text, text_rect)