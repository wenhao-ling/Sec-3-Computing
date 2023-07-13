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

Clock = pygame.time.Clock() # idk what this is i think its fps thing

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
PUZZLE1_WIDTH = 60
PUZZLE1_HEIGHT = 30
PUZZLE2_X = 340
PUZZLE2_Y = 290
PUZZLE2_WIDTH = 80
PUZZLE2_HEIGHT = 10
PUZZLE3_X = 100
PUZZLE3_Y = 280
PUZZLE3_WIDTH = 40
PUZZLE3_HEIGHT = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
door = pygame.image.load("door.png")
door_rect = pygame.Rect(0,0,DOOR_WIDTH,DOOR_HEIGHT)
colour_door_rect = (255,255,255)
xbutton = pygame.image.load("xbutton.png")
puzzle1_rect = pygame.Rect(PUZZLE1_X,PUZZLE1_Y,PUZZLE1_WIDTH,PUZZLE1_HEIGHT)
# colour, correct order = 132
puzzle1_square1 = pygame.Rect(150,125,50,50)
puzzle1_square2 = pygame.Rect(225,125,50,50)
puzzle1_square3 = pygame.Rect(300,125,50,50)
puzzle1_square1_pressed = False
puzzle1_square2_pressed = False
puzzle1_square3_pressed = False
puzzle2_rect = pygame.Rect(PUZZLE2_X,PUZZLE2_Y,PUZZLE2_WIDTH,PUZZLE2_HEIGHT)
# width, correct order = 321 
puzzle2_square1 = pygame.Rect(150,125,30,50)
puzzle2_square2 = pygame.Rect(210,125,70,50)
puzzle2_square3 = pygame.Rect(300,125,50,50)
puzzle2_square1_pressed = False
puzzle2_square2_pressed = False
puzzle2_square3_pressed = False
puzzle3_rect = pygame.Rect(PUZZLE3_X,PUZZLE3_Y,PUZZLE3_WIDTH,PUZZLE3_HEIGHT)
# height, correct order = 231
puzzle3_square1 = pygame.Rect(150,125,50,50)
puzzle3_square2 = pygame.Rect(225,125,50,60)
puzzle3_square3 = pygame.Rect(300,125,50,40)
puzzle3_square1_pressed = False
puzzle3_square2_pressed = False
puzzle3_square3_pressed = False
haveKey = False
haveTouchedDoorOnce = False
puzzle1_complete = False
puzzle2_complete = False
puzzle3_complete = False
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
  pygame.draw.circle(screen,(0,0,100),(sprite.x, sprite.y), sprite.radius, sprite.width) # draw sprite
  
  pygame.draw.rect(screen,colour_door_rect,door_rect) # draw hitbox under door image
  screen.blit(pygame.transform.scale(door,(DOOR_WIDTH, DOOR_HEIGHT)), (0,0)) # draw door image

  pygame.draw.rect(screen,(0,255,0) if puzzle1_complete else (255,0,0),puzzle1_rect) # draw red puzzle 1, if complete then green
  pygame.draw.rect(screen,(0,255,0) if puzzle2_complete else (255,255,0),puzzle2_rect) # draw puzzle 2
  pygame.draw.rect(screen,(0,255,0) if puzzle3_complete else (0,0,255),puzzle3_rect) # draw puzzle 3
  
  pygame.display.update()


def isTouchingDoor():
  sprite_rect = pygame.Rect(sprite.hitbox) # assign sprite.hitbox a variable to be used in below statement
  if sprite_rect.colliderect(door_rect): # if colliding
    return True


def isTouchingPuzzle1():
  sprite_rect = pygame.Rect(sprite.hitbox)
  if sprite_rect.colliderect(puzzle1_rect): 
    return True


def isTouchingPuzzle2():
  sprite_rect = pygame.Rect(sprite.hitbox)
  if sprite_rect.colliderect(puzzle2_rect): 
    return True


def isTouchingPuzzle3():
  sprite_rect = pygame.Rect(sprite.hitbox)
  if sprite_rect.colliderect(puzzle3_rect): 
    return True


def drawText(text, font, colour, x, y): 
  img = font.render(text, True, colour)
  screen.blit(img, (x,y))
  pygame.display.flip()
  

def createPopup(): # popup parameters not customisable due to convenience
  pygame.draw.rect(screen,(0,0,0),(POPUP_X,POPUP_Y,POPUP_WIDTH,POPUP_HEIGHT)) # draw border behind
  pygame.draw.rect(screen,(230,230,230),(POPUP_X+2,POPUP_Y+2,POPUP_WIDTH-4,POPUP_HEIGHT-4)) # draw inner rect

  pygame.draw.rect(screen,(255,255,255),(POPUP_X+POPUP_WIDTH-XBUTTON_WIDTH,POPUP_Y,XBUTTON_WIDTH,XBUTTON_WIDTH)) # draw hitbox for xbutton
  screen.blit(pygame.transform.scale(xbutton, (XBUTTON_WIDTH,XBUTTON_WIDTH)),(POPUP_X+POPUP_WIDTH-XBUTTON_WIDTH,POPUP_Y))
  pygame.display.flip()
  

def isClickingX(): 
  mousePos = pygame.mouse.get_pos()
  xbutton_rect = pygame.Rect(POPUP_X+POPUP_WIDTH-XBUTTON_WIDTH, POPUP_Y, XBUTTON_WIDTH, XBUTTON_WIDTH)
  if pygame.mouse.get_pressed()[0] and xbutton_rect.collidepoint(mousePos):
    return True


# main loop
while running:
  colour_door_rect = (255,255,255)

  if inPopup: 
    if isClickingX():
      if isTouchingPuzzle1():
        sprite.y += 10
        refreshHitbox()
      if isTouchingPuzzle2() or isTouchingPuzzle3():
        sprite.y -= 10
        refreshHitbox()
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
      screen.fill((255,255,255))
      drawText("yippee you have ESCAPED THE ROOM", text_font, (0,0,0), 70, 100)
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
    inPopup = True
    createPopup()
    drawText("clockwise", text_font, (0,0,0), 200, 80)
    pygame.draw.rect(screen,(255,0,0),puzzle1_square1)
    pygame.draw.rect(screen,(0,0,255),puzzle1_square2)
    pygame.draw.rect(screen,(255,255,0),puzzle1_square3)
    pygame.display.flip() 
    # correct pressing order = square1, square3, square2
    if pygame.mouse.get_pressed()[0] and puzzle1_square1.collidepoint(pygame.mouse.get_pos()):
      puzzle1_square1_pressed = True
      puzzle1_square2_pressed = False
      puzzle1_square3_pressed = False

    if pygame.mouse.get_pressed()[0] and puzzle1_square3.collidepoint(pygame.mouse.get_pos()):
      if puzzle1_square1_pressed and not puzzle1_square2_pressed:
        puzzle1_square3_pressed = True
      else: 
        puzzle1_square1_pressed = False
        puzzle1_square2_pressed = False
        puzzle1_square3_pressed = False
        
    if pygame.mouse.get_pressed()[0] and puzzle1_square2.collidepoint(pygame.mouse.get_pos()):
      if puzzle1_square3_pressed and puzzle1_square1_pressed:
        # correct order
        puzzle1_complete = True
        redrawScreen()
      else: 
        puzzle1_square1_pressed = False
        puzzle1_square2_pressed = False
        puzzle1_square3_pressed = False


  if isTouchingPuzzle2():
    inPopup = True
    createPopup()
    pygame.draw.rect(screen,(0,0,0),puzzle2_square1)
    pygame.draw.rect(screen,(0,0,0),puzzle2_square2)
    pygame.draw.rect(screen,(0,0,0),puzzle2_square3)
    pygame.display.flip() 
    # correct pressing order = square3, square2, square1
    if pygame.mouse.get_pressed()[0] and puzzle2_square3.collidepoint(pygame.mouse.get_pos()):
      puzzle2_square3_pressed = True
      puzzle2_square2_pressed = False
      puzzle2_square1_pressed = False

    if pygame.mouse.get_pressed()[0] and puzzle2_square2.collidepoint(pygame.mouse.get_pos()):
      if puzzle2_square3_pressed and not puzzle2_square1_pressed:
        puzzle2_square2_pressed = True
      else: 
        puzzle2_square1_pressed = False
        puzzle2_square2_pressed = False
        puzzle2_square3_pressed = False
        
    if pygame.mouse.get_pressed()[0] and puzzle2_square1.collidepoint(pygame.mouse.get_pos()):
      if puzzle2_square3_pressed and puzzle2_square2_pressed:
        # correct order
        puzzle2_complete = True
        redrawScreen()
      else: 
        puzzle2_square1_pressed = False
        puzzle2_square2_pressed = False
        puzzle2_square3_pressed = False

  if isTouchingPuzzle3():
    inPopup = True
    createPopup()
    pygame.draw.rect(screen,(0,0,0),puzzle3_square1)
    pygame.draw.rect(screen,(0,0,0),puzzle3_square2)
    pygame.draw.rect(screen,(0,0,0),puzzle3_square3)
    pygame.display.flip() 
    # correct pressing order = square2, square3, square1
    if pygame.mouse.get_pressed()[0] and puzzle3_square2.collidepoint(pygame.mouse.get_pos()):
      puzzle3_square2_pressed = True
      puzzle3_square3_pressed = False
      puzzle3_square1_pressed = False

    if pygame.mouse.get_pressed()[0] and puzzle3_square3.collidepoint(pygame.mouse.get_pos()):
      if puzzle3_square2_pressed and not puzzle3_square1_pressed:
        puzzle3_square3_pressed = True
      else: 
        puzzle3_square1_pressed = False
        puzzle3_square2_pressed = False
        puzzle3_square3_pressed = False
        
    if pygame.mouse.get_pressed()[0] and puzzle3_square1.collidepoint(pygame.mouse.get_pos()):
      if puzzle3_square3_pressed and puzzle3_square2_pressed:
        # correct order
        puzzle3_complete = True
        redrawScreen()
      else: 
        puzzle3_square1_pressed = False
        puzzle3_square2_pressed = False
        puzzle3_square3_pressed = False

  
  if puzzle1_complete and puzzle2_complete and puzzle3_complete and not haveKey and inPopup: 
    if isTouchingPuzzle1():
      sprite.y += 10
      refreshHitbox()
    if isTouchingPuzzle2() or isTouchingPuzzle3():
      sprite.y -= 10
      refreshHitbox()
    time.sleep(1)
    haveKey = True
    inPopup = True
    createPopup()
    drawText("You have found the key", text_font, (0,0,0), 140, 100)
  
  
  if not inPopup:
    redrawScreen()
  
  Clock.tick(120) # fps

pygame.quit()
