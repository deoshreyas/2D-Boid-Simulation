import pygame
import random
from pygame.locals import *

pygame.init()

# WINDOW
WIDTH, HEIGHT = 600, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boid Simulation")

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# BOID CLASS
boids = []
class Boid:
    def __init__(self, x, y, vel, max_vel, acc, separation_distance=20):
        self.x = x 
        self.y = y 
        self.points = [(self.x, self.y), (self.x - 10, self.y + 10), (self.x + 10, self.y + 10)]
        self.vel = pygame.Vector2(vel)
        self.max_vel = max_vel
        self.acc = pygame.Vector2(acc)
        self.separation_distance = separation_distance
        boids.append(self)
    
    def draw(self):
        pygame.draw.polygon(window, BLACK, self.points)
    
    def update(self):
        self.move()
        self.avoid_others()

    def limit(self, vector, max_val):
        if vector.length() > max_val:
            vector.scale_to_length(max_val)
        return vector

    def check_edges(self):
        if self.x > WIDTH:
            self.x = 0
        if self.x < 0:
            self.x = WIDTH
        if self.y > HEIGHT:
            self.y = 0
        if self.y < 0:
            self.y = HEIGHT
    
    def move(self):
        self.vel += self.acc
        self.vel = self.limit(self.vel, self.max_vel)
        
        self.x += self.vel.x
        self.y += self.vel.y
        self.points = [(self.x, self.y), (self.x - 10, self.y + 10), (self.x + 10, self.y + 10)]

        self.check_edges()

    def avoid_others(self):
        move = pygame.Vector2(0, 0)
        for other in boids:
            if other != self:
                distance = pygame.Vector2(self.x - other.x, self.y - other.y).length()
                if distance < self.separation_distance:
                    move += pygame.Vector2(self.x - other.x, self.y - other.y)
        if move.length() > 0:
            self.acc = (move.normalize() * self.max_vel - self.vel).normalize()
        else:
            self.acc += pygame.Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
            self.acc = self.limit(self.acc, 1) 

# MAIN LOOP
for i in range(50):
    Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3), 3, pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)))
running = True
while running:
    window.fill(WHITE)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    for boid in boids:
        boid.update()
        boid.draw()

    pygame.display.update()