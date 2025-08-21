import pygame

class Player(pygame.sprite.Sprite):
    
    x = 0  
    y = 0 
    
    def __init__(self, height, width, img):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = pygame.image.load(img)
        self.original_image = img
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        # Store the current angle of the Player
        self.angle = 0  
        self.velocity = 0
        self.gen=0 
       

    def setUp_Player(self, layer, x, y):
        self.layer = layer
        self.rect.x = x  # go to
        self.rect.y = y  # go to y
        self.x = x  # Store initial x position
        self.y = y  # Store initial y position

    def rotateUp(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def rotateDown(self, angle):
        self.angle += angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def jump(self):
        self.rotateUp(45)
        self.setVelocity(-8)

    def update(self):
        self.velocity += 0.5
        if self.velocity > 10:
            self.velocity = 10
        self.rect.y += int(self.velocity)
        
        if self.angle > -90:
            self.rotateDown(-1)
            self.angle -= 1
            
    def setVelocity(self, velocity):
        self.velocity = velocity