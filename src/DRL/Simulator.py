from src.DRL.Environment import SimplifiedRoboEnv
import random
import numpy as np
import pygame
from pygame.locals import *





def TestRandomPolicy(env):
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('This is a simulation!')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))

    """
    completely random policy in environment
    """
    environment = env
    time_step = environment.reset()
    print(time_step)
    cumulative_reward = time_step.reward
    # background.blit(Rob, pos)
    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    for _ in range(100000):
        action = np.array([random.uniform(-10, 10), random.uniform(-1, 1)], dtype=np.float32)
        time_step = environment.step(action)
        screen.blit(background, (0, 0))  # erase
        state = environment.get_state()
        pygame.draw.rect(surface=background, color=(255, 0, 0), rect=pygame.Rect(state[0][0], state[0][1], 1, 1))
        pygame.draw.rect(surface=background, color=(127, 127, 127), rect=pygame.Rect(state[1][0], state[1][1], 10, 10))
        pygame.display.update()  # and show it all
        pygame.time.delay(100)
        cumulative_reward += time_step.reward

    print('Final Reward = ', cumulative_reward)


    # Event loop
    # while 1:
    #    for event in pygame.event.get():
    #        if event.type == QUIT:
     #           return

     #   screen.blit(background, (0, 0))
    #    pygame.display.flip()


if __name__ == '__main__':
    env = SimplifiedRoboEnv()
    display(env)