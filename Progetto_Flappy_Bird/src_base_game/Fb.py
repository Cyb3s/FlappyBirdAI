import pygame
import random
from Or_player import Player
from Or_pipe import Pipe
import os
import time
import neat
import visualize
import pickle

# Function to display the alert message
def show_alert(display, message):
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, (255, 0, 0))
    text_rect = text.get_rect(center=(display.get_width() / 2, display.get_height() / 2))
    display.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def draw_text(display,text, font, text_color,x,y):
    img = font.render(text, True, text_color)
    display.blit(img, (x, y))

def main():
    pygame.init()
    pygame.event.wait(5000)
    #environment variables
    FPS = 60
    clock = pygame.time.Clock()
    pipe_frequency = 1500 #milliseconds
    last_pipe = pygame.time.get_ticks() -pipe_frequency
    running = True
    sfondo_x = 0 #Initial x position of the background
    grass_x = 0 #Initial x position of the grass 
    score=0
    pass_pipe=False
    font = pygame.font.SysFont('Bauhaus 93', 60)
    white = (255, 255, 255)
    
    
    #set up the display
    display = pygame.display.set_mode((864, 836))
    pygame.display.set_caption("FlappyBird")
    backgroundColor = (122, 227, 243)
    display.fill(backgroundColor)

    #load images
    background=pygame.image.load('sprite\\background.png').convert()
    grass=pygame.image.load('sprite\\grass.png').convert()
    
    
    player = Player(25, 25, 'sprite\\pgBird.png')
    player.setUp_Player(1, 150, 275)


    bird_list = pygame.sprite.Group()
    pipe_list = pygame.sprite.Group()
    bird_list.add(player)
    
    

    while running:
        #generate pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(864, 375+pipe_height, 'sprite\\pipe.png', False)
            top_pipe = Pipe(864, 375+pipe_height, 'sprite\\pipe.png', True)
            pipe_list.add(top_pipe)  
            pipe_list.add(btm_pipe)
            last_pipe = time_now
        pipe_list.update()
        
        #stamp the image and sprites onto the screen 
        display.blit(background, (sfondo_x,0 ))
        display.blit(background, (sfondo_x + 864,  0 ))
        pipe_list.draw(display)
        display.blit(grass, (grass_x, 860-160))
        display.blit(grass, (grass_x + 864, 860-160))
        bird_list.draw(display)


        # Move the background
        sfondo_x -= 0.25
        if sfondo_x <= -864:
            sfondo_x = 0

        grass_x -= 5
        if grass_x <= -864:
            grass_x = 0
  
        bird_list.update()
        
        #check the score
        if len(pipe_list) > 0:
            if bird_list.sprites()[0].rect.left > pipe_list.sprites()[0].rect.left\
                and bird_list.sprites()[0].rect.right < pipe_list.sprites()[0].rect.right\
                and pass_pipe == False:
                pass_pipe = True
            if pass_pipe == True:
                if bird_list.sprites()[0].rect.left > pipe_list.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False
                    print("Score: ", score)
                    #864, 836
        draw_text(display,str(score), font, white, int(836/2), 20)
        
        #player touch ground
        if player.rect.y > 836-215 or pygame.sprite.groupcollide(bird_list, pipe_list, False,False) or player.rect.y < 0:
            start_time = pygame.time.get_ticks()  # Registra il tempo iniziale
            while pygame.time.get_ticks() - start_time < 30:  # Aspetta 500 millisecondi
                # Continua ad aggiornare il movimento del giocatore e il display
                pipe_list.update()
                bird_list.update()
                
                display.blit(background, (sfondo_x, 0))
                display.blit(background, (sfondo_x + 864, 0))
                pipe_list.draw(display)
                display.blit(grass, (grass_x, 860 - 160))
                display.blit(grass, (grass_x + 864, 860 - 160))
                bird_list.draw(display)
                
                pygame.display.flip()
                clock.tick(FPS)
            show_alert(display,"Game Over")
            running = False
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.rotateUp(45)
                    player.setVelocity(-8)       
        pygame.display.update()
        clock.tick(FPS)
        
    return 0



if __name__ == "__main__":
    main()
    pygame.quit()
    quit()