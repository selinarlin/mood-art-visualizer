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
        y = self.center[1] + math.sin(self.angle) * self.radius

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


class App():
    
    def __init__(self):
        pygame.init()
        self.res = (1000, 700)
        self.screen = pygame.display.set_mode(self.res)
        self.clock = pygame.time.Clock()
        self.state = MENU
        self.mood = 1
        self.trails = []

    def draw_button(self, text, rect, color):
        mouse = pygame.mouse.get_pos()
        # Hover effect
        draw_color = (color[0]+30, color[1]+30, color[2]+30) if rect.collidepoint(mouse) else color
        pygame.draw.rect(self.screen, draw_color, rect, border_radius=10)
        font = pygame.font.SysFont(None, 30)
        img = font.render(text, True, (255, 255, 255))
        self.screen.blit(img, (rect.x + (rect.width - img.get_width())//2, rect.y + 15))

    def run(self):
        while True:
            if self.state == MENU:
                self.menu_loop()
            else:
                self.visualizer_loop()
    
    def menu_loop(self):
        self.screen.fill((30, 30, 30))
        btn_width, btn_height = 200, 50
        # Buttons
        buttons = {
            1: pygame.Rect(self.res[0]//2 - 100, 200, btn_width, btn_height),
            2: pygame.Rect(self.res[0]//2 - 100, 270, btn_width, btn_height),
            3: pygame.Rect(self.res[0]//2 - 100, 340, btn_width, btn_height),
            4: pygame.Rect(self.res[0]//2 - 100, 410, btn_width, btn_height),
            "quit": pygame.Rect(self.res[0]//2 - 100, 550, btn_width, btn_height)
        }

        for mood_id, rect in buttons.items():
            text =f"Mood {mood_id}" if isinstance(mood_id, int) else "Quit Game"
            color = (50, 50, 150) if isinstance(mood_id, int) else (150, 50, 50)
            self.draw_button(text, rect, color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for mood_id, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        if mood_id == "quit": pygame.quit(); sys.exit()
                        self.mood = mood_id
                        self.trails = [ParticleTrail(self.res, self.mood) for _ in range(15)]
                        self.state = VISUALIZER
        
        pygame.display.flip()

    def visualizer_loop(self):
        self.screen.fill((10, 10, 20))
        back_btn = pygame.Rect(20, 20, 150, 40)
        self.draw_button("Return to Menu", back_btn, (100, 100, 100))

        for trail in self.trails:
            trail.update(16)
            trail.draw(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidpoint(event.pos):
                    self.state = MENU
        
        pygame.display.flip()
        self.clock.tick(60)

if __name__ == "__main__":
    App().run()