import pygame
import random
import math

class Image:
    def __init__(self, imagepath, position=(0,0), scale = None): # scale = resize image # position = position it acc to x and y cod
        self.Image = pygame.image.load(imagepath).convert_alpha()

        if scale:
           self.Image = pygame.transform.scale(self.Image, scale)
        
        self.rect = self.Image.get_rect()
        self.rect.topleft = (position)
        self.mask = pygame.mask.from_surface(self.Image) # Masking creates (1) on visible button and (0) on transparent rect

    def draw_image(self, screen):
        screen.blit(self.Image,self.rect)
    
    def set_coordinates(self, x, y):
        self.rect.x = x
        self.rect.y = y



class Button(Image):
    def __init__(self, imagepath, position=(0, 0), scale=None):
        super().__init__(imagepath, position, scale)
        

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Convert mouse pos to local image pos
                x = event.pos[0] - self.rect.x
                y = event.pos[1] - self.rect.y
                if 0<=x < self.mask.get_size()[0] and 0<=y < self.mask.get_size()[1]:
                    return self.mask.get_at((x, y))  # True only if pixel is visible
            
        return False
    #def is_clicked(self, event):
    #    if event.type == pygame.MOUSEBUTTONDOWN:
    #        if self.rect.collidepoint(event.pos):
    #            return True
    #    return False

class ScrollingBackground(Image):
    def __init__(self, imagepath, speed=1, scale=None):
        super().__init__(imagepath, (0, 0), scale)
        self.speed = speed
        self.y1 = 0 # First image starting positon
        self.y2 = -self.rect.height # Second Image starting position eg: (-600)

    def update(self):
        self.y1 += self.speed  # Add the speed value that is set accordingly
        self.y2 += self.speed

        # If the image has moved entirely off screen, reset it above the other one
        if self.y1 >= self.rect.height: # Check if the image one is moved off the screen
            self.y1 = self.y2 - self.rect.height # Change it's value. For EG: if 600 >=600 then the y1 become -600
        if self.y2 >= self.rect.height: # do the same like above one but in opposite
            self.y2 = self.y1 - self.rect.height

    def draw_scrolling_image(self, screen):
        screen.blit(self.Image, (0, self.y1))
        screen.blit(self.Image, (0, self.y2))


class Spaceship(Image):
    def __init__(self, imagepath, position=(0, 0), scale=None, speed=1):
        super().__init__(imagepath, position, scale)
        self.speed = speed

    def move(self, key, width, height):

        if key[pygame.K_LEFT]:
            self.rect.x -=self.speed
        if key[pygame.K_RIGHT]:
            self.rect.x +=self.speed
        if key[pygame.K_UP]:
            self.rect.y -=self.speed
        if key[pygame.K_DOWN]:
            self.rect.y +=self.speed
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
    
    def get_coordinates(self):
        return self.rect.x , self.rect.y

        
class Bullet(Image):
    def __init__(self, imagepath, position=(0, 0), scale=None, speed=1, state=""):
        super().__init__(imagepath, position, scale)
        self.speed = speed
        self.state = state
    
    def fire_bullet(self, screen):
        self.state = "Fire"
        self.draw_image(screen)
        
    
    def out_of_screen(self):
        return self.rect.bottom < 0
    
    def move(self):
        self.rect.y-=self.speed
    
    
class Enemy(Image):
    def __init__(self, imagepath, position=(0, 0), scale=None,speed=1):
        super().__init__(imagepath, position, scale)
        self.speed = speed
    
    def move(self, width, height):
        self.rect.x += self.speed
        if self.rect.right >= width or self.rect.left <= 0:
           self.speed *= -1  # Reverse direction
           self.rect.y += 40   # Move enemy down


        if self.rect.y > height:
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, width - self.rect.width)
    
        self.rect.y = int(self.rect.y)
        


    def IsCollision(self, BulletX, BulletY):
        distance = math.sqrt(math.pow(self.rect.x - BulletX, 2) + math.pow(self.rect.y - BulletY, 2))
        if distance < 27:
            return True
        else:
            return False

