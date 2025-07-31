import sys
import os
import pygame
from asset_class import Image, Button, ScrollingBackground, Spaceship, Bullet, Enemy 
import random
from pygame import mixer

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  # PyInstaller uses this
    except Exception:
        base_path = os.path.abspath(".")  # Normal dev mode

    return os.path.join(base_path, relative_path)


def play_music():
    pygame.mixer.music.load(resource_path("asset/background.wav"))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
def show_text(text, score,x,y):
    score = font.render(text + str(score),True, (255,255,255) )
    screen.blit(score, (x, y))

def draw_menu():
     screen.fill((0,0,0))
     Background.draw_image(screen)
     Logo.draw_image(screen)
     Play.draw_image(screen)
     Exit.draw_image(screen)
     

def draw_difficuly_menu(screen):
     screen.fill((0,0,0))
     Background.draw_image(screen)
     Difficulty.draw_image(screen)
     Easy.draw_image(screen)
     Medium.draw_image(screen)
     Hard.draw_image(screen)

def difficulty_option(event):
   global enemy_per_frame, enemy_speed, difficulty_text
   if event.type == pygame.MOUSEBUTTONDOWN:
      if Easy.is_clicked(event):
         difficulty_text+="Easy"
         enemy_speed = 1
         enemy_per_frame = 2000
         return True
      
      if Medium.is_clicked(event):
         difficulty_text+="Medium"
         enemy_speed = 1
         enemy_per_frame = 500
         return True
      
      if Hard.is_clicked(event):
         difficulty_text+="HardCore"
         enemy_speed = 2
         enemy_per_frame = 1000
         return True
      return False
 

def infinte_scrolling(screen):
      screen.fill((0,0,0))
      Scrolling_background.update()
      Scrolling_background.draw_scrolling_image(screen)

def isenemycollide(enemy, player):
    offset = (enemy.rect.x - player.rect.x, enemy.rect.y - player.rect.y)
    if player.mask.overlap(enemy.mask, offset):
        return True
    return False

def play_game():
   global score
   global enemy_counter
   global difficulty_text
   enemy_counter+=1
   infinte_scrolling(screen)
   player.move(key, 800, 600)
   player.draw_image(screen)
   if enemy_counter > enemy_per_frame:
      etype = random.choice(enemy_type)
      enemy = Enemy(
       etype["img"],
       (random.randint(0, 736), -30),
       (64, 64),
       enemy_speed
      )
      All_enemies.append(enemy)
      enemy_counter = 0


   for Ene in All_enemies:
       Ene.move(800,600)
       Ene.draw_image(screen)
       if bullet.state == "Fire":
          if Ene.IsCollision(bullet.rect.x, bullet.rect.y):
             All_enemies.remove(Ene)
             Explosion_Sound.play()
             bullet.state = "Rest"
             bullet.set_coordinates(0, 0) 
             score+=1
   
       if isenemycollide(Ene, player):
           pygame.mixer_music.stop()
           Game_Over_Sound.play()
           game_over.draw_image(screen)
           show_text("Score: ",score, 350,400)
           show_text("Difficulty Selected: ",difficulty_text, 230, 500)
           difficulty_text = ""
           pygame.display.update()  
           pygame.time.delay(3000)
           All_enemies.clear() 
           play_music()
           return True



   if key[pygame.K_SPACE]:
      if bullet.state == "Rest":
         x, y = player.get_coordinates()
         bullet.set_coordinates(x+19, y)
         bullet.state = "Fire"
         Bullet_Sound.play()
    
   if bullet.state == "Fire":
            bullet.move()
            bullet.fire_bullet(screen)
    
   if bullet.out_of_screen():
            bullet.state = "Rest"
            bullet.set_coordinates(0, 0)
   
   show_text("Score: ", score,10,10)
   return False

pygame.init()


play_music()
game_state = "menu"

screen = pygame.display.set_mode((800,600))
Background = Image(resource_path("asset/background.png"))
icon = pygame.image.load(resource_path('asset/ufo.png'))
Logo = Image(resource_path('asset/Space Invader Logo.png'), (200,10))
Play = Button(resource_path('asset/Play Button.png'), (150,325))
Exit = Button(resource_path('asset/Exit Button.png'), (450,330), scale=(190,190))
Scrolling_background = ScrollingBackground(resource_path("asset/background.png"), scale=(800, 600), speed=0.1)
game_over = Image(resource_path('asset/Game Over.png'), (70, 100))
player = Spaceship(resource_path('asset/spaceship.png'), (375, 450), scale=(70,70))
bullet = Bullet(resource_path("asset/bullet.png"), (0,0), (32,32), speed=2, state="Rest")
Easy = Button(resource_path('asset/Easy.png'), (270,100), (250,250))
Medium = Button(resource_path('asset/Normal.png'), (270,225), (250,250))
Hard = Button(resource_path('asset/Hard.png'), (270,350), (250,250))
Difficulty = Image(resource_path('asset/Difficulty.png'), (200, -100), (400,400))
Explosion_Sound = mixer.Sound(resource_path('asset/explosion.wav'))
Bullet_Sound = mixer.Sound(resource_path('asset/laser.wav'))
Game_Over_Sound = mixer.Sound(resource_path('asset/Game Over.wav'))
font = pygame.font.Font(resource_path('asset/Pricedown.otf'), 32)
click_sound = mixer.Sound(resource_path('asset/Click.wav'))
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Invader")

score = 0
enemy_counter = 0
difficulty_text = ""
enemy_type = [
    {"img": resource_path("asset/Red Goblin.png")},
    {"img": resource_path("asset/Green Goblin.png")},
    {"img": resource_path("asset/Purple Goblin.png")}
]

enemy_per_frame = 1500
All_enemies = []
running = True
ignore_click = 0

while running:
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
        running = False
        
       if game_state == "menu":
          if Exit.is_clicked(event):
             click_sound.play()
             pygame.time.delay(200)
             running = False
     
          if Play.is_clicked(event):
              click_sound.play()
              game_state = "difficulty"
              ignore_click = 2 # skip next click events
      
       if game_state == "difficulty":
          # Step 1: Skip one frame of clicks
          if ignore_click > 0:
              ignore_click -= 1  # countdown the delay
              continue  # skip handling clicks for this loop

          # Step 2: Now allow difficulty buttons to work
          if difficulty_option(event):
              click_sound.play()  # Your button handler
              game_state = "play"

    
    if game_state == "menu":
       player.set_coordinates(375, 450)
       bullet.set_coordinates(32,32)
       game_over.set_coordinates(70, 100)
       score = 0
       draw_menu()

    if game_state == "difficulty":
        draw_difficuly_menu(screen)
        
        


    if game_state == "play":
       isover =  play_game()
       if isover:
           game_state = "Game Over"
      
    if game_state == "Game Over":
        game_state = "menu"

       
    pygame.display.update()