# gui/widgets.py
import pygame

class Button:
    def __init__(self, x, y, w, h, text, callback=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
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
                    self.callback()


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


class TextBox:
    def __init__(self, x, y, width=60, height=30, label="", default="25", min_val=10, max_val=100):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.text = default
        self.font = pygame.font.SysFont("consolas", 18)
        self.active = False
        self.min_val = min_val
        self.max_val = max_val

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():
                self.text += event.unicode

    def draw(self, surface):
        # Draw background color based on validation
        color = (255, 200, 200) if not self.is_valid() else (255, 255, 255)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)

        # Draw text inside the box
        txt_surface = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))

        # Draw label above
        if self.label:
            label_surface = self.font.render(self.label, True, (200, 200, 200))
            surface.blit(label_surface, (self.rect.x, self.rect.y - 20))

    def get_value(self):
        try:
            return int(self.text)
        except ValueError:
            return None

    def is_valid(self):
        val = self.get_value()
        return val is not None and self.min_val <= val <= self.max_val

