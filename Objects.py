import pygame, sys, random
import threading
import time
from Functions import *
import numpy as np

pygame.init()
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0,0,0)
WINDOW = (500,500)
SCREEN = pygame.display.set_mode(WINDOW)
pygame.display.set_caption('Snake')
CLOCK = pygame.time.Clock()
fruit_image = pygame.image.load("fruitt-removebg-preview.png")
fruit_image = pygame.transform.scale(fruit_image, (25,25))
crate_image = pygame.image.load("download (1).jpg")
crate_image = pygame.transform.scale(crate_image, (50,50))
all_sprites = pygame.sprite.Group()
all_sprites_drawn = pygame.sprite.Group()
fruit_sprites = pygame.sprite.Group()
crate_sprites = pygame.sprite.Group()


  

class Snake(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.lengt = 1
    self.blocks = [Block((0,0)),Block((0,0))]
    self.direction = [1,0]
    self.alive = True
    self.imune = False
    self.distance_travelled = 0
    
  def eyes(self):
    pygame.draw.circle()

  def update(self):
    self.move()
    self.check_death()
    
  def move(self):  
    move_snake(self.direction,self.blocks) #move the snake 
    self.distance_travelled += 5
    move_list(self.blocks)  #move every block 1 place is the list
    for block in self.blocks:
      block.update_pos()
      
  def make_snake_longer(self): #make the snake longer
    for i in range(5):
      block = Block(self.blocks[1].pos)
      self.blocks.append(block)
      all_sprites.add(block)
      all_sprites_drawn.add(block)
    
  def check_death(self): #see if the snake hits an object
    for block in self.blocks:
      if self.blocks[1].pos == block.pos and block != self.blocks[1]:
        self.alive = False

  def set_distance_travelled(self): #set the distance travelled back to 0
    self.distance_travelled = 0
        


class Block(pygame.sprite.Sprite):
  def __init__(self,start_pos):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface((25,25))
    self.pos = start_pos
    self.color = (0,154,205)
    self.image.fill(self.color)
   
  def update(self):
    pass
    
  def update_pos(self):
    self.rect = pygame.Rect((self.pos),(25,25))

  
    
    

class Fruit(pygame.sprite.Sprite):
  def __init__(self,spawnpositions):
    pygame.sprite.Sprite.__init__(self)
    self.image = fruit_image
    self.rect = self.image.get_rect()
    self.spawnpositions = spawnpositions
    self.pos = self.deside_pos()
    
   
  def update(self):
     self.rect = pygame.Rect((self.pos),(25,25))
    
 
  def deside_pos(self):
    flat_x = self.spawnpositions.flatten()
    random_element = np.random.choice(flat_x)
    while random_element == 0:   #check if the spawn positions is taken
      random_element = np.random.choice(flat_x)
    location = np.where(self.spawnpositions == random_element)
    row_index = location[0][0]
    column_index = location[1][0]
    pos_x = 50*row_index
    
    pos_y = 50*column_index
   
    self.spawnpositions[self.spawnpositions == random_element] = int(0)
    
    return (pos_x,pos_y)

class Crate(pygame.sprite.Sprite):
  def __init__(self,spawnpositions):
    pygame.sprite.Sprite.__init__(self)
    self.spawnpositions = spawnpositions
    self.image = crate_image
    self.pos = self.deside_pos()
    self.rect = self.image.get_rect()


  def update(self):
     self.rect = pygame.Rect((self.pos),(35,35))

  def deside_pos(self):
    flat_x = self.spawnpositions.flatten()
    random_element = np.random.choice(flat_x)
    while random_element == 0:  #check if the spawn positions is taken
      random_element = np.random.choice(flat_x)
    location = np.where(self.spawnpositions == random_element)
    row_index = location[0][0]
    column_index = location[1][0]
    pos_x = 50*row_index
   
    pos_y = 50*column_index
   

    self.spawnpositions[self.spawnpositions == random_element] = int(0)

    return (pos_x,pos_y)
    

  
    
    

class Game():
  def __init__(self):
    self.screen = SCREEN
    self.snake = Snake()
    self.alive = True
    self.fruit_amount = 3
    self.FPS = 30
    self.playing = True
    all_sprites.add(self.snake)
    self.add_blocks_to_snake()
    self.level = 1
    self.crate_amount = 2
    self.spawnpositions = np.arange(1,101, dtype=np.int64).reshape(10,10)
    
  def prepare_game(self):  #load everthing in when a new lvl is reached
    self.spawnpositions = np.arange(1,101, dtype=np.int64).reshape(10,10)  #make a new 2d array where nothing is 0
    imune = threading.Thread(target= self.make_snake_imune)
    imune.start()
    print(self.spawnpositions)
    for crate in crate_sprites:
      crate.kill()
    for i in range(self.fruit_amount):
      fruit = Fruit(self.spawnpositions)
      all_sprites.add(fruit)
      all_sprites_drawn.add(fruit)
      fruit_sprites.add(fruit)
    for i in range(self.crate_amount):
      crate = Crate(self.spawnpositions)
      all_sprites.add(crate)
      all_sprites_drawn.add(crate)
      crate_sprites.add(crate)

  def make_snake_imune(self): #make snake imune so that you dont die when a new lvl starts if a crate spawns on the snake
    self.snake.imune = True
    time.sleep(3)
    self.snake.imune = False
    

  def level_text(self): #display the lvl 
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("level " + str(self.level), True, black, None)
    textRect = text.get_rect()
    textRect.center = (440, 40)
    self.screen.blit(text, textRect)

  def run(self):  #run the game
    if self.playing: #can pause game
      self.screen.fill((255,0,0))
      self.playboard() #draw the playboard
      all_sprites.update() #update all the sprites
      self.check_if_hit_border() #check if snake hit border
      all_sprites_drawn.draw(SCREEN) #draw all the sprites
      self.draw_eyes()
      self.level_text()
      pygame.display.update()
      CLOCK.tick(self.FPS)
    if not (fruit_sprites): #check if fruit_sprites is empty
      self.level += 1
      self.fruit_amount += 2
      self.crate_amount += 1
      self.prepare_game()
    # print(CLOCK.get_fps())

  def add_blocks_to_snake(self):
    for block in self.snake.blocks:
      all_sprites.add(block)
      all_sprites_drawn.add(block)
  

  def playboard(self):
    make_playboard(self.screen) #draw the playboard

  def check_if_hit_border(self):  #check if the snake hits the border
    if self.snake.blocks[1].pos[0] < 0:
     self.snake.blocks[1].pos = (self.snake.blocks[1].pos[0] + 525, self.snake.blocks[1].pos[1])
    if self.snake.blocks[1].pos[0] > 500:
     self.snake.blocks[1].pos = (self.snake.blocks[1].pos[0] -525, self.snake.blocks[1].pos[1])
    if self.snake.blocks[1].pos[1] < 0:
     self.snake.blocks[1].pos = (self.snake.blocks[1].pos[0] , self.snake.blocks[1].pos[1] + 525)
    if self.snake.blocks[1].pos[1] > 500:
     self.snake.blocks[1].pos = (self.snake.blocks[1].pos[0] , self.snake.blocks[1].pos[1] - 525)

  def draw_eyes(self):  #draw the eyes of the snake 
    if self.snake.direction == [1,0]:
      pygame.draw.circle(self.screen,(255,255,255), (self.snake.blocks[1].pos[0] + 25, self.snake.blocks[1].pos[1] + 6),6 )
      pygame.draw.circle(self.screen,(255,255,255), (self.snake.blocks[1].pos[0] + 25, self.snake.blocks[1].pos[1] + 18),6 )
      pygame.draw.circle(self.screen,(0,0,0), (self.snake.blocks[1].pos[0] + 27, self.snake.blocks[1].pos[1] + 6),2 )
      pygame.draw.circle(self.screen,(0,0,0), (self.snake.blocks[1].pos[0] + 27, self.snake.blocks[1].pos[1] + 18),2 )
    if self.snake.direction == [-1,0]:
      pygame.draw.circle(self.screen,(255,255,255), (self.snake.blocks[1].pos[0] + 0, self.snake.blocks[1].pos[1] + 6),6 )
      pygame.draw.circle(self.screen,(255,255,255), (self.snake.blocks[1].pos[0] + 0, self.snake.blocks[1].pos[1] + 18),6 )
      pygame.draw.circle(self.screen,(0,0,0), (self.snake.blocks[1].pos[0] -2, self.snake.blocks[1].pos[1] + 6),2 )
      pygame.draw.circle(self.screen,(0,0,0), (self.snake.blocks[1].pos[0] + -2, self.snake.blocks[1].pos[1] + 18),2 )
    if self.snake.direction == [0,1]:
      pygame.draw.circle(self.screen,(255,255,255), (self.snake.blocks[1].pos[0] + 6, self.snake.blocks[1].pos[1]+25),6 )
      pygame.draw.circle(self.screen,(255,255,255), (self.snake.blocks[1].pos[0] + 18, self.snake.blocks[1].pos[1]+25),6 )
      pygame.draw.circle(self.screen,(0,0,0), (self.snake.blocks[1].pos[0] + 6, self.snake.blocks[1].pos[1] + 27),2 )
      pygame.draw.circle(self.screen,(0,0,0), (self.snake.blocks[1].pos[0] + 18, self.snake.blocks[1].pos[1] + 27),2 )
    if self.snake.direction == [0,-1]:
      pygame.draw.circle(self.screen,(255,255,255), (self.snake.blocks[1].pos[0] + 6, self.snake.blocks[1].pos[1] ),6 )
      pygame.draw.circle(self.screen,(255,255,255), (self.snake.blocks[1].pos[0] + 18, self.snake.blocks[1].pos[1] ),6 )
      pygame.draw.circle(self.screen,(0,0,0), (self.snake.blocks[1].pos[0] + 6, self.snake.blocks[1].pos[1] - 2),2 )
      pygame.draw.circle(self.screen,(0,0,0), (self.snake.blocks[1].pos[0] + 18, self.snake.blocks[1].pos[1] - 2),2 )
      

    
   
      
      
     
    
    