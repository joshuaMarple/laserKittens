import pygame, random, sys
from pygame.locals import *
import globalDefs
from kitty import *
from bear import *
from music import *
from corgi import *
def startGame():
    pygame.init()
    mainClock = pygame.time.Clock()

    windowSurface = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    # windowSurface = pygame.display.set_mode((1000,700))
    globalDefs.WINDOWWIDTH = pygame.display.Info().current_w
    globalDefs.WINDOWHEIGHT = pygame.display.Info().current_h
    planet = pygame.image.load('./res/okayplanet.png').convert_alpha()
    background = pygame.transform.scale(pygame.image.load('./res/space.png').convert_alpha(), (globalDefs.WINDOWWIDTH, globalDefs.WINDOWHEIGHT))
    globalDefs.background = pygame.transform.scale(background, (globalDefs.WINDOWWIDTH, globalDefs.WINDOWHEIGHT))
    pygame.display.set_caption('Kitten Lasers')
    pygame.mouse.set_visible(False)
    windowSurface.fill(globalDefs.BACKGROUNDCOLOR)
    windowSurface.blit(globalDefs.background, (0,0))
    font = pygame.font.Font("./res/manteka.ttf", 30)
    # muse = music()
    # muse.levelSong()

    def terminate():
        pygame.quit()
        sys.exit()

    def waitKey():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        terminate()
                    if event.key == K_RETURN:
                        return

    def drawText(text, font, surface, x, y):
        textobj = font.render(text, 1, globalDefs.TEXTCOLOR)
        textrect = textobj.get_rect()
        textrect.topleft = (x,y)
        surface.blit(textobj, textrect)

    def clearScreen():
        windowSurface.fill(globalDefs.BACKGROUNDCOLOR)
        windowSurface.blit(globalDefs.background, (0,0))

    def restart():
        windowSurface.fill(globalDefs.BACKGROUNDCOLOR)
        windowSurface.blit(globalDefs.background, (0,0))
        drawText('Press Enter for a new game', font, windowSurface, (globalDefs.WINDOWWIDTH /8), (globalDefs.WINDOWHEIGHT / 3))
        drawText('Maybe you won\'t suck so hard this time', font, windowSurface, (globalDefs.WINDOWWIDTH /8), (globalDefs.WINDOWHEIGHT / 3) + 50)
        pygame.display.update()
        waitKey()
        for i in globalDefs.planets[:]:
            globalDefs.planets.remove(i)
        globalDefs.EarthHealth = 100
        planetAddCounter = 5
        kitCharge = 0
        globalDefs.score = 0

    def earthDead():
        clearScreen()
        drawText('EARTH IS DESTROYED!', font, windowSurface, (globalDefs.WINDOWWIDTH /8), (globalDefs.WINDOWHEIGHT / 3))
        drawText('YOU HAVE FAILED US, LASERKITTEN.', font, windowSurface, (globalDefs.WINDOWWIDTH /8), (globalDefs.WINDOWHEIGHT / 3) + 50)
        pygame.display.update()
        waitKey()
        restart()

    def kitDead():
        kit.health = 100
        clearScreen()
        drawText('LASERKITTEN IS DEAD', font, windowSurface, (globalDefs.WINDOWWIDTH /8), (globalDefs.WINDOWHEIGHT / 3))
        drawText('GOD HELP US ALL', font, windowSurface, (globalDefs.WINDOWWIDTH /8), (globalDefs.WINDOWHEIGHT / 3) + 50)
        pygame.display.update()
        waitKey()
        restart()

    def genPlanets(planetList):
        randomPlanet = random.random()
        if randomPlanet >= (.98 - ((globalDefs.score % 100)/1000.)):
            planetSize = random.randint(20, 200)+globalDefs.score/100
            newPlanet = {'size':planetSize,
                        'rect': pygame.Rect(globalDefs.WINDOWWIDTH - planetSize
                                             , random.randint(0, globalDefs.WINDOWHEIGHT-planetSize+globalDefs.score/10), planetSize, planetSize),
                         'speed': random.randint(globalDefs.planetMoveMin, globalDefs.planetMoveMax+globalDefs.score/100),
                         'surface':pygame.transform.scale(planet, (planetSize, planetSize)), }

            planetList.append(newPlanet)
        return planetList



    def planetChecker():
        for p in globalDefs.planets:
            p['rect'].move_ip(-p['speed'], random.randint(-5,5))

        for p in globalDefs.planets[:]:
            if p['rect'].left < 0:
                globalDefs.planets.remove(p)
                globalDefs.EarthHealth -= p['size']/10

    def redraw(kit, bear, planets):
        global window
        windowSurface.fill(globalDefs.BACKGROUNDCOLOR)
        windowSurface.blit(globalDefs.background, (0,0))
        
        #draw text
        drawText('Score: %s' % (globalDefs.score), font, windowSurface, 10, 0)
        drawText('Earth Health: %s' % (globalDefs.EarthHealth), font, windowSurface, 10, 48)
        drawText('spaceCat Health: %s' % (kit.health), font, windowSurface, 10, 96)
        # drawText('spaceBear Health: %s' % (bear.health), font, windowSurface, 10, 144)
        for p in globalDefs.planets:
            windowSurface.blit(p['surface'], p['rect'])
            
        kit.chargeKitty(windowSurface)
        windowSurface.blit(kit.kittyPic, kit.kitRect)
        kit.splazers(windowSurface, planets)

        if (beary.isSummoned()):
            beary.chargeBear(windowSurface)
            windowSurface.blit(beary.BearPic, beary.bearRect)

            beary.splazers(windowSurface, planets)

        # windowSurface.blit(corgi.image, corgi.rect)
        # corg.update(kit.kitRect, windowSurface)
        # corg.rockets.update(windowSurface)
        pygame.display.update()

        earthHealthIncrementer()
        mainClock.tick(globalDefs.FPS)

    def earthHealthIncrementer():
        globalDefs.earthHealthCounter +=1
        if (globalDefs.earthHealthCounter > 100 & globalDefs.EarthHealth < 100):
            globalDefs.EarthHealth += 1
            globalDefs.earthHealthCounter = 0

    def earthChecker():
        if globalDefs.EarthHealth <= 0:
            globalDefs.EarthHealth = 100
            earthDead()

    def eventChecker(event, kit):
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                kit.moveModder(True, False)
                beary.moveModder(True, False)
            if event.key == K_UP:
                kit.moveModder(False, True)
                beary.moveModder(False, True)
            if event.key == K_SPACE:
                kit.laserFire = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                drawText('press enter to unpause', font, windowSurface, (globalDefs.WINDOWWIDTH /3), (globalDefs.WINDOWHEIGHT / 3))
                drawText('press esc again to exit', font, windowSurface, (globalDefs.WINDOWWIDTH /3), (globalDefs.WINDOWHEIGHT / 3) + 50)
                pygame.display.update()
                waitKey()
            if event.key == K_UP:
                kit.moveModder(False, False)
                beary.moveModder(False, False)
            if event.key == K_DOWN:
                kit.moveModder(False, False)
                beary.moveModder(False, False)
            if event.key == K_SPACE:
                kit.laserFire = False

    def scoreChecker():
        if (globalDefs.score > 1):
            if (globalDefs.score % 100 == 0):
                globalDefs.score += 1
                beary.summon()
                kit.health = 100
                beary.health = 100
                for i in globalDefs.planets[:]:
                    globalDefs.planets.remove(i)

    def laserColDet(kit, beary):
        if kit.laserRect.colliderect(beary.bearRect) & kit.laserFire == True & beary.isSummoned() == True:
            beary.health -= kit.kitCharge/100.
        if beary.laserRect.colliderect(kit.kitRect) & beary.laserFire == True:
            kit.health -= beary.bearCharge/100.

    windowSurface.fill(globalDefs.BACKGROUNDCOLOR)
    windowSurface.blit(globalDefs.background, (0,0))

    drawText('KITTEN LASERS!', font, windowSurface, (globalDefs.WINDOWWIDTH /3), (globalDefs.WINDOWHEIGHT / 3))
    drawText("Protector of Earth. LaserCat has made it his sworn", font, windowSurface, (globalDefs.WINDOWWIDTH/8), (globalDefs.WINDOWHEIGHT / 3) + 50)
    drawText("duty to protect all Earthlings from the evil planets.", font, windowSurface, (globalDefs.WINDOWWIDTH/8), (globalDefs.WINDOWHEIGHT / 3)+ 100)
    drawText("PRESS ENTER TO BEGIN THE DEFENSE.", font, windowSurface, (globalDefs.WINDOWWIDTH/8), (globalDefs.WINDOWHEIGHT / 3)+150)
    pygame.display.update()
    waitKey()
    kit = kitty()
    kit.center()
    beary = bear()
    beary.center()
    # corg = Corgi()
    kitOptions = {"dead", kitDead}
    while True:
        for event in pygame.event.get():
            eventChecker(event, kit)

        globalDefs.planets = genPlanets(globalDefs.planets)
        if (kit.update() == "dead"):
            kitDead()

        beary.update()

        planetChecker()
 

        laserColDet(kit, beary)

        earthChecker()

        scoreChecker()

        redraw(kit, beary, globalDefs.planets)
        
