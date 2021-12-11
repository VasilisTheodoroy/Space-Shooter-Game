#Create your own shooter
from random import randint
from pygame import *
from time import sleep
from time import time as timer
import sys


font_regular = 'BigJohnPRO-Regular.otf'
font_bold = 'BigJohnPRO-Bold.otf'

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       sprite.Sprite.__init__(self)
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x 
       self.rect.y = player_y
    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 1815:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx - 12, self.rect.top, 25, 40, -20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 1050:
            self.rect.x = randint(5, window_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
#window height and width
window_height = 1920
window_width = 1080

#creating window, setting window parameters same as window height and width that we created before
window = display.set_mode((window_height,window_width))
#naming the window(the name shows on the top left corner)
display.set_caption('Shooter Game')
#creating the background
background = transform.scale(image.load('galaxy.jpg'),(window_height,window_width))

mixer.init()
mixer.music.load('music1.mp3')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')
bullets = sprite.Group()

ship = Player("rocket.png", 100,915, 100,100, 10)
monsters = sprite.Group()
lost = 0
score = 0
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
for i in range(5):
    monster = Enemy(img_enemy, randint(5, window_width - 80),0, 150,100, randint(3,10))
    monsters.add(monster)

font.init()
myfont = font.Font(font_regular, 50)

wl_font = font.Font(font_bold, 120)
win_txt = wl_font.render('You WON!', False, (0,200,0))
lose_txt = wl_font.render('You LOST!', False, (200,0,0))

lose_limit = 3
win_limit = 10

clock = time.Clock()
FPS = 60
num_fire = 0
num_show = 10
rel_time = False

mixer.init()
shoot = mixer.Sound('ship_fire_sound.wav')

#setting game to True
game = True
finish = False
#main game loop
while game:
    #a loop that if we close the game, it stops working
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire += 1
                    num_show -= 1
                    ship.fire()
                if num_fire >= 10 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    #rendering the background
    if not finish:
        window.blit(background,(0,0))
        score_txt = myfont.render('Score: '+ (str(score) + '/10'), True, (255,255,255))
        window.blit(score_txt,(30,30))
        lost_txt = myfont.render('Missed: ' + (str(lost) + '/3'), False, (255,255,255))
        window.blit(lost_txt, (window_width + 580, 30))
        #window.blit(win_txt, (630,500))
        #window.blit(lose_txt, (620,500))
        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        rel_show = myfont.render((str(num_show) + '/10'), True, (255,255,255))
        window.blit(rel_show, (50,1000))
        
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload_txt = myfont.render('Reloading...', True, (255,0,0))
                window.blit(reload_txt, (1680,1000))
            else:
                num_fire = 0
                num_show = 10
                rel_time = False

        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(5, window_width - 80),0, 150,100, randint(3,10))
            monsters.add(monster)
        if sprite.spritecollide(ship,monsters,True) or lost >= lose_limit:
            finish = True
            window.blit(lose_txt, (620,500))
        if score >= win_limit:
            finish = True
            window.blit(win_txt, (630,500))
    

    #making the display updating continiously as the game runs
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        num_show = 10
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(5):
            monster = Enemy(img_enemy, randint(5, window_width - 80),0, 150,100, randint(3,10))
            monsters.add(monster)
        monster = Enemy(img_enemy, randint(5, window_width - 80),0, 150,100, randint(3,10))
        monsters.add(monster)

    clock.tick(FPS)
    display.update()