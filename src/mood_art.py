import random
import pygame


class Particle():
     
    def __init__(self, pos=(0,0), size=15, life=1000):
        self.pos = pos
        self.size = size
        # Random colors
        self.color = pygame.Color(
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        self.age = 0 # in milliseconds
        self.life = life # in milliseconds
        self.dead = False
        self.alpha = 139
        
        self.shape = random.choice(['square', 'circle'])
        self.surface = self.update_surface()

    def update(self, dt):
        self.age += dt
        if self.age > self.life:
            self.dead = True
        self.alpha = 139 * (1 - (self.age / self.life))

    def update_surface(self):
        if self.shape == 'square':
            surf = pygame.Surface((self.size*0.8, self.size*0.8))
            surf.fill(self.color)
        else:
            size_int = int(self.size)
            surf = pygame.Surface((size_int, size_int), pygame.SRCALPHA)
            pygame.draw.circle(surf, self.color, (size_int//2, size_int//2), size_int//2)
        return surf
    
    def draw(self, surface):
        if self.dead:
            return
        self.surface.set_alpha(self.alpha)
        surface.blit(self.surface, self.pos)


class ParticleTrail():
    def __init__(self, pos, size, life):
        self.pos = pos
        self.size = size
        self.life = life
        self.particles = []

    def update(self, dt):
        particle = Particle(self.pos, size=self.size, life=self.life)
        self.particles.insert(0, particle)
        self._update_particles(dt)
        self._update_pos()

    def _update_particles(self, dt):
        for idx, particle in enumerate(self.particles):
            particle.update(dt)
            if particle.dead:
                del self.particles[idx]

    def _update_pos(self):
        x, y = self.pos
        y += self.size
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
        trail_is_offscreen = trail.particles[-1].pos[1] > self.screen_res[1]
        return trail_is_offscreen

    def _birth_new_particles(self):
        for count in range(self.birth_rate):
            screen_width = self.screen_res[0]
            x = random.randrange(0, screen_width, self.particle_size)
            pos = (x,0)
            life = random.randrange(500, 3000)
            trail = ParticleTrail(pos, self.particle_size, life)
            self.trails.insert(0, trail)

    def draw(self, surface):
        for trail in self.trails:
            trail.draw(surface)

def main():
    pygame.init()
    pygame.display.set_caption("Mood Visualizer")
    clock = pygame.time.Clock()
    dt = 0

    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)
    rain = Rain(resolution)

    running = True
    while running:
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Fullscreen toggle
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if not rain.fullscreen:
                        resolution = (1920, 1080)
                        screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
                        rain.fullscreen = True
                        rain.screen_res = resolution
                    else:
                        resolution = (800, 600)
                        screen = pygame.display.set_mode(resolution)
                        rain.fullscreen = False
                        rain.screen_res = resolution

        # Game logic
        rain.update(dt)
        # Render & Display
        orange = pygame.Color(242, 193, 119)
        screen.fill(orange)
        rain.draw(screen)
        pygame.display.flip()

        dt = clock.tick(12)
    pygame.quit()


if __name__ == "__main__":
    main()