import pygame

class Button:
    def __init__(self, x, y, w, h, text, callback=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback  # <-- NEW
        self.font = pygame.font.SysFont("consolas", 18)
        self.hovered = False

    def draw(self, surface):
        color = (100, 100, 200) if self.hovered else (80, 80, 160)
        pygame.draw.rect(surface, color, self.rect)
        label = self.font.render(self.text, True, (255, 255, 255))
        surface.blit(label, (self.rect.x + 10, self.rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print(f"{self.text} button clicked")
                if self.callback:
                    self.callback()  # <-- NEW


class RadioSelector:
    def __init__(self, x, y, options, default_index=0):
        self.options = options
        self.selected = default_index
        self.font = pygame.font.SysFont("consolas", 16)
        self.x = x
        self.y = y

    def draw(self, surface):
        for i, option in enumerate(self.options):
            is_selected = i == self.selected
            color = (200, 200, 50) if is_selected else (200, 200, 200)
            pygame.draw.circle(surface, color, (self.x, self.y + i * 30), 10)
            label = self.font.render(option, True, color)
            surface.blit(label, (self.x + 20, self.y - 10 + i * 30))

    def get_selected(self):
        return self.options[self.selected]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(self.options)):
                circle_rect = pygame.Rect(self.x - 10, self.y + i * 30 - 10, 20, 20)
                if circle_rect.collidepoint(event.pos):
                    self.selected = i
                    print(f"Selected: {self.options[i]}")


class Checkbox:
    def __init__(self, x, y, label="", checked=False):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.checked = checked
        self.label = label
        self.font = pygame.font.SysFont("consolas", 16)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
        if self.checked:
            pygame.draw.line(surface, (0, 255, 0), self.rect.topleft, self.rect.bottomright, 3)
            pygame.draw.line(surface, (0, 255, 0), self.rect.topright, self.rect.bottomleft, 3)

        label_surf = self.font.render(self.label, True, (200, 200, 200))
        surface.blit(label_surf, (self.rect.right + 10, self.rect.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
                print(f"Checkbox {'checked' if self.checked else 'unchecked'}")

    def is_checked(self):
        return self.checked
