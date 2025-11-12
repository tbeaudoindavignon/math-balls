import pygame
import sys
import scene as sc
import ball as bl
import container as cnt
import mathBall as mb
import wallbox
from ctypes import windll

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(4)

WIDTH = 1080
HEIGHT = 1920
BG_COLOR = (250, 250, 255)
FPS = 60

font_large = pygame.font.SysFont('franklin', 72, bold=True)
font_medium = pygame.font.SysFont('franklin', 48, bold=True)
font_small = pygame.font.SysFont('franklin', 32, bold=True)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Math Balls Fighter")

h = windll.user32.FindWindowA(b'Shell_TrayWnd', None)
windll.user32.ShowWindow(h, 0) # 0 for SW_HIDE

clock = pygame.time.Clock()
scene = sc.Scene(screen)

game_state = {
    'player1_blocks_destroyed': 0,
    'player2_blocks_destroyed': 0,
    'game_over': False,
    'winner': None,
    'damage_indicators': []
}

class DamageIndicator:
    def __init__(self, x, y, damage, color):
        self.x = x
        self.y = y
        self.damage = damage
        self.color = color
        self.lifetime = 60
        self.age = 0
        self.rise_speed = 2
        
    def update(self):
        self.age += 1
        self.y -= self.rise_speed
        return self.age < self.lifetime
    
    def draw(self, screen, font):
        alpha = int(255 * (1 - self.age / self.lifetime))
        
        text = font.render(f"-{self.damage}", True, self.color)
        text.set_alpha(alpha)
        text_rect = text.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(text, text_rect)

def on_wallbox_collision(collider, ball, collision_point):
    if isinstance(collider, wallbox.WallBox):
        if hasattr(ball, 'on_hit'):
            damage = ball.on_hit()
        else:
            damage = 1

        collider.apply_ball_tint(ball.color)

        indicator = DamageIndicator(
            collision_point[0],
            collision_point[1],
            damage,
            ball.color
        )
        game_state['damage_indicators'].append(indicator)
            
        collider.health -= damage
        
        if collider.health <= 0:
            scene.remove_collider(collider)
            if collider.y < HEIGHT / 2:
                game_state['player1_blocks_destroyed'] += 1
            else:
                game_state['player2_blocks_destroyed'] += 1
            
            if game_state['player1_blocks_destroyed'] >= 3:
                game_state['game_over'] = True
                game_state['winner'] = 'Player 2'
            elif game_state['player2_blocks_destroyed'] >= 3:
                game_state['game_over'] = True
                game_state['winner'] = 'Player 1'

def setup_arena():
    container_width = 600
    container_height = 600
    block_height = 132
    top_margin = 300
    
    player1_container = cnt.Container(
        WIDTH // 2 - container_width // 2,
        top_margin,
        container_width,
        container_height,
        color=(0, 0, 0),
        outline_thickness=6
    )
    scene.add_container(player1_container)
    
    player1_ball = mb.create_math_ball(
        'triangular',
        radius=25,
        position=[WIDTH // 2, top_margin + 25],
        velocity=[4, 5]
    )
    scene.add_object(player1_ball)
    
    for i in range(3):
        health = 10**((i+1)*3)
        block = wallbox.WallBox(
            WIDTH // 2 - container_width // 2,
            top_margin + container_height - ((block_height - 12) * 3) + (i * (block_height - 12)) + 10,
            container_width,
            block_height,
            color=(255, 255, 255),
            health=health,
            outline_thickness=6
        )
        block.set_collision_handler(on_wallbox_collision)
        scene.add_collider(block)
    
    player2_container = cnt.Container(
        WIDTH // 2 - container_width // 2,
        HEIGHT - top_margin - container_height,
        container_width,
        container_height,
        color=(0, 0, 0),
        outline_thickness=6
    )
    scene.add_container(player2_container)
    
    player2_ball = mb.create_math_ball(
        'prime',
        radius=25,
        position=[WIDTH // 2, HEIGHT - top_margin - container_height + 25],
        velocity=[4, 0]
    )
    scene.add_object(player2_ball)
    
    for i in range(3):
        health = 10**((i+1)*3)
        block = wallbox.WallBox(
            WIDTH // 2 - container_width // 2,
            HEIGHT - top_margin - ((block_height - 12) * 3) + (i * (block_height - 12)),
            container_width,
            block_height,
            color=(255, 255, 255),
            health=health,
            outline_thickness=6
        )
        block.set_collision_handler(on_wallbox_collision)
        scene.add_collider(block)

def reset_game():
    scene.objects.clear()
    scene.colliders.clear()
    game_state['player1_blocks_destroyed'] = 0
    game_state['player2_blocks_destroyed'] = 0
    game_state['game_over'] = False
    game_state['winner'] = None
    game_state['damage_indicators'].clear()
    setup_arena()

setup_arena()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                reset_game()
            elif event.key == pygame.K_SPACE and game_state['game_over']:
                reset_game()

    screen.fill(BG_COLOR)

    damage_font = pygame.font.Font(None, 48)
    game_state['damage_indicators'] = [
        indicator for indicator in game_state['damage_indicators']
        if indicator.update()
    ]

    for indicator in game_state['damage_indicators']:
        indicator.draw(screen, damage_font)

    scene.update()
    
    title_text = font_large.render("MATH BALLS", True, (255, 255, 255))
    title_rect = title_text.get_rect(centerx=WIDTH//2, top=20)
    screen.blit(title_text, title_rect)

    player1_ball = None
    player2_ball = None

    for ball in scene.objects:
        if hasattr(ball, 'math_type'):
            if ball.position[1] < HEIGHT / 2:
                player1_ball = ball
            else:
                player2_ball = ball

    if player1_ball:
        damage_text = font_medium.render(
            f"DAMAGE: {player1_ball.calculate_damage_for_hit(player1_ball.hitcount + 1)}",
            True,
            player1_ball.color
        )
        screen.blit(damage_text, (260, 320))

    if player2_ball:
        damage_text = font_medium.render(
            f"DAMAGE: {player2_ball.calculate_damage_for_hit(player2_ball.hitcount + 1)}",
            True,
            player2_ball.color
        )
    screen.blit(damage_text, (260, 1040))
    
    fps_text = font_small.render(f"FPS: {int(clock.get_fps())}", True, (200, 200, 200))
    screen.blit(fps_text, (WIDTH - 150, 20))
    
    if game_state['game_over']:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        winner_text = font_large.render(f"{game_state['winner']} WINS!", True, (255, 255, 100))
        winner_rect = winner_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(winner_text, winner_rect)
        
        restart_text = font_medium.render("Press SPACE to restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        screen.blit(restart_text, restart_rect)
    
    pygame.display.flip()
    clock.tick(FPS)

windll.user32.ShowWindow(h, 9)
pygame.quit()
sys.exit()