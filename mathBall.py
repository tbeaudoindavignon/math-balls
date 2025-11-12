import ball
import math
import pygame

class MathBall(ball.Ball):
    def __init__(self, radius, color, icon, starting_position, starting_velocity, math_type="linear", sound_frequency=440, gravity=0.2):
        super().__init__(radius, color, icon, starting_position, starting_velocity, gravity)
        self.math_type = math_type
        self.total_damage = 0
        self.sound_frequency = sound_frequency
        self.sound_duration = 100
        self.sound = None
        self.sound_channel = None
        self.load_sound()
        
    def calculate_damage(self):
        return 1
    
    def on_hit(self):
        self.hitcount += 1
        damage = self.calculate_damage()
        self.total_damage += damage
        self.play_sound()
        return damage
    
    def load_sound(self):
        try:
            sound_file = f"sounds/{self.math_type}.mp3"
            self.sound = pygame.mixer.Sound(sound_file)
            self.sound.set_volume(0.3)
        except:
            sound_file = "sounds/fibonacci.mp3"
            self.sound = pygame.mixer.Sound(sound_file)
            self.sound.set_volume(0.3)
    
    def play_sound(self):
        if self.sound:
            if self.sound_channel and self.sound_channel.get_busy():
                self.sound_channel.stop()
            
            self.sound_channel = self.sound.play()

    def calculate_damage_for_hit(self, hit_number):
        temp_hitcount = self.hitcount
        self.hitcount = hit_number
        damage = self.calculate_damage()
        self.hitcount = temp_hitcount
        return damage
    
    def draw_icon(self, screen):
        if self.icon:
            font = pygame.font.Font(None, int(self.radius * 1.7))
            text = font.render(self.icon, True, (0, 0, 0))
            text_rect = text.get_rect(center=(int(self.position[0]), int(self.position[1])))
            screen.blit(text, text_rect)


class FibonacciBall(MathBall):
    def __init__(self, radius, starting_position, starting_velocity):
        super().__init__(
            radius=radius,
            color=(46, 204, 113),
            icon="φ",
            starting_position=starting_position,
            starting_velocity=starting_velocity,
            math_type="fibonacci",
            sound_frequency=523,
            gravity=0.2
        )
        self.fib_cache = {0: 0, 1: 1}
    
    def fibonacci(self, n):
        if n in self.fib_cache:
            return self.fib_cache[n]
        
        if n > 100:
            n = 100
            
        self.fib_cache[n] = self.fibonacci(n-1) + self.fibonacci(n-2)
        return self.fib_cache[n]
    
    def calculate_damage(self):
        return max(1, self.fibonacci(self.hitcount + 2))


class FactorialBall(MathBall):
    def __init__(self, radius, starting_position, starting_velocity):
        super().__init__(
            radius=radius,
            color=(231, 76, 60),
            icon="n!",
            starting_position=starting_position,
            starting_velocity=starting_velocity,
            math_type="factorial",
            sound_frequency=659,
            gravity=0.2
        )
    
    def calculate_damage(self):
        n = min(self.hitcount, 20)
        return max(1, math.factorial(n + 1))


class PowerBall(MathBall):
    def __init__(self, radius, starting_position, starting_velocity, base=2):
        super().__init__(
            radius=radius,
            color=(155, 89, 182),
            icon=f"{base}ⁿ",
            starting_position=starting_position,
            starting_velocity=starting_velocity,
            math_type="power",
            sound_frequency=784,
            gravity=0.2
        )
        self.base = base
    
    def calculate_damage(self):
        n = min(self.hitcount, 50)
        return max(1, self.base ** n)


class PrimeBall(MathBall):
    def __init__(self, radius, starting_position, starting_velocity):
        super().__init__(
            radius=radius,
            color=(241, 196, 15),
            icon="P",
            starting_position=starting_position,
            starting_velocity=starting_velocity,
            math_type="prime",
            sound_frequency=880,
            gravity=0.2
        )
        self.primes_cache = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
        self.max_prime_index = 1000
    
    def is_prime(self, n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def get_nth_prime(self, n):
        if n < len(self.primes_cache):
            return self.primes_cache[n]
        
        candidate = self.primes_cache[-1] + 2
        while len(self.primes_cache) <= n:
            if self.is_prime(candidate):
                self.primes_cache.append(candidate)
            candidate += 2
        
        return self.primes_cache[n]
    
    def calculate_damage(self):
        n = min(self.hitcount, self.max_prime_index)
        return self.get_nth_prime(n)


class SquareBall(MathBall):
    def __init__(self, radius, starting_position, starting_velocity):
        super().__init__(
            radius=radius,
            color=(52, 152, 219),
            icon="n²",
            starting_position=starting_position,
            starting_velocity=starting_velocity,
            math_type="square",
            sound_frequency=698,
            gravity=0.2
        )
    
    def calculate_damage(self):
        n = self.hitcount + 1
        return n * n


class LinearBall(MathBall):
    def __init__(self, radius, starting_position, starting_velocity, multiplier=1):
        super().__init__(
            radius=radius,
            color=(149, 165, 166),
            icon=f"{multiplier}n",
            starting_position=starting_position,
            starting_velocity=starting_velocity,
            math_type="linear",
            sound_frequency=440,
            gravity=0.2
        )
        self.multiplier = multiplier
    
    def calculate_damage(self):
        return self.multiplier * (self.hitcount + 1)


class TriangularBall(MathBall):
    def __init__(self, radius, starting_position, starting_velocity):
        super().__init__(
            radius=radius,
            color=(230, 126, 34),
            icon="Δ",
            starting_position=starting_position,
            starting_velocity=starting_velocity,
            math_type="triangular",
            sound_frequency=587,
            gravity=0
        )
    
    def calculate_damage(self):
        n = self.hitcount + 1
        return (n * (n + 1)) // 2


class ExponentialBall(MathBall):
    def __init__(self, radius, starting_position, starting_velocity):
        super().__init__(
            radius=radius,
            color=(26, 188, 156),
            icon="eⁿ",
            starting_position=starting_position,
            starting_velocity=starting_velocity,
            math_type="exponential",
            sound_frequency=935,
            gravity=0.2
        )
    
    def calculate_damage(self):
        n = min(self.hitcount, 30)
        return max(1, int(math.exp(n)))


BALL_TYPES = {
    'fibonacci': FibonacciBall,
    'factorial': FactorialBall,
    'power': PowerBall,
    'prime': PrimeBall,
    'square': SquareBall,
    'linear': LinearBall,
    'triangular': TriangularBall,
    'exponential': ExponentialBall,
}

BALL_INFO = {
    'fibonacci': {
        'name': 'Fibonacci',
        'color': (46, 204, 113),
        'icon': 'Fib',
        'description': 'Damage: 1, 2, 3, 5, 8, 13...',
        'formula': 'F(n) = F(n-1) + F(n-2)'
    },
    'factorial': {
        'name': 'Factorial',
        'color': (231, 76, 60),
        'icon': 'n!',
        'description': 'Damage: 1, 2, 6, 24, 120...',
        'formula': 'n!'
    },
    'power': {
        'name': 'Power',
        'color': (155, 89, 182),
        'icon': '2ⁿ',
        'description': 'Damage: 2, 4, 8, 16, 32...',
        'formula': '2^n'
    },
    'prime': {
        'name': 'Prime',
        'color': (241, 196, 15),
        'icon': 'P',
        'description': 'Damage: 2, 3, 5, 7, 11...',
        'formula': 'nth prime'
    },
    'square': {
        'name': 'Square',
        'color': (52, 152, 219),
        'icon': 'n²',
        'description': 'Damage: 1, 4, 9, 16, 25...',
        'formula': 'n²'
    },
    'linear': {
        'name': 'Linear',
        'color': (149, 165, 166),
        'icon': 'n',
        'description': 'Damage: 1, 2, 3, 4, 5...',
        'formula': 'n'
    },
    'triangular': {
        'name': 'Triangular',
        'color': (230, 126, 34),
        'icon': '△',
        'description': 'Damage: 1, 3, 6, 10, 15...',
        'formula': 'n(n+1)/2'
    },
    'exponential': {
        'name': 'Exponential',
        'color': (26, 188, 156),
        'icon': 'eⁿ',
        'description': 'Damage: 1, 3, 7, 20, 55...',
        'formula': 'e^n'
    }
}

def create_math_ball(ball_type, radius, position, velocity, **kwargs):
    ball_class = BALL_TYPES.get(ball_type.lower())
    if ball_class:
        return ball_class(radius, position, velocity, **kwargs)
    return LinearBall(radius, position, velocity)
