import pygame
import sys
from random import randint

lost = 0

# клас-батько для інших спрайтів
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.speed = player_speed
        self.image = pygame.transform.scale(pygame.image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))


# клас головного гравця
class Player(GameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self, win_width):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

        if keys[pygame.K_x]:
            self.pause = True


        if keys[pygame.K_z]:
            self.pause = False




        
    
    def fire(self, bullets, screen):                            
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 25, 37.5, 35, screen)
        bullets.add(bullet)


#клас спрайта-ворога
class Enemy(GameSprite):
    def update(self, win_height, win_width):
        self.rect.y += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            global lost
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(0, win_width - 80)


#клас для куль
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()


# Клас гри
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen_width = 700
        self.screen_height = 600
        self.screen_size = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)

        self.background = pygame.transform.scale(pygame.image.load('galaxy.jpg'), self.screen_size)

        # створюємо об'єкт гравця
        self.player = Player('rocket.png', 300, 500, 50, 80, 7.5, self.screen)

        # створюємо групу спрайтів для ворогів
        self.enemies = pygame.sprite.Group()
        self.enemies2 = pygame.sprite.Group()
        self.enemies3 = pygame.sprite.Group()

        # створюємо групу спрайтів для куль
        self.bullets = pygame.sprite.Group()

        self.generate_enemies()
        self.generate_enemies2()
#        self.generate_enemies3()
        
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True
        self.finished = False
        self.pause = False

        self.hp_boss = False

        # створюємо властивості для підрахунку статистики 
        self.left = 100

        self.win = 0

        self.hp = 2

        # створюємо свій шрифт для написів
        self.statistic_font = pygame.font.Font(None, 35)
        self.resalt_font = pygame.font.Font(None, 85)

        self.game_run()


    # метод, який генерує ворогів та додає їх до групи спрайтів
    def generate_enemies(self):
        for i in range(2):
            enemy = Enemy("ufo.png", randint(0, self.screen_width - 80), -40, 80, 80, randint(1, 4), self.screen)
            self.enemies.add(enemy)


    def generate_enemies2(self):
        for i in range(2):
            enemy2 = Enemy("ufo1.png", randint(0, self.screen_width - 80), -40, 80, 80, randint(1, 4), self.screen)
            self.enemies2.add(enemy2)

#    def generate_enemies3(self):
#        for i in range(1):
#            boss = Enemy("boss.png", randint(0, self.screen_width - 80), -40, 70, 60, randint(1, 4), self.screen)
#            self.enemies.add(boss)



    # метод з ігровим циклом
    def game_run(self):
        pygame.mixer.music.load("background_music.mp3")
        pygame.mixer.music.play(-1)   
        while self.running:         
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Перевірка натискання кнопки клавіатури
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_SPACE:
                        self.player.fire(self.bullets, self.screen)

                    if event.key == pygame.K_x and self.pause == False:
                        self.pause = True

                    if event.key == pygame.K_z and self.pause == True:
                        self.pause = False
                        
                        
            if not self.finished:
                if self.pause == False:
                        
                    global lost
                    

                    self.screen.blit(self.background, (0, 0))

                    # малюємо та оновлюємо позицію гравця
                    self.player.update(self.screen_width) 
                    self.player.draw()  

                    # малюємо та оновлюємо позицію ворогів
                    self.enemies.update(self.screen_width, self.screen_height)
                    self.enemies.draw(self.screen)  

                    self.enemies2.update(self.screen_width, self.screen_height)
                    self.enemies2.draw(self.screen)
                    # малюємо та оновлюємо позицію куль
                    self.bullets.update()
                    self.bullets.draw(self.screen)

                    
                    # збиття ворогів 
                    collides = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
                    for c in collides:
                        self.left -= 1
                        enemy = Enemy("ufo.png", randint(0, self.screen_width - 80), -40, 80, 50, randint(1, 5), self.screen)
                        enemy2 = Enemy("ufo1.png", randint(0, self.screen_width - 80), -40, 80, 80, randint(1, 5), self.screen)
                        self.enemies2.add(enemy2)

                    collides2 = pygame.sprite.groupcollide(self.enemies2, self.bullets, True, True)
                    for v in collides2:
                        self.left -= 1
                        enemy = Enemy("ufo.png", randint(0, self.screen_width - 80), -40, 80, 50, randint(1, 5), self.screen)
                        enemy2 = Enemy("ufo1.png", randint(0, self.screen_width - 80), -40, 80, 80, randint(1, 5), self.screen)
                        self.enemies.add(enemy)

#                  collides3 = pygame.sprite.groupcollide(self.enemies3, self.bullets, False, True)
#                   for v in collides2:
#                         self.left -= 1
#                          boss = Enemy("boss.png", randint(0, self.screen_width - 80), -40, 80, 50, randint(1, 5), self.screen)
#                          self.enemies3.add(boss)                
                    if pygame.sprite.spritecollide(self.player, self.enemies, True):
                        self.hp -= 1
                        enemy2 = Enemy("ufo1.png", randint(0, self.screen_width - 80), -40, 80, 80, randint(1, 5), self.screen)
                        self.enemies2.add(enemy2)

                    if pygame.sprite.spritecollide(self.player, self.enemies2, True):
                        self.hp -= 1
                        enemy = Enemy("ufo.png", randint(0, self.screen_width - 80), -40, 80, 50, randint(1, 5), self.screen)
                        self.enemies.add(enemy)

                    if self.hp <= 0 or lost >= 2:
                        self.finished = True
                        lusetext = self.resalt_font.render("GAME OVER", True, (255, 255, 255))
                        self.screen.blit(lusetext, (170, 250))
                        self.win = 0
                    

                    if self.left <= 0:
                        self.finished = True
                        lusetext = self.resalt_font.render("YOU WIN", True, (255, 255, 255))
                        self.screen.blit(lusetext, (225, 250))
                        self.win += 1

                    if self.pause == True:
                        lusetext = self.resalt_font.render("Pause", True, (255, 255, 255))
                        self.screen.blit(lusetext, (225, 250))





                    # пишемо стаистику на екрані   
                    text_score = self.statistic_font.render("left: " + str(self.left), 1, (255, 255, 255))
                    self.screen.blit(text_score, (10, 20))

                    text_lost = self.statistic_font.render("missed: " + str(lost), 1, (255, 255, 255))
                    self.screen.blit(text_lost, (10, 50))

                    text_life = self.statistic_font.render("life: " + str(self.hp), 1, (255, 255, 255))
                    self.screen.blit(text_life, (10, 80))

                    text_win = self.statistic_font.render("win streak: " + str(self.win), 1, (255, 255, 255))
                    self.screen.blit(text_win, (10, 110))


                 
            else:
                self.finished = False
                lost = 0
                self.left = 100
                self.hp = 2

                for enemy in self.enemies:
                    enemy.kill()

                for enemy2 in self.enemies2:
                    enemy2.kill()

                for bullet in self.bullets:
                    bullet.kill()






                self.generate_enemies()
                self.generate_enemies2()

                pygame.time.delay(3000)
                

                
            self.clock.tick(self.fps)
            pygame.display.update()

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    Game()







