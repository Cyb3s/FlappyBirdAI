import pygame

pipe_gap = 150

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, img, flip):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        if flip:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y-int(pipe_gap/2))
        else:
            self.rect.topleft = (x, y+int(pipe_gap/2))
            
    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()
