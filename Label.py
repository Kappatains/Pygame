import pygame

class Label(pygame.sprite.Sprite):
    def __init__(self, x , y, w, h, type, font, text):
        super().__init__()
        self.text = text
        self.type = type
        self.font = font
        self.label_image = pygame.Surface((w, h))
        self.text_surf = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center = (w // 2, h // 2))

        self.label_image.fill((226, 226, 226))
        self.label_image.blit(self.text_surf, self.text_rect)
        self.image = self.label_image
        self.rect = pygame.Rect(x, y, w, h)

    #Plus utilisé
    # def updateLabel(self, value):
    #     self.text = value
    #     self.text_surf = self.font.render(self.text, True, (0, 0, 0))
    #     self.label_image.fill((226, 226, 226))
    #     self.label_image.blit(self.text_surf, self.text_rect)
        
        