import pygame
from shots import Shot

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1000

class Player():

    def __init__(self, position, img):
        self.position = position
        self.img = img
        self.rect = pygame.Rect(position[0]+8, position[1]+5, img.get_width()-16, img.get_height()-10)
        self.grau = 0
        self.passo = 1
        self.vel = 7
        self.life = 5
        self.heartText = pygame.font.SysFont('arial', 30).render("Life: ", True, (0, 0, 0))
        self.heartImage = pygame.image.load('sprites_player/heart.png')
        self.shots = []
        self.ammo = 10
        self.ammoImage = pygame.image.load('sprites_player/ammo_amount.png')
        self.ammoText = pygame.font.SysFont('arial', 21).render("Ammo:", True, (0, 0, 0))
        self.canSpawnBullets = True
        self.score = 0
        self.scoreText = pygame.font.SysFont('arial', 30).render("Score: " + str(self.score), True, (0, 0, 0))
  
    def setPosition(self, position):
        self.position = position

    def setImage(self, image):
        self.img = image

    def setRect(self, rect):
        self.rect = rect

    def animatePlayerSprite(self):
        if self.grau >= 360:
            self.grau = 0
        if self.grau < 0:
            self.grau = 360 + self.grau

        if self.passo > 3:
            self.passo = 1
            
        image = pygame.image.load('sprites_player/sprite' + str(self.passo) + '_player_' + str(self.grau) + '.png')      
        self.setImage(image)

    def moveUp(self):
        if self.position[1] > 0:
            self.setPosition((self.position[0], self.position[1]-self.vel))
            self.rect.y -= self.vel
        
    def moveDown(self):
        if self.position[1] < SCREEN_HEIGHT - self.img.get_height():
            self.setPosition((self.position[0], self.position[1]+self.vel))
            self.rect.y += self.vel

    def moveRight(self):
        if self.position[0] < SCREEN_WIDTH - self.img.get_width():
            self.setPosition((self.position[0]+self.vel, self.position[1]))
            self.rect.x += self.vel

    def moveLeft(self):
        if self.position[0] > 0:
            self.setPosition((self.position[0]-self.vel, self.position[1]))
            self.rect.x -= self.vel

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def damagePlayer(self, amount):
        self.life -= amount

    def healPlayer(self, amount):
        if self.life < 5:
            self.life += amount
        else:
            self.addScore(1000)

    def isPlayerDead(self):
        return self.life <= 0

    def showLife(self, screen):
        screen.blit(self.heartText, (7, 7))
        for i in range(1, self.life+1):
            screen.blit(self.heartImage, (20 + 40*i, 10))

    def shoot(self, game_map):
        if self.ammo > 0:
            self.ammo -= 1
            if self.grau == 0:
                self.shots.append(Shot((self.position[0]+40, self.position[1]), 'y', -1))
            elif self.grau == 180:
                self.shots.append(Shot((self.position[0]+20, self.position[1]+40), 'y',  1)) 
            elif self.grau == 90:
                self.shots.append(Shot((self.position[0]+40, self.position[1]+40), 'x',  1))
            else:
                self.shots.append(Shot((self.position[0], self.position[1]+20), 'x', -1))
            if self.ammo == 0 and self.canSpawnBullets:
                game_map.spawnBullets(4)
                self.canSpawnBullets = False

    def showAmmoAmount(self, screen):
        screen.blit(self.ammoText, (7, 50))
        for i in range(self.ammo):
            screen.blit(self.ammoImage, (60 + (20*i), 50))

    def addAmmo(self, amount):
        self.ammo += amount

    def addScore(self, amount):
        self.score += amount
        self.scoreText = pygame.font.SysFont('arial', 30).render("Score: " + str(self.score), True, (0, 0, 0))

    def showScore(self, screen):
        screen.blit(self.scoreText, (850 , 7))
