import pygame
import random

pygame.init()

# CONSTANTS (Update for interesting results)
NUM_BOIDS = 100
EDGE_MARGIN = 150
EYE_RANGE = 150 
MAX_SPEED = 15 
MIN_SPEED = 3 
INIT_SPEED = 15 
MIN_DISTANCE = 10 
SEPARATION = 0.05
COHESION = 0.015
ALIGNMENT = 0.015

# WINDOW
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boid Simulation")

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# BOID CLASS 
class Boid:
    pass 

global_boids = [] # stores all the boids currently in the scene

# FUNCTIONS
def init_boids():
    boids = []
    for i in range(NUM_BOIDS):
        boid = Boid()
        boid.loc = complex(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        boid.vel = complex(random.randint(0, INIT_SPEED), random.randint(0, INIT_SPEED))
        boids.append(boid)
    return boids

def edge_constraint(boid):
    if (boid.loc.real < EDGE_MARGIN):
        boid.vel += 0.4+0j
    if (boid.loc.real > WIDTH - EDGE_MARGIN) :
        boid.vel += -0.4+0j
    if (boid.loc.imag < EDGE_MARGIN) :
        boid.vel += 0+0.4j
    if (boid.loc.imag > HEIGHT - EDGE_MARGIN) :
        boid.vel += 0-0.4j

def cohesion(boid):
    center = 0+0j
    neighbours = 0
    for other_boid in global_boids:
        if abs(boid.loc - other_boid.loc) < EYE_RANGE :
            center += other_boid.loc
            neighbours += 1
    if neighbours > 0 :
        center = center / neighbours
    boid.loc += (center - boid.loc) * COHESION

def avoid_other_boids(boid):
    move = 0+0j
    for other_boid in global_boids :
        if not (other_boid is boid) :
            if abs(boid.loc - other_boid.loc) < MIN_DISTANCE :
                move += boid.loc - other_boid.loc
    boid.vel += move * SEPARATION

def match_flying_speed(boid):
    avg_vel = 0+0j
    neighbours = 0
    for otherBoid in global_boids:
        if abs(boid.loc - otherBoid.loc) < EYE_RANGE :
            avg_vel += otherBoid.vel
            neighbours += 1
    if neighbours > 0:
        avg_vel /= neighbours
    boid.vel += (avg_vel - boid.vel) * ALIGNMENT

def limit_speed(boid):
    speed = abs(boid.vel)
    if (speed > MAX_SPEED) :
        boid.vel = boid.vel / speed * MAX_SPEED
    if (speed < MIN_SPEED) :
        boid.vel = boid.vel / speed * MIN_SPEED

def draw_boid(boid):
    # draw circle head
    pygame.draw.circle(window, WHITE, (int(boid.loc.real), int(boid.loc.imag)), 5)
    tail = boid.loc + boid.vel * 1.8
    # draw line tail
    pygame.draw.line(window, RED, (int(boid.loc.real), int(boid.loc.imag)), (int(tail.real), int(tail.imag)))

def draw():
    window.fill((0, 0, 0))
    for boid in global_boids:
        draw_boid(boid)

def update():
    for boid in global_boids:
        # Rules for flocking algorithm
        cohesion(boid)
        avoid_other_boids(boid)
        match_flying_speed(boid)
        limit_speed(boid)
        edge_constraint(boid)
        boid.loc += boid.vel

global_boids = init_boids()

# MAIN FUNCTION
def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60) 
        window.fill(WHITE)

        # Draw boids
        draw()
        update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()