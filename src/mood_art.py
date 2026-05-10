import random
import pygame
import math
import sys

MENU = "menu"
VISUALIZER = "visualizer"

class Particle():
     
    def __init__(self, pos, vel, size, life, mood):
        self.pos = list(pos)
        self.vel = vel
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
            4: [(200, 150, 0), (255, 220, 100)]     # Nostalgic: Gold/Yellow
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

        self.pos[0] += self.vel[0] * dt * 0.05
        self.pos[1] += self.vel[1] * dt * 0.05

        if self.age > self.life:
            self.dead = True

    def update_surface(self):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(surf, self.color, (self.size//2, self.size//2), self.size//2)
        return surf
    
    def draw(self, surface):
       progress = self.age / self.life
       # Spiral stay visible for first 70%
       if progress < 0.7:
           alpha = 255
        # Fade last 30%
       else:
           fade_progress = (progress - 0.7) / 0.3
           alpha = int(255 * (1 - fade_progress))
           
       alpha = max(0, min(255, alpha))
       
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
        self.direction = random.choice([1, -1]) # clockwise/ counter-clockwise

        self.mood = mood
        self.particles = []

    def update(self, dt):
        self.angle += self.rot_speed * self.direction
        x = self.center[0] + math.cos(self.angle) * self.radius
        y = self.center[1] + math.sin(self.angle) * self.radius

        if random.random() > 0.7:
        # Spiral movement direction
            vx = math.cos(self.angle + math.pi / 2) * 2
            vy = math.sin(self.angle + math.pi / 2) * 2

            self.particles.append(
                Particle((x, y), (vx, vy), 10, 3000, self.mood)
        )

        for p in self.particles:
            p.update(dt)

        self.particles = [p for p in self.particles if not p.dead]

    def draw(self, surface):
        for p in self.particles: p.draw(surface)


class App():
    
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.res = (1000, 700)
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption("Mood Art Visualizer")
        self.clock = pygame.time.Clock()
        self.state = MENU
        self.mood = 1
        self.trails = []
        self.running = True

    def draw_button(self, text, rect, color):
        mouse = pygame.mouse.get_pos()
        # Hover effect
        draw_color = (min(color[0]+30, 255), min(color[1]+30, 255), min(color[2]+30, 255)) if rect.collidepoint(mouse) else color
        pygame.draw.rect(self.screen, draw_color, rect, border_radius=10)
        font = pygame.font.SysFont(None, 30)
        img = font.render(text, True, (255, 255, 255))
        self.screen.blit(img, (rect.x + (rect.width - img.get_width())//2, rect.y + 15))

    def run(self):
        while self.running:
            dt = self.clock.tick(60)
            if self.state == MENU:
                self.menu_loop()
            else:
                self.visualizer_loop(dt)
        
        pygame.quit()
        sys.exit()
    
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

        mood_names = {1: "Calm", 2: "Chaotic", 3: "Sad", 4: "Nostalgic"}

        for mood_id, rect in buttons.items():
            text = mood_names[mood_id] if isinstance(mood_id, int) else "Quit Game"
            color = (50, 50, 50) if isinstance(mood_id, int) else (150, 50, 50)
            self.draw_button(text, rect, color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for mood_id, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        if mood_id == "quit":
                            self.running = False
                        else:
                            self.mood = mood_id
                            self.trails = [ParticleTrail(self.res, self.mood) for _ in range(10)]
                            self.state = VISUALIZER
        
        pygame.display.flip()

    def visualizer_loop(self, dt):
        self.screen.fill((10, 10, 20))
        back_btn = pygame.Rect(20, 20, 150, 40)
        self.draw_button("Return to Menu", back_btn, (100, 100, 100))

        for trail in self.trails:
            trail.update(dt)
            trail.draw(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    self.state = MENU
        
        pygame.display.flip()

if __name__ == "__main__":
    App().run()