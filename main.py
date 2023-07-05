import pygame
from pygame.locals import QUIT
import time

pygame.init()

class player(object):
  def __init__(self, x, y, radius, width):
    self.x = x
    self.y = y
    self.radius = radius
    self.width = width
    self.velocity = 2
    self.hitbox = (self.x, self.y, radius*2, radius*2)

sprite = player(230, 130, 20, 20) # width is the perimeter thickness
# ^ is setting the name for player class to "sprite" 

Clock = pygame.time.Clock() # idk what this is ashton helped me do it (fps thing)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 300
DOOR_WIDTH = 40
DOOR_HEIGHT = 60
XBUTTON_WIDTH = 25

POPUP_X = 50
POPUP_Y = 50
POPUP_WIDTH = 400
POPUP_HEIGHT = 200

PUZZLE1_X = 300
PUZZLE1_Y = 0
PUZZLE1_WIDTH = 50
PUZZLE1_HEIGHT = 10
PUZZLE2_X = 300
PUZZLE2_Y = 290
PUZZLE2_WIDTH = 50
PUZZLE2_HEIGHT = 10
leftClick, scrollClick, rightClick = pygame.mouse.get_pressed()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
door = pygame.image.load("door.png")
door_rect = pygame.Rect(0,0,DOOR_WIDTH,DOOR_HEIGHT)
colour_door_rect = (255,255,255)
xbutton = pygame.image.load("xbutton.png")
puzzle1_rect = pygame.Rect(PUZZLE1_X,PUZZLE1_Y,PUZZLE1_WIDTH,PUZZLE1_HEIGHT)
# puzzle2_rect = pyga
haveKey = False
haveTouchedDoorOnce = False
puzzle1_complete = False
puzzle2_complete = False
inPopup = False

running = True

logo = pygame.image.load("logo.png")
pygame.display.set_icon(logo)
pygame.display.set_caption('Escape the room!')
text_font = pygame.font.SysFont("Arial",20) # set font for drawText func


def refreshHitbox(): # refresh hitbox, need the "-sprite.radius" bc sprite.x and y is in the middle of circle
  sprite.hitbox = (sprite.x - sprite.radius, sprite.y - sprite.radius, sprite.radius*2, sprite.radius*2)

  
def redrawScreen(): 
  screen.fill((255,255,255))
  
  refreshHitbox() # refresh hitbox, need the "-sprite.radius" bc sprite.x and y is in the middle of circle
  pygame.draw.rect(screen,(255,255,255),sprite.hitbox) # draw hitbox under sprite
  pygame.draw.circle(screen,(0,0,255),(sprite.x, sprite.y), sprite.radius, sprite.width) # draw sprite
  
  pygame.draw.rect(screen,colour_door_rect,door_rect) # draw hitbox under door image
  screen.blit(pygame.transform.scale(door,(DOOR_WIDTH, DOOR_HEIGHT)), (0,0)) # draw door image

  pygame.draw.rect(screen,(0,255,0) if puzzle1_complete else (255,0,0),puzzle1_rect) # draw red puzzle 1, if complete then green
  
  
  pygame.display.update()


def isTouchingDoor():
  sprite_rect = pygame.Rect(sprite.hitbox) # assign sprite.hitbox a variable to be used in below statement
  if sprite_rect.colliderect(door_rect): # if colliding
    return True


def isTouchingPuzzle1():
  sprite_rect = pygame.Rect(sprite.hitbox)
  if sprite_rect.colliderect(puzzle1_rect): 
    return True


def drawText(text, font, colour, x, y): 
  img = font.render(text, True, colour)
  screen.blit(img, (x,y))
  pygame.display.flip()
  

def createPopup():
  pygame.draw.rect(screen,(0,0,0),(POPUP_X,POPUP_Y,POPUP_WIDTH,POPUP_HEIGHT)) # draw border behind
  pygame.draw.rect(screen,(230,230,230),(POPUP_X+2,POPUP_Y+2,POPUP_WIDTH-4,POPUP_HEIGHT-4)) # draw inner rect

  pygame.draw.rect(screen,(255,255,255),(POPUP_X+POPUP_WIDTH-XBUTTON_WIDTH,POPUP_Y,XBUTTON_WIDTH,XBUTTON_WIDTH)) # draw hitbox for xbutton
  screen.blit(pygame.transform.scale(xbutton, (XBUTTON_WIDTH,XBUTTON_WIDTH)),(POPUP_X+POPUP_WIDTH-XBUTTON_WIDTH,POPUP_Y))
  pygame.display.flip()
  

def isClickingX(): # input same parameters as createPopup function
  mousePos = pygame.mouse.get_pos()
  xbutton_rect = pygame.Rect(POPUP_X+POPUP_WIDTH-XBUTTON_WIDTH, POPUP_Y, XBUTTON_WIDTH, XBUTTON_WIDTH)
  if pygame.mouse.get_pressed()[0] and xbutton_rect.collidepoint(mousePos):
    return True


# main loop
while running:
  colour_door_rect = (255,255,255)

  if inPopup: 
    if isClickingX():
      inPopup = False # exits popup
  
  for event in pygame.event.get():
    if event.type == QUIT:
      running = False
  
  key = pygame.key.get_pressed()
  if not inPopup: 
    if key[pygame.K_a] and sprite.x > (0 + sprite.radius) and not isTouchingDoor(): # if key A pressed
      sprite.x -= sprite.velocity
    if key[pygame.K_d] and sprite.x < (SCREEN_WIDTH - sprite.radius):
      sprite.x += sprite.velocity
    if key[pygame.K_w] and sprite.y > (0 + sprite.radius) and not isTouchingDoor():
      sprite.y -= sprite.velocity
    if key[pygame.K_s] and sprite.y < (SCREEN_HEIGHT - sprite.radius):
      sprite.y += sprite.velocity
  
    if key[pygame.K_e]: # test
      inPopup = True
      createPopup()
      drawText("test", text_font, (0,0,0), 230, 100)

  if isTouchingDoor(): 
    if haveKey:
      createPopup()
      drawText("yippee you have completed the game", text_font, (0,0,0), 100, 100)
      time.sleep(3)
      running = False
      break
    else: 
      colour_door_rect = (255,0,0)
      
    if not haveTouchedDoorOnce:
      inPopup = True
      createPopup()
      drawText("you don't have a key", text_font, (0,0,0), 140, 100)
      haveTouchedDoorOnce = True

  if isTouchingPuzzle1():
    sprite.y += 10
    refreshHitbox()
    inPopup = True
    createPopup()
    
  
  if not inPopup:
    redrawScreen()
  
  Clock.tick(120) # fps

pygame.quit()