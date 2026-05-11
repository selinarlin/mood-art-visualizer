import random
import pygame
import math
import sys

used_centers = []
ui_block = None

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
            1: [(255, 138, 198), (255, 84, 158)],      # Calm: Pink
            2: [(180, 0, 0), (255, 100, 0)],        # Mad: Red/Orange
            3: [(8, 140, 196), (45, 23, 71)],    # Sad: Dark Blue/Purple
            4: [(255, 176, 100), (255, 197, 82)]     # Nostalgic: Yellow/Orange
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
        margin = 80
        min_distance = 180
        
        while True:
            candidate = [
                random.randint(margin, screen_res[0] - margin),
                random.randint(margin, screen_res[1] - margin)
            ]

            if (
                all(math.dist(candidate, c) > min_distance for c in used_centers)
                and (ui_block is None or not ui_block.collidepoint(candidate))
            ):
                used_centers.append(candidate)
                self.center = candidate
                break

        self.spiral_scale = random.uniform(0.6, 2.5)
        self.radius = random.randint(20, 100) * self.spiral_scale
        self.trail_size = random.randint(6, 40)
        self.trail_variation = random.uniform(0.85, 1.15)
        self.angle = random.uniform(0, math.pi * 2)

        # Random speed for each mood
        speed_mult = { 1: 0.06, 2: 0.1, 3: 0.02, 4: 0.04}
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
            vx, vy = 0, 0

            size = int(self.trail_size * self.trail_variation)

            self.particles.append(
                Particle((x, y), (0, 0), size, 3000, self.mood)
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
        font = pygame.font.SysFont(None, 25)
        img = font.render(text, True, (255, 255, 255))
        self.screen.blit(img, (rect.x + (rect.width - img.get_width())//2, rect.y + 15))

    def run(self):
        while self.running:
            dt = self.clock.tick(60)

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            if self.state == MENU:
                self.menu_loop(events)
            else:
                self.visualizer_loop(dt, events)
        
        pygame.quit()
        sys.exit()
    
    def menu_loop(self, events):
        self.screen.fill((0, 0, 0))
        btn_width, btn_height = 200, 50
        title_font = pygame.font.SysFont(None, 100)
        title_text = title_font.render("Visualize Your Mood!", True, (255, 255, 255))
        self.screen.blit(
            title_text,
            (self.res[0]//2 - title_text.get_width()//2, 65)
        )
    
        # Buttons
        buttons = {
            1: pygame.Rect(self.res[0]//2 - 100, 200, btn_width, btn_height),
            2: pygame.Rect(self.res[0]//2 - 100, 270, btn_width, btn_height),
            3: pygame.Rect(self.res[0]//2 - 100, 340, btn_width, btn_height),
            4: pygame.Rect(self.res[0]//2 - 100, 410, btn_width, btn_height),
            "quit": pygame.Rect(self.res[0]//2 - 100, 550, btn_width, btn_height)
        }

        mood_names = {1: "Calm", 2: "Mad", 3: "Sad", 4: "Nostalgic"}

        for mood_id, rect in buttons.items():
            text = mood_names[mood_id] if isinstance(mood_id, int) else "Quit Game"
            mood_colors = {
                1: (105, 166, 51),
                2: (180, 0, 0),
                3: (8, 140, 196),
                4: (247, 165, 72)
            }
            color = mood_colors.get(mood_id, (54, 54, 54))
            self.draw_button(text, rect, color)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for mood_id, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        if mood_id == "quit":
                            self.running = False
                        else:
                            self.mood = mood_id
                            used_centers.clear()
                            self.trails = [ParticleTrail(self.res, self.mood) for _ in range(10)]
                            self.state = VISUALIZER
        
        pygame.display.flip()

    def visualizer_loop(self, dt, events):
        
        if self.mood == 1: # calm
            self.screen.fill((105, 166, 51))
        elif self.mood == 2: # mad
            self.screen.fill((51, 20, 9))
        elif self.mood == 3: # sad
            self.screen.fill((10, 12, 36))
        elif self.mood == 4: # nostalgic
            self.screen.fill((247, 165, 72))
        else:
            self.screen.fill((10, 10, 20))

        back_btn = pygame.Rect(20, 20, 150, 40)

        ui_padding = 20
        global ui_block

        ui_block = pygame.Rect(
            back_btn.x - ui_padding,
            back_btn.y - ui_padding,
            back_btn.width + ui_padding * 2,
            back_btn.height + ui_padding * 2
        )

        for trail in self.trails:
            trail.update(dt)
            trail.draw(self.screen)

        self.draw_button("Return to Menu", back_btn, (54, 54, 54))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    self.state = MENU
        
        pygame.display.flip()

if __name__ == "__main__":
    App().run()