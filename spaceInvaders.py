import pygame as pg
import sys
import os

pg.init()

screenResolution = pg.display.Info()
width = screenResolution.current_w
height = screenResolution.current_h
screen = pg.display.set_mode((width, height), pg.FULLSCREEN)
print(width, height)
clock = pg.time.Clock()

shipSprite = pg.image.load("space invaders\ship.png")
alenSprite = pg.image.load("space invaders\invader.png")

moveRight = False
moveLeft = False
spacePressed = False
loop = 0
bulletOut = False

once = False

runOnce = False
X = 0
Y = 0

AmoveRight = True
AmoveLeft = False

checkRight = 1070
checkLeft = 0

class player:

    def __init__(self):
        self.health = 100
        x = 100
        self.posX = width/2
        self.posY = 1000

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
        Y -= 25
        pg.time.wait(10)

class alien:

    def __init__(self):
        self.y = 50
        self.x = 0
        self.xOffset = 0
        self.listAlens = []
        for a in range(15):
            self.x = 20 + self.xOffset + 75 * a
            self.listAlens.append([self.x, self.y]) #[self.x, self.y]            

# alen
    def blitAlens(self):
        for a in range(15):
            if self.listAlens[a] != "":
                screen.blit(alenSprite, (self.listAlens[a][0], self.listAlens[a][1]))
        self.listAlens[5] = ""

    def moveAlens(self):
        global AmoveRight
        global AmoveLeft
        global checkLeft
        global checkRight
        global once
        speed = 1
        if checkLeft < 0:
            print("THIS")
            AmoveRight = True
            AmoveLeft = False
            speed += speed / 2
        if checkRight > 12000:
            print("THAT")
            AmoveLeft = True
            AmoveRight = False
            once = True
            speed += speed / 2
        if AmoveRight == True:
            for a in range(15):  #fix this movement stuff
                if self.listAlens[a] != "":
                    self.listAlens[a][0] += speed
                    checkRight += speed
                    checkLeft += speed
        if AmoveLeft == True:
            for a in range(15):
                if self.listAlens[a] != "":
                    if once == True:
                        print(speed, "speed")
                        for b in range(15):
                            if self.listAlens[b] != "":
                                self.listAlens[b][1] += 10
                        once = False
                if self.listAlens[a] != "":
                    self.listAlens[a][0] -= speed
                    checkRight -= speed
                    checkLeft -= speed
            

ship = player()
aliens = alien()
running = True

while running:
    mouse = pg.mouse.get_pos()
    clock.tick(60)
    pg.Surface.fill(screen, (150, 50, 55))

    running = True
    ship.spriteBlit()

    aliens.moveAlens()
    aliens.blitAlens()

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
        print(coords)
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
    

    pg.display.update()





    # when bullet collides with bunker, draw rect (that is same color as background) over that part of the bunker.
    # only check for collision with bunker if bullet does not collide with the drawn rect
