class Ball:
    def __init__(self, radius, color, icon, starting_position, starting_velocity, gravity=0.2):
        self.radius = radius
        self.color = color
        self.icon = icon
        self.position = starting_position
        self.velocity = starting_velocity
        self.gravity = gravity
        self.hitcount = 0
        self.container = None
