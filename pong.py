"""The Pong Game."""
#pip install -U pysdl2
#pip install pysdl2-dll

import sys
import sdl2
import sdl2.ext
import sdl2.sdlttf

#Kolory
BLACK = sdl2.ext.Color(0, 0, 0)
WHITE = sdl2.ext.Color(255, 255, 255)
#Szybkośc paletek
PADDLE_SPEED = 3
BALL_SPEED = 3
#Punkty
player1_score = 0
player2_score = 0


class CollisionSystem(sdl2.ext.Applicator):

    def __init__(self, minx, miny, maxx, maxy):
        super(CollisionSystem, self).__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.ball = None
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy


    #Sprwadza czy piłka odbija dotka paletki
    def _overlap(self, item):
        sprite = item[1]
        #Ignoruje piłkę
        if sprite == self.ball.sprite:
            return False
        #Wczytuje pozycje piłki i paletki
        left, top, right, bottom = sprite.area
        bleft, btop, bright, bbottom = self.ball.sprite.area
        #Sprawdza czy piłka dotyka paletki
        return (bleft < right and bright > left and
                btop < bottom and bbottom > top)


    def process(self, world, componentsets):
        #Zmienne globalne punktów
        global player1_score
        global player2_score
        #Dla kazdego sprite'a sprawdza czy kolizuje z piłką
        collitems = [comp for comp in componentsets if self._overlap(comp)]
        #Jeśli jakiś sprite kolizuje z piłką zmienia kierunek lotu piłki
        if len(collitems) != 0:
            #Zmiana prędkości piłki dla osi x
            self.ball.velocity.vx = -self.ball.velocity.vx

            #Sprite kolizującego obiektu
            sprite = collitems[0][1]
            ballcentery = self.ball.sprite.y + self.ball.sprite.size[1] // 2
            halfheight = sprite.size[1] // 2
            stepsize = halfheight // 10
            degrees = 0.7
            paddlecentery = sprite.y + halfheight
            if ballcentery < paddlecentery:
                #factor - ilość kroków miedzy srodkiem paletki a piłki
                factor = (paddlecentery - ballcentery) // stepsize
                self.ball.velocity.vy = -int(round(factor * degrees))
            elif ballcentery > paddlecentery:
                factor = (ballcentery - paddlecentery) // stepsize
                self.ball.velocity.vy = int(round(factor * degrees))
            else:
                self.ball.velocity.vy = -self.ball.velocity.vy
        #Obsługa kolizji z górną i dolną częścią okna
        if (self.ball.sprite.y <= self.miny or
            self.ball.sprite.y + self.ball.sprite.size[1] >= self.maxy):
            self.ball.velocity.vy = -self.ball.velocity.vy
        #Obsługa kolizji z lewą i prawą częścią okna + zliczanie punktów
        if (self.ball.sprite.x <= self.minx or
            self.ball.sprite.x + self.ball.sprite.size[0] >= self.maxx):

            if self.ball.sprite.x<= self.minx:
                player2_score = player2_score+1
            else:
                player1_score = player1_score+1

            if player1_score > 9 or player2_score > 9:
                player1_score=0
                player2_score=0

            self.ball.sprite.x=390
            self.ball.sprite.y=290
            self.ball.velocity.vy = 0


class MovementSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def process(self, world, componentsets):
        for velocity, sprite in componentsets:
            #Wczytanie wysokości sprite'a
            sheight = sprite.size[1]
            #Zmiana pozycji sprite'a
            sprite.x += velocity.vx
            sprite.y += velocity.vy
            #Uniemożliwienie wyjścia poza okno z góry
            sprite.y = max(self.miny, sprite.y)
            # Dolna granica sprite'a
            pmaxy = sprite.y + sheight
            # Uniemożliwienie wyjścia poza okno z dołu
            if pmaxy > self.maxy:
                sprite.y = self.maxy - sheight


class TrackingAIController(sdl2.ext.Applicator):
    def __init__(self, miny, maxy):
        super(TrackingAIController, self).__init__()
        self.componenttypes = PlayerData, Velocity, sdl2.ext.Sprite
        self.miny = miny
        self.maxy = maxy
        self.ball = None

    def process(self, world, componentsets):
        for pdata, vel, sprite in componentsets:
            if not pdata.ai:
                continue

            sheight = sprite.size[1]
            centery = sprite.y + sheight // 2
            # Piłka oddala się od AI
            if self.ball.velocity.vx < 0:
                if centery < self.maxy // 2 - PADDLE_SPEED:
                    vel.vy = PADDLE_SPEED
                elif centery > self.maxy // 2 + PADDLE_SPEED:
                    vel.vy = -PADDLE_SPEED
                else:
                    vel.vy = 0
            # Piłka zbliża się do AI
            else:
                bcentery = self.ball.sprite.y + self.ball.sprite.size[1] // 2
                if bcentery < centery:
                    vel.vy = -PADDLE_SPEED
                elif bcentery > centery:
                    vel.vy = PADDLE_SPEED
                else:
                    vel.vy = 0


class SoftwareRenderSystem(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderSystem, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, BLACK)
        sdl2.ext.line(self.surface,WHITE,[400, 10, 400, 20, 400, 40, 400, 50, 400, 70, 400, 80, 400, 100, 400, 110, 400, 130, 400, 140, 400, 160, 400, 170, 400, 190, 400, 200, 400, 220, 400, 230, 400, 250, 400, 260, 400, 280, 400, 290, 400, 310, 400, 320, 400, 340, 400, 350, 400, 370, 400, 380, 400, 400, 400, 410, 400, 430, 400, 440, 400, 460, 400, 470, 400, 490, 400, 500, 400, 520, 400, 530, 400, 550, 400, 560, 400, 580, 400, 590],1)
        sdl2.ext.line(self.surface, WHITE,getListForNumber(player1_score,1) ,5)
        sdl2.ext.line(self.surface, WHITE,getListForNumber(player2_score,2), 5)
        super(SoftwareRenderSystem, self).render(components)


class Velocity(object):
    def __init__(self):
        super(Velocity, self).__init__()
        self.vx = 0
        self.vy = 0


class PlayerData(object):
    def __init__(self):
        super(PlayerData, self).__init__()
        self.ai = False



class Player(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0, ai=False):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity()
        self.playerdata = PlayerData()
        self.playerdata.ai = ai


class Ball(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity()

def getListForNumber(number,player):
    match number:
        case 0 :
            if player == 1:
                return [300,40,350,40, 348,38,348,107, 350,104,300,104, 302,107,302,40]
            else:
                return [500,40,450,40, 452,38,452,110, 450,107,500,107, 497,107,497,40]
        case 1:
            if player == 1:
                return [348,38,348,110]
            else:
                return [497,107,497,40]
        case 2:
            if player == 1:
                return [300,40,350,40,  348,38,348,72,  300,69,350,69,  302,107,302,69,  300,104,350,104]
            else:
                return [500,40,450,40, 500,38,500,72, 500,69,450,69, 452,107,452,69, 502,104,450,104]
        case 3:
            if player == 1:
                return [300,40,350,40,  348,38,348,107,  300,69,350,69,  350,104,300,104]
            else:
                return [500,40,450,40, 497,38,497,107, 500,69,450,69, 450,104,500,104]
        case 4:
            if player == 1:
                return [348,38,348,107, 300,69,350,69,  302,38,302,69]
            else:
                return [498,38,498,107, 500,69,450,69, 452,38,452,69]
        case 5:
            if player == 1:
                return [300,40,350,40,  300,38,300,72, 300,69,350,69, 347,107,347,69, 298,104,350,104]
            else:
                return [500, 40, 450, 40, 452, 38, 452, 72, 500, 69, 450, 69, 498, 107, 498, 69, 500, 104, 450, 104]
        case 6:
            if player == 1:
                return [300,40,350,40, 302,107,302,40, 300,104,350,104, 347,107,347,69, 300,69,350,69]
            else:
                return [500,40,450,40, 452,107,452,40, 500,104,450,104, 497,107,497,69, 500,69,450,69]
        case 7:
            if player == 1:
                return [300,40,350,40,348, 38, 348, 110]
            else:
                return [500,40,450,40, 497,107,497,40]
        case 8:
            if player == 1:
                return [300,40,350,40, 348,38,348,107, 350,104,300,104, 302,107,302,40, 300,69,350,69]
            else:
                return [500,40,450,40, 452,38,452,107, 450,104,500,104, 497,107,497,40, 500,69,450,69]
        case 9:
            if player == 1:
                return [300,40,350,40,  348,38,348,107,  300,69,350,69,  298,104,350,104, 300,38,300,72]
            else:
                return [500,40,450,40, 500,38,500,107, 500,69,450,69, 502,104,450,104, 452,38,452,72]




def run(ai):

    sdl2.ext.init()
    window = sdl2.ext.Window("The Pong Game", size=(800, 600))
    window.show()

    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

    #Tworzenie sprite'ów paletek i piłki
    sp_paddle1 = factory.from_color(WHITE, size=(20, 100))
    sp_paddle2 = factory.from_color(WHITE, size=(20, 100))
    sp_ball = factory.from_color(WHITE, size=(20, 20))
    #Tworzenie "Swiata" który przechwuje wszystkie encje i systemy gry
    world = sdl2.ext.World()

    #Inicjalizacja systemów
    movement = MovementSystem(0, 0, 800, 600)
    collision = CollisionSystem(0, 0, 800, 600)
    aicontroller = TrackingAIController(0, 600)
    spriterenderer = SoftwareRenderSystem(window)

    #Dodanie systemów do "świata"
    world.add_system(aicontroller)
    world.add_system(movement)
    world.add_system(collision)
    world.add_system(spriterenderer)
    #Twożenie entities graczy i piłki
    player1 = Player(world, sp_paddle1, 0, 250)
    player2 = Player(world, sp_paddle2, 780, 250, ai)
    ball = Ball(world, sp_ball, 390, 290)
    ball.velocity.vx = -BALL_SPEED
    collision.ball = ball
    aicontroller.ball = ball

    running = True
    while running:
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_UP and not ai:
                    player2.velocity.vy = -PADDLE_SPEED
                elif event.key.keysym.sym == sdl2.SDLK_DOWN and not ai:
                    player2.velocity.vy = PADDLE_SPEED
                if event.key.keysym.sym == sdl2.SDLK_w:
                    player1.velocity.vy = -PADDLE_SPEED
                elif event.key.keysym.sym == sdl2.SDLK_s:
                    player1.velocity.vy = PADDLE_SPEED
            elif event.type == sdl2.SDL_KEYUP:
                if event.key.keysym.sym in (sdl2.SDLK_w,sdl2.SDLK_s):
                    player1.velocity.vy = 0
                if event.key.keysym.sym in (sdl2.SDLK_UP, sdl2.SDLK_DOWN):
                    player2.velocity.vy = 0
        sdl2.SDL_Delay(10)
        world.process()


if __name__ == "__main__":
    sys.exit(run(True))