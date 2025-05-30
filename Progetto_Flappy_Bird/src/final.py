import pygame
import random
from player import Player
from pipe import Pipe
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

def eval_genomes(genomes, config):
    pygame.init()

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
    pipe_index=0
    font = pygame.font.SysFont('Bauhaus 93', 60) 
    white = (255, 255, 255)
    global  gen 
    
    nets = []
    ge = []
    players = []

    #create the players
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(Player(25,25,'sprite\\pgBird.png'))
        players[-1].setUp_Player(1, 150, 275)
        ge.append(genome)
    
    #set up the display
    display = pygame.display.set_mode((864, 836))
    pygame.display.set_caption("FlappyBird")
    backgroundColor = (122, 227, 243)
    display.fill(backgroundColor)

    #load images
    background=pygame.image.load('sprite\\background.png').convert()
    grass=pygame.image.load('sprite\\grass.png').convert()
    

    pipe_list = pygame.sprite.Group()
    

    while running and len(players) > 0:
       
        #generate pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(864, 375+pipe_height, 'sprite\\pipe.png', False)
            top_pipe = Pipe(864, 375+pipe_height, 'sprite\\pipe.png', True)
            pipe_list.add(top_pipe)  
            pipe_list.add(btm_pipe)
            last_pipe = time_now
        
        #stamp the image and sprites onto the screen 
        display.blit(background, (sfondo_x,0 ))
        display.blit(background, (sfondo_x + 864,  0 ))
        pipe_list.draw(display)
        for player in players:
            display.blit(player.image,player.rect)
        display.blit(grass, (grass_x, 860-160))
        display.blit(grass, (grass_x + 864, 860-160))
        draw_text(display,str(score), font, white, int(836/2), 20)
        
        if len(players) > 0:
            if pipe_index < len(pipe_list.sprites()) and players[0].rect.x > pipe_list.sprites()[pipe_index].rect.x + 100:  # determine whether to use the first or second
                pipe_index+=2

        for x, player in enumerate(players):  # give each bird a fitness of 0.1 for each frame it stays alive
            ge[x].fitness += 0.1

            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output = nets[players.index(player)].activate((player.rect.y, abs(player.rect.y - pipe_list.sprites()[pipe_index+1].height), abs(player.rect.y - pipe_list.sprites()[pipe_index].bottom)))

            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                player.jump()

        # Move the background
        sfondo_x -= 0.25
        if sfondo_x <= -864:
            sfondo_x = 0

        grass_x -= 5
        if grass_x <= -864:
            grass_x = 0
 

        pipe_list.update()
        for player in players:
            player.update()
     

        for player in players:
            #check the score
            if len(pipe_list) > 0:
                if player.rect.left > pipe_list.sprites()[0].rect.left\
                    and player.rect.right < pipe_list.sprites()[0].rect.right\
                    and pass_pipe == False:
                    pass_pipe = True
                if pass_pipe == True:
                    if player.rect.left > pipe_list.sprites()[0].rect.right:
                        score += 1
                        for genome in ge:
                            genome.fitness += 5
                        pass_pipe = False
                        print("Score: ", score)
            
           
        for player in players:
        #player touch ground
            if player.rect.y > 836-215 or pygame.sprite.spritecollide(player, pipe_list, False) or player.rect.y < 0:
                ge[players.index(player)].fitness -= 1  # if player dies, reduce fitness    
                nets.pop(players.index(player))
                ge.pop(players.index(player))
                players.pop(players.index(player))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
                break     
                
        pygame.display.update()
        clock.tick(FPS)
        
    return 0

def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    config_dir = r"c:\Users\Utente\Documents\Capolavoro\Progetto_Flappy_Bird\config" 
    config_path = os.path.join(config_dir, 'config-feedforward.txt')
    run(config_path)

