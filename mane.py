from pygame import*
from random import randint
from time import time as timer
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w = 100, h = 100):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.player_speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, ( self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 1:
            self.rect.x -= self.player_speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.player_speed
    def fire(self):
        bullet = Bullet("pngtree-bullet-icon-in-cartoon-style-png-image_5097087__1_-removebg-preview (1).png", self.rect.centerx, self.rect.top, -15, 20 , 15)
        bullets.add(bullet)
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.player_speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.player_speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

score = 0
lost = 0
goal = 4
max_lost = 3
life = 3
num_fire = 0

game = True
finish = False
rel_time = False

font.init()
font2 = font.Font(None, 80)
font1 = font.Font(None, 30)
win = font2.render("YOU WIN!", True, (255, 255, 255))
lose = font2.render("YOU LOSE!", True, (255, 255, 255))

text_lost = font2.render("Пропущено:" + str(lost), 1, (180, 0, 0))

win_width = 700

win_height = 500

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("12121233-removebg-preview.png", randint(80, win_width - 80), -40, randint(1, 5))
    monsters.add(monster)

astroids = sprite.Group()
for i in range(1, 3):
    astroid = Enemy("2222222222-removebg-preview.png", randint(80, win_width - 80), -40, randint(1, 5))
    astroids.add(astroid)

bullets = sprite.Group()


window = display.set_mode((700, 500))

player = Player("123321-removebg-preview.png", 5, win_height - 80, 4)

display.set_caption("Шутер")
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
www3 = transform.scale(image.load("44444444.jpg"), (win_width, win_height))

mixer.init()
mixer.music.load("Ancient Mystery Waltz Allegro.mp3")
mixer.music.play()

clock = time.Clock()
FPS = 60

finish = False
game = True
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                player.fire()
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    player.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(www3, (0, 0))
        text_lose = font1.render("Пропущено: " + str(lost), 1, (0,0,0))
        player.reset()
        player.update()
        astroids.update()

        bullets.update()
        monsters.update()
        monsters.draw(window)

        astroids.draw((window))
        bullets.draw(window)
        player.reset()
        player.update()

        if sprite.groupcollide(monsters, bullets, True, True):
            score = score + 1
            monster = Enemy("12121233-removebg-preview.png", randint(80, win_width - 80), -40, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, True) or sprite.spritecollide(player, astroids, True):
            life = life - 1
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1,(150, 0, 0))
                window.blit(reload, (200, 450))
            else:
                num_fire = 0
                rel_time = False





        text_life = font1.render(("Житів:") + str(life), 1, life_color)
        window.blit(text_life, (10, 80))
    display.update()
    clock.tick(FPS)