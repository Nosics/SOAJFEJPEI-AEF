import pygame as pg
import sys
import os
import random

pg.init()

screenResolution = pg.display.Info()
width = screenResolution.current_w
height = screenResolution.current_h
screen = pg.display.set_mode((width, height), pg.FULLSCREEN)
print(width, height)
clock = pg.time.Clock()
pg.font.init()
font = pg.font.Font("space invaders\slkscr.ttf", 32)

shipSprite = pg.image.load("space invaders\ship.png")
alenSprite = pg.image.load("space invaders\invader.png")

moveRight = False
moveLeft = False
spacePressed = False
loop = 0
bulletOut = False

once = False

speed = 2

runOnce = False
runOnce2 = False
X = 0
Y = 0

AmoveRight = True
AmoveLeft = False

checkRight = 1070
checkLeft = 0


class player:

    def __init__(self):
        self.health = 100
        self.posX = width/2
        self.posY = 1000
        self.bulletPos = 0, 0, 0, 0


# movement
    def spriteBlit(self):
        screen.blit(shipSprite, (self.posX, self.posY))

    def moveLeft(self):
        self.posX -= 10
        print(self.posX)

    def moveRight(self):
        self.posX += 10
        print(self.posX)

# bullet
    def initBullet(self):
        bulletPosX = self.posX
        bulletPosY = 1000
        return bulletPosX, bulletPosY

    def blitBullet(self, thisX, thisY):
        global runOnce
        global X, Y
        if runOnce == False:
            X = thisX
            Y = thisY
            runOnce = True
        pg.draw.rect(screen, (255, 255, 255), (X + 40.5, Y - 20, 5, 20))
        self.bulletPos = (X + 40.5, Y - 20, 5, 20)
        Y -= 25

class alien:

    def __init__(self):
        self.y = 50
        self.x = 0
        self.xOffset = 0
        self.listAlens = []
        self.alienBullets = []
        for a in range(15):
            self.x = 20 + self.xOffset + 75 * a
            self.listAlens.append([self.x, self.y]) #[self.x, self.y]            

# alen
    def blitAlens(self):
        for a in range(15):
            if self.listAlens[a] != "":
                screen.blit(alenSprite, (self.listAlens[a][0], self.listAlens[a][1]))
        #self.listAlens[5] = ""  <---- how to remove an alien

    def moveAlens(self):
        global AmoveRight
        global AmoveLeft
        global checkLeft
        global checkRight
        global once
        global speed
        if checkLeft < 0:
            print("THIS")
            AmoveRight = True
            AmoveLeft = False
            speed += 0.5
        if checkRight > 1800:
            print("THAT")
            AmoveLeft = True
            AmoveRight = False
            once = True
        if AmoveRight == True:
            for a in range(15):
                if self.listAlens[a] != "":
                    self.listAlens[a][0] += speed
            checkRight += speed
            checkLeft += speed
        print(checkRight, checkLeft)
        if AmoveLeft == True:
            for a in range(15):
                if self.listAlens[a] != "":
                    if once == True:
                        for b in range(15):
                            if self.listAlens[b] != "":
                                self.listAlens[b][1] += 30
                        once = False
                if self.listAlens[a] != "":
                    self.listAlens[a][0] -= speed
            checkRight -= speed
            checkLeft -= speed

    def shootBullet(self):
        for a in range(15):
            if random.randint(1, 8) == 1:
                self.alienBullets.append(self.listAlens[a])

        for i in range(len(self.alienBullets) - 1): # HERE
            x = self.alienBullets[i][0]
            y = self.alienBullets[i][1]
            pg.draw.rect(screen, (255, 155, 255), (x + 25, y + 40, 5, 20))

        pg.time.wait(10)


ship = player()
aliens = alien()


def collide():
    for a in range(15):
        if aliens.listAlens[a] != "":
            rect = pg.Rect(aliens.listAlens[a][0], aliens.listAlens[a][1], 55, 40)
            bulletPos = pg.Rect(ship.bulletPos)
            if pg.Rect.colliderect(bulletPos, rect):
                aliens.listAlens[a] = ""
                break

running = True

while running:
    mouse = pg.mouse.get_pos()
    clock.tick(60)
    pg.Surface.fill(screen, (150, 50, 55))

    running = True
    ship.spriteBlit()

    aliens.moveAlens()
    aliens.blitAlens()
    aliens.shootBullet()
    collide()

    for a in range(15): # CHECK FOR WIN!
        if aliens.listAlens[a] == "":
            win = True
        else:
            win = False
            break

    if moveRight:
        ship.moveRight()
    if moveLeft:
        ship.moveLeft()
    if spacePressed and bulletOut == False:
        print("space pressed")
        coords = ship.initBullet()
        loop = 1000
        bulletOut = True
        X = coords[0]
        Y = coords[1]


    if loop > 0:
        loop -= 25
        ship.blitBullet(X, Y)
    else:
        bulletOut = False
        

    for event in pg.event.get():
        if event.type == pg.QUIT: #quit game via X button
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE: #quit via esc key
                pg.quit()
                sys.exit()
            if event.key == pg.K_d:
                moveRight = True
            if event.key == pg.K_a:
                moveLeft = True
            if event.key == pg.K_SPACE:
                spacePressed = True
        else:
            moveRight = False
            moveLeft = False
            spacePressed = False
    
    if win == True:
        screen.blit(font.render("YOU WIN BABYYYY", True, (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))), (width/2 - 1000 + random.randint(1, 2005), height/2 - 400 + random.randint(1, 815)))
        screen.blit(font.render("YOU WIN BABYYYY", True, (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))), (width/2 - 1000 + random.randint(1, 2005), height/2 - 400 + random.randint(1, 815)))
        screen.blit(font.render("YOU WIN BABYYYY", True, (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))), (width/2 - 1000 + random.randint(1, 2005), height/2 - 400 + random.randint(1, 815)))
        screen.blit(font.render("YOU WIN BABYYYY", True, (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))), (width/2 - 1000 + random.randint(1, 2005), height/2 - 400 + random.randint(1, 815)))
        screen.blit(font.render("YOU WIN BABYYYY", True, (255, 255, 255)), (width/2 - 60, height/2 - 40))

    pg.display.update()

    # when bullet collides with bunker, draw rect (that is same color as background) over that part of the bunker.
    # only check for collision with bunker if bullet does not collide with the drawn rect
