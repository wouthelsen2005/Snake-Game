import pygame, sys, time, threading
from pygame.locals import QUIT

def handle_events(snake, game):
  events = pygame.event.get()
  for event in events:
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_DOWN:
        event_key = event.key
      if event.key == pygame.K_UP:  
        event_key = event.key
      if event.key == pygame.K_RIGHT:
        event_key = event.key
      if event.key == pygame.K_LEFT:
        event_key = event.key
      try:
        t = threading.Thread(target= controls, args = (snake,game,event_key)) #start a thread that constant checks if the snake should be able to move 
        t.start()
      except:
        pass
      
      if event.key == pygame.K_SPACE:
        if game.playing:
          game.playing = False
        else:
          game.playing = True
      
          

def check_collision(snake,fruits_sprites, crates_spirtes):
  fruit = pygame.sprite.spritecollideany(snake.blocks[1], fruits_sprites)
  try:
    fruit.kill()
    snake.make_snake_longer()
  except:
    pass
  crate = pygame.sprite.spritecollideany(snake.blocks[1], crates_spirtes)
  if snake.imune == False:
    try:
      crate.kill()
      snake.alive = False
    except:
      pass
      
def move_snake(snake_direction,snake_blocks):
  if snake_direction[0] == 1:
    snake_blocks[0].pos = (snake_blocks[1].pos[0] + 5, snake_blocks[1].pos[1])
  if snake_direction[1] == -1:
    snake_blocks[0].pos = (snake_blocks[1].pos[0], snake_blocks[1].pos[1] - 5 )
  if snake_direction[0] == -1:
    snake_blocks[0].pos = (snake_blocks[1].pos[0] -5, snake_blocks[1].pos[1])
  if snake_direction[1] == 1:
    snake_blocks[0].pos = (snake_blocks[1].pos[0] , snake_blocks[1].pos[1] + 5)

def move_list(list): #move the list with 1
  a = list
  x = a.pop()
  a.insert(0, x)
  return a

def make_playboard(screen):  
  for len in range(0,500,50):
    for height in range(0,500,50):
      pygame.draw.rect(screen, (162,205,90), (len,height,25,25))
  for len in range(25,500,50):
    for height in range(25,500,50):
      pygame.draw.rect(screen, (162,205,90), (len,height,25,25))
  for len in range(0,500,50):
    for height in range(25,500,50):
      pygame.draw.rect(screen, (130,205,90), (len,height,25,25))
  for len in range(25,500,50):
    for height in range(0,500,50):
      pygame.draw.rect(screen, (130,205,90), (len,height,25,25))

  
def controls(snake, game, event_key):
  done = False
  while not done:
    if snake.distance_travelled % 25 == 0:
      snake.set_distance_travelled()  #set the distance back to 0
      done = True
      if event_key == pygame.K_DOWN and snake.direction != [0,-1]:
        snake.direction = [0,1]
      if event_key == pygame.K_UP and snake.direction != [0,1]:
        snake.direction = [0,-1]
      if event_key == pygame.K_LEFT and snake.direction != [1,0]:
        snake.direction = [-1,0]
      if event_key == pygame.K_RIGHT and snake.direction != [-1,0]:
        snake.direction = [1,0]
    time.sleep(0.01)  #set timer so program doesn't get stuck
    
  
  
    
  
   



