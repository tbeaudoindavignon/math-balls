from collider import Collider
import math

class Container(Collider):
    def __init__(self, x, y, width, height, color=(150, 150, 150), outline_thickness=2):
        super().__init__(x, y, width, height, color, outline_thickness)
        self.items = []
        
    def contains_point(self, x, y):
        return (self.x < x < self.x + self.width and
                self.y < y < self.y + self.height)
    
    def contains_ball(self, ball):
        return self.contains_point(ball.position[0], ball.position[1])

    def resolve_collision(self, ball):
        bounds = self.get_bounds()
        bx, by = ball.position[0], ball.position[1]
        r = ball.radius
        
        is_inside = self.contains_point(bx, by)
        
        if is_inside:
            return self._resolve_inner_collision(ball, bounds, bx, by, r)
        else:
            return self._resolve_outer_collision(ball, bounds, bx, by, r)
    
    def _resolve_inner_collision(self, ball, bounds, bx, by, r):
        collided = False
        
        if bx - r < bounds['left']:
            ball.position[0] = bounds['left'] + r
            ball.velocity[0] = abs(ball.velocity[0])
            collided = True
            
        elif bx + r > bounds['right']:
            ball.position[0] = bounds['right'] - r
            ball.velocity[0] = -abs(ball.velocity[0])
            collided = True
        
        if by - r < bounds['top']:
            ball.position[1] = bounds['top'] + r
            ball.velocity[1] = abs(ball.velocity[1])
            collided = True
            
        elif by + r > bounds['bottom']:
            ball.position[1] = bounds['bottom'] - r
            ball.velocity[1] = -abs(ball.velocity[1])
            collided = True
        
        if collided and self.on_collision:
            self.on_collision(self, ball, [bx, by])
            
        return collided
    
    def _resolve_outer_collision(self, ball, bounds, bx, by, r):
        closest_x = max(bounds['left'], min(bx, bounds['right']))
        closest_y = max(bounds['top'], min(by, bounds['bottom']))
        
        dx = bx - closest_x
        dy = by - closest_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance < r:
            if distance > 0:
                nx = dx / distance
                ny = dy / distance
            else:
                nx, ny = 1.0, 0.0
            
            penetration = r - distance
            ball.position[0] += nx * (penetration + 0.5)
            ball.position[1] += ny * (penetration + 0.5)
            
            dot_product = ball.velocity[0] * nx + ball.velocity[1] * ny
            if dot_product < 0:
                ball.velocity[0] -= 2 * dot_product * nx
                ball.velocity[1] -= 2 * dot_product * ny
            
            if self.on_collision:
                self.on_collision(self, ball, [closest_x, closest_y])
            
            return True
        
        return False