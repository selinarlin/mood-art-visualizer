import random
import pygame
import math
import sys

MENU = "menu"
VISUALIZER = "visualizer"

class Particle():
     
    def __init__(self, pos, size, life, mood):
        self.pos = list(pos)
        self.size = size
        self.mood = mood
        self.age = 0
        self.life = life
        self.dead = False

        # Color Logic
        self.color = self._get_mood_color()
        self.surface = self.update_surface()

    def _get_mood_color(self):
        # Base Mood Colors
        schemes = {
            1: [(0, 100, 255), (0, 255, 200)],      # Calm: Blue/Teal
            2: [(180, 0, 0), (255, 100, 0)],        # Chaotic: Red/Orange
            3: [(80, 80, 150), (120, 120, 220)],    # Sad: Dark Blue/Purple
            4: [(200, 150, 0), (255, 220, 100)]     # Nostalgic: Gold/ Yellow
        }
        c1, c2 = schemes.get(self.mood, [(255, 255, 255), (200, 200,200)])

        # Random Color Blends
        mix = random.random()
        return pygame.Color(
            int(c1[0] * mix + c2[0] * (1-mix)),
            int(c1[1] * mix + c2[1] * (1-mix)),
            int(c1[2] * mix + c2[2] * (1-mix)),
        )

    def update(self, dt):
        self.age += dt
        if self.age > self.life:
            self.dead = True

    def update_surface(self):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(surf, self.color, (self.size//2, self.size//2), self.size//2)
        return surf
    
    def draw(self, surface):
        alpha = 255 * (1 - (self.age / self.life))
        self.surface.set_alpha(alpha)
        surface.blit(self.surface, self.pos)


class ParticleTrail():
    def __init__(self, screen_res, mood):
        # Initiate random particle positions
        self.center = [random.randint(0, screen_res[0]), random.randint(0, screen_res[1])]
        self.radius = random.randint(20, 100)
        self.angle = random.uniform(0, math.pi * 2)

        # Random speed for each mood
        speed_mult = { 1: 0.02, 2: 0.08, 3: 0.01, 4: 0.04}
        self.rot_speed = random.uniform(0.5, 1.5) * speed_mult.get(mood, 0.02)
        self.direction = random.choice(1, -1) # clockwise/ counter-clockwise

        self.mood = mood
        self.particles = []

    def update(self, dt):
        self.angle += self.rot_speed * self.direction
        x = self.center[0] + math.cos(self.angle) * self.radius
        y = self.center[1] + maath.sin(self.angle) * self.radius

        if random.random() > 0.7:
            self.particles.append(Particle((x, y), 10, 1000, self.mood))

        for p in self.particles[:]:
            p.update(dt)
            if p.dead: self.particles.remove(p)

    def draw(self, surface):
        for p in self.particles: p.draw(surface)

    def _update_particles(self, dt):
        for idx, particle in enumerate(self.particles):
            particle.update(dt)
            if particle.dead:
                del self.particles[idx]

    def _update_pos(self):
        speeds = {1: 2, 2: 7, 3: 1, 4:3}
        speed = speeds.get(self.mood, 2)

        x, y = self.pos
        self.angle += 0.15
        x += math.sin(self.angle) * 8
        y += 4
        self.pos = (x, y)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)


class Rain():
    
    def __init__(self, screen_res):
        self.screen_res = screen_res
        self.particle_size = 15
        self.birth_rate = 1 # trails per frame
        self.trails = []
        self.fullscreen = False
        self.mood = 1

    def update(self, dt):
        self._birth_new_particles()
        self._update_trails(dt)

    def _update_trails(self, dt):
        for idx, trail in enumerate(self.trails):
            trail.update(dt)
            if self._trail_is_offscreen(trail):
                del self.trails[idx]

    def _trail_is_offscreen(self, trail):
        if not trail.particles:
            return False
        return trail.particles[-1].pos[1] > self.screen_res[1]

    def _birth_new_particles(self):
        for count in range(self.birth_rate):
            x = random.randrange(0, self.screen_res[0], self.particle_size)
            pos = (x,0)
            life = random.randrange(500, 3000)
            trail = ParticleTrail(pos, self.particle_size, life, self.mood)
            self.trails.insert(0, trail)

    def draw(self, surface):
        for trail in self.trails:
            trail.draw(surface)

def main():
    pygame.init()
    pygame.display.set_caption("Mood Visualizer")
    clock = pygame.time.Clock()

    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)
    rain = Rain(resolution)

    running = True
    while running:
        dt = clock.tick(60)
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Fullscreen toggle
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    rain.mood = int(event.unicode)

        #BG color per mood
        rain.update(dt)
        bg_colors = {1: (38, 124, 171), 2: (25, 0, 0), 3: (20, 20, 35), 4: (60, 40, 10)}
        screen.fill(bg_colors.get(rain.mood, (0,0,0)))

        rain.draw(screen)
        
        font = pygame.font. SysFont(None, 24)
        text = font.render("1: Calm | 2: Chaotic | 3: Sad | 4: Nostalgic", True, (255, 255, 255))
        screen.blit(text, (20,20))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()