import pygame

class Button(pygame.sprite.Sprite):

    def __init__(self, x ,y,w,h,type,font, text ,link=None):
        super().__init__()
        self.font = font
        self.text = text
        self.text_surf = font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center = (w // 2, h // 2))
        
        #setting du boutton standard
        self.button_image = pygame.Surface((w, h))
        self.button_image.fill((226, 226, 226))
        self.button_image.blit(self.text_surf, self.text_rect)

        #setting du boutton survolé
        self.hover_image = pygame.Surface((w, h))
        self.hover_image.fill((96, 96, 96))
        self.hover_image.blit(self.text_surf, self.text_rect)

        pygame.draw.rect(self.hover_image, (96, 96, 250), self.hover_image.get_rect(), 3)
        self.image = self.button_image
        self.rect = pygame.Rect(x, y, w, h)
        self.clicked = False
        self.buttons = None
        self.link = link
        self.type = type
    