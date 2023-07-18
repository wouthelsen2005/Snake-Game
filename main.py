import pygame, sys
from pygame.locals import QUIT
from Objects import *
from Functions import *

game = Game()

game.prepare_game()
while game.snake.alive:
 
  game.run()
  check_collision(game.snake,fruit_sprites, crate_sprites)
  handle_events(game.snake, game)
  


  
  
  