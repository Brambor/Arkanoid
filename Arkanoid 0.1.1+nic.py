import pygame
import sys
import math
import random
import time
import platform

print(platform.system(), platform.release())

#inicializace
pygame.init() #1.vždy
screen = pygame.display.set_mode((400, 600)) #2.okno; x,y
pygame.display.set_caption("Arkanoid") #3.Název okna
pygame.display.set_icon(pygame.image.load("pic/ikona32.png")) #ikona na baru      výběr=16,32,40,48      Windows 7: ikona32     Windows XP: ikona32
pygame.display.set_mode
clock = pygame.time.Clock()
bg_color=(0,0,30) #barva (pozadí)

#nacteni palky a micku
palka_img = pygame.image.load("pic/palka.png").convert_alpha() #convert načítá se, pak rychlejší; alfa>průhlednost
palka = pygame.sprite.Sprite() #s tim budem hejbat
palka.image = palka_img
palka.rect = palka_img.get_rect() #pálce dá stejnej tvar, jako je velikost obrázku (ke kolizi)
palka.rect.center = (200,583) #vespodu (7 pixelů nad zemí), uprostřed
palka.speedX = 0 #rychlost

micky = pygame.sprite.Group()
mic = pygame.sprite.Sprite()
mic.image = pygame.image.load("pic/mic.png").convert_alpha()
mic.rect = mic.image.get_rect()
mic.rect.bottom = palka.rect.top
mic.rect.left = palka.rect.left
mic.speed = [-3.75, -3.307189138830738] #[0,-5]
mic.speed2 = [0, 0]
MAX_SPEED = 5
mic.sticky = True
micky.add(mic)

#text
text = pygame.sprite.Sprite()
text.num = []
for i in range(10):
    text.num.append(pygame.image.load("pic/"+str(i)+".png").convert_alpha())

#nahrani obrazku kosticek
bloky_img = []
for i in range(1, 5):
    bloky_img.append(pygame.image.load("pic/blok"+str(i)+".png").convert_alpha())

#generovani kosticek
bloky = pygame.sprite.Group()
for i in range(8):#8
    for j in range(6):#6
        x = 40 + i * 40
        y = 38 + j * 19 #+mezery
        blok = pygame.sprite.Sprite()
        blok.image = random.choice(bloky_img)
        blok.rect = blok.image.get_rect()
        blok.rect.topleft = (x, y)
        bloky.add(blok)

#životy
lives = pygame.sprite.Sprite()
lives.total = 2

lives.img = pygame.image.load("pic/lives.png").convert_alpha()
lives.rect = lives.img.get_rect()
lives.rect.center = (356, 594)
lives.rect2 = text.num[0].get_rect()
lives.rect2.top = lives.rect.top
lives.rect2.left = lives.rect.right

#skóre
score = pygame.sprite.Sprite()
score.total = 0
score.lis = ["0"]

score.img = pygame.image.load("pic/score.png").convert_alpha()
score.rect = score.img.get_rect()
score.rect.center = (20, 595)

#powerupy
powerups = pygame.sprite.Group() #COPIED
pu_micky_image = pygame.image.load("pic/pu_micky.png").convert_alpha() #COPIED

#hlavni smycka
while True:
    clock.tick(60) #4.omezuje na 60FPS (ne 61)
    for event in pygame.event.get(): #co uživatel zmáčkl od posledního zeptání
        if event.type == pygame.QUIT: #jestli zmáčku křížek/Alt+F4/ze správce úloh
            sys.exit() #nefunguje jen v IDLU
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        if event.type == pygame.KEYDOWN: #KEYDOWN = zmáčknutí nějaké klávesy
            if event.key == pygame.K_LEFT:
                palka.speedX -= 3
            if event.key == pygame.K_RIGHT:
                palka.speedX += 3
            if event.key == pygame.K_SPACE:
                for mic in micky:
                    mic.sticky = False
        if event.type == pygame.KEYUP: #KEYUP =odmáčknutí nějaké klávesy
            if event.key == pygame.K_LEFT:
                palka.speedX += 3
            if event.key == pygame.K_RIGHT:
                palka.speedX -= 3
                
    #pohyb
    palka.rect.left += palka.speedX
    if palka.rect.left < 0:
        palka.rect.left=0
    elif palka.rect.right > 400:
        palka.rect.right=400

    #pohyb vsech micku
    for mic in micky:
        if mic.sticky:
            mic.rect.bottom = palka.rect.top #kvůli dalším životům
            mic.rect.left = palka.rect.left
        else:
            mic.rect.x += int(mic.speed[0]) + int(mic.speed2[0])
            mic.speed2[0] -= int(mic.speed2[0])
            mic.speed2[0] += mic.speed[0] - int(mic.speed[0])

            mic.rect.y += int(mic.speed[1]) + int(mic.speed2[1])
            mic.speed2[1] -= int(mic.speed2[1])
            mic.speed2[1] += mic.speed[1] - int(mic.speed[1])

        #odrazy micku od sten a stropu
        if mic.rect.top < 0:
            mic.rect.top = 0
            mic.speed[1] = -mic.speed[1]
        if mic.rect.right > 400:
            mic.rect.right = 400
            mic.speed[0] = -mic.speed[0]
        elif mic.rect.left < 0:
            mic.rect.left = 0
            mic.speed[0] = -mic.speed[0]
            
        #odraz od palky
        if pygame.sprite.collide_rect (mic, palka):
            mic.rect.bottom = palka.rect.top + 1 #upravit
            palka_pulka = palka.rect.width / 2
            ratio = (mic.rect.centerx - palka.rect.centerx) / palka_pulka
            mic.speed[0] = ratio * MAX_SPEED
            mic.speed [1] = -math.sqrt (max(1, MAX_SPEED ** 2 - mic.speed[0] ** 2)) #pořád se dostává přes 5

        #odraz od kosticek(bloků)
        odrazeno = False
        for blok in pygame.sprite.spritecollide(mic, bloky, 1):
            score.total += 1
            if not odrazeno: #Neni to celý špatně?
                if (mic.rect.centerx > blok.rect.centerx) and (mic.rect.centery > blok.rect.centery): #1.
                    if (mic.rect.centerx - blok.rect.right) < (mic.rect.centery - blok.rect.bottom): #A3 B3
                        mic.speed[1] = -mic.speed[1]
                    elif (mic.rect.centerx - blok.rect.right) > (mic.rect.centery - blok.rect.bottom):
                        mic.speed[0] = -mic.speed[0]
                    else:
                        mic.speed[0] = -mic.speed[0]
                        mic.speed[1] = -mic.speed[1]
                elif (mic.rect.centerx > blok.rect.centerx) and (mic.rect.centery < blok.rect.centery): #2.
                    if (mic.rect.centerx - blok.rect.right) < -(mic.rect.centery - blok.rect.top): #C3 B1
                        mic.speed[1] = -mic.speed[1]
                    elif (mic.rect.centerx - blok.rect.right) > -(mic.rect.centery - blok.rect.top):
                        mic.speed[0] = -mic.speed[0]
                    else:
                        mic.speed[0] = -mic.speed[0]
                        mic.speed[1] = -mic.speed[1]
                elif (mic.rect.centerx < blok.rect.centerx) and (mic.rect.centery < blok.rect.centery): #3 NOT
                    if -(mic.rect.centerx - blok.rect.left) < -(mic.rect.centery - blok.rect.top): #C1 D1
                        mic.speed[1] = -mic.speed[1]
                    elif -(mic.rect.centerx - blok.rect.left) > -(mic.rect.centery - blok.rect.top): #C1 D1
                        mic.speed[1] = -mic.speed[1]
                    else:
                        mic.speed[0] = -mic.speed[0]
                        mic.speed[1] = -mic.speed[1]
                elif (mic.rect.centerx < blok.rect.centerx) and (mic.rect.centery > blok.rect.centery): #4. NOT
                    if -(mic.rect.centerx - blok.rect.left) < (mic.rect.centery - blok.rect.bottom): #A1 D3
                        mic.speed[1] = -mic.speed[1]
                    elif -(mic.rect.centerx - blok.rect.left) > (mic.rect.centery - blok.rect.bottom):
                        mic.speed[0] = -mic.speed[0]
                    else:
                        mic.speed[0] = -mic.speed[0]
                        mic.speed[1] = -mic.speed[1]
                    #mic.speed[0] = -mic.speed[0]
                    #mic.speed[1] = -mic.speed[1]
                odrazeno=True
            # powerupy
            if random.randint(1,36) == 1:
                powerup = pygame.sprite.Sprite() #COPIED
                powerup.image = pu_micky_image #COPIED
                powerup.rect = powerup.image.get_rect() #COPIED
                powerup.rect.center = blok.rect.center #COPIED
                powerups.add(powerup) #COPIED



        #Prohra
        if mic.rect.bottom > 588:
            micky.remove(mic)
            if micky.sprites() == []:
                lives.total -= 1 # odebrat mic, ne ubrat život
                mic = pygame.sprite.Sprite()
                mic.image = mic_img
                mic.rect = mic_img.get_rect()
                mic.rect.bottom = palka.rect.top
                mic.rect.left = palka.rect.left
                mic.speed = [0.0, 5.0]
                mic.speed2 = [0, 0]
                mic.sticky = True
                micky.add(mic)
                if lives.total < 1:
                    GO_img = pygame.image.load("pic/Game Over.png").convert_alpha()
                    GO = pygame.sprite.Sprite()
                    GO.image = GO_img
                    GO.rect = GO_img.get_rect()
                    GO.rect.center = (200,300)
                    screen.blit(GO.image, GO.rect)
                    pygame.display.update()
                    time.sleep(2)
                    sys.exit()

    #Vyhra
    if bloky.sprites() == []: # Tady je problém
        V_img = pygame.image.load("pic/Victory.png").convert_alpha()
        V = pygame.sprite.Sprite()
        V.image = V_img
        V.rect = V_img.get_rect()
        V.rect.center = (200,300)
        screen.blit(V.image, V.rect)
        pygame.display.update()
        time.sleep(2)
        sys.exit()

    # powerupy
    for powerup in powerups:
        powerup.rect.centery += 5
    for powerup in pygame.sprite.spritecollide(palka, powerups, 1):
        mic = pygame.sprite.Sprite()
        mic.image = mic_img
        mic.rect = mic_img.get_rect()
        mic.rect.bottom = palka.rect.top
        mic.rect.left = palka.rect.left
        mic.speed = [0.0, 5.0]
        mic.speed2 = [0, 0]
        mic.sticky = True
        micky.add(mic)

    score.Nrect = []

    score.lis = list(str(score.total))
    for i in range(len(score.lis)):
        score.Nrect.append((40 + 8 * i, 588, 8, 12))
        

    #kresleni
    screen.fill(bg_color) #5.vyplní okno barvou
    screen.blit(palka.image, palka.rect)#zobrazí pálku na souřadnice
    powerups.draw(screen)
    micky.draw(screen)
    bloky.draw(screen) #vykresli bloky

    #vypisování skóre
    screen.fill((0, 0, 0), (0, 588, 400, 12)) #(left, top, width, height)
    screen.blit(score.img, score.rect)
    for i in range(len(score.lis)):
        screen.blit(text.num[int(score.lis[i])], score.Nrect[i])
    
    #a zivotu
    screen.blit(lives.img, lives.rect)
    screen.blit(text.num[lives.total], lives.rect2)

    pygame.display.update() #6.zobrazí, co je uloženo
