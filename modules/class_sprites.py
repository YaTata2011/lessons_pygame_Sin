import pygame
from random import randint
import os
pygame.init()


def abs_path():
    path_object = os.path.abspath(__file__ + "/..")
    path_object = path_object.split("\\")
    del path_object[-1]
    path_object = "\\".join(path_object)
    return path_object 

work_directory = abs_path()
os.chdir(work_directory)
print(work_directory)



# створюємо віконце
win_width = 700
win_height = 500
pygame.display.set_caption("Shooter")
window = pygame.display.set_mode((win_width, win_height))

# нам потрібні такі картинки:
img_back = "images/galaxy.jpg"  # фон гри
img_hero = "images/rocket.png"  # герой
img_bullet = "images/bullet.png" # куля
img_enemy = "images/ufo.png"  # ворог

background = pygame.transform.scale(pygame.image.load(img_back), (win_width,win_height))
 
# фонова музика
pygame.mixer.init()
pygame.mixer.music.load('music/space.ogg')
pygame.mixer.music.play()
fire_sound = pygame.mixer.Sound('music/fire.ogg')

score = 0  # збито кораблів
goal = 10 # стільки кораблів потрібно збити для перемоги
lost = 0  # пропущено кораблів
max_lost = 3 # програли, якщо пропустили стільки




# клас-батько для інших спрайтів
class GameSprite(pygame.sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        pygame.sprite.Sprite.__init__(self)
 
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = pygame.transform.scale(
            pygame.image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    # метод, що малює героя у вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
# клас головного гравця
class Player(GameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 
    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
 
# клас спрайта-ворога
class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

# клас спрайта-кулі   
class Bullet(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()

bullets = pygame.sprite.Group()

 
# створюємо спрайти
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
monsters = pygame.sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(
        80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
 