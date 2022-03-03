#TODO add scoring, add collision, add bot controls
#note pygame local docs cmd python -m pygame.docs 
import pygame

pygame.init()

# global variables
ScreenWidth = 640
ScreenHeight = 480

font = pygame.font.Font("ARCADECLASSIC.TTF", 100)

IsOpen = True
FPS = 120
KeyDown = False
KeyUp = False

window = pygame.display.set_mode((ScreenWidth, ScreenHeight))
clock = pygame.time.Clock()

#paddle class
class Paddles:
    def __init__(self, xcoord, ycoord, width, height):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.width = width
        self.height = height
        
    def RenderPaddle(self):
        # x, y, width, height
         pygame.draw.rect(window, (255, 255, 255), pygame.Rect(self.xcoord, self.ycoord, self.width, self.height))

    def MovePaddle(self, PaddleDown, PaddleUp):
        global IsOpen
        # control the paddles
        if PaddleDown:
            self.ycoord += 3
        if PaddleUp:
            self.ycoord -= 3
        #collision for the paddles
        if self.ycoord > ScreenHeight - 50:
            self.ycoord = ScreenHeight - 50
        if self.ycoord < 0:
            self.ycoord = 0
class Ball:
    def __init__(self, xcoord, ycoord, radius, moveleft, moveright, moveup, movedown, ballspeed):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.radius = radius
        self.ballspeed = ballspeed
        self.moveleft = moveleft
        self.moveright = moveright
        self.moveup =  moveup
        self.movedown = movedown
        

    def RenderBall(self):
        #x, y radius
        pygame.draw.circle(window, (255, 255, 255), [self.xcoord, self.ycoord], self.radius)

    def BallCollision(self):
        global ScreenHeight, ScreenWidth
        #bounces the ball up and down on the top and bottom of the screen
        if self.ycoord >= ScreenHeight - self.radius:
            self.moveup = True
            self.movedown = False
        if self.ycoord <= 0 + self.radius:
            self.moveup = False
            self.movedown = True
        #bounces the ball left and right on the left and right of the screen
        if self.xcoord >= ScreenWidth - self.radius:
            self.moveright = False
            self.moveleft = True
        if self.xcoord <= 0 + self.radius:
            self.moveright = True
            self.moveleft = False
        
    def BallMovement(self):
        #makes the ball move
        if self.moveleft == True:
            self.xcoord -= self.ballspeed
        if self.moveright == True:
            self.xcoord += self.ballspeed
        if self.moveup == True:
            self.ycoord -= self.ballspeed
        if self.movedown == True:
            self.ycoord += self.ballspeed

#create objects
paddle1 = Paddles(50, 240, 10, 60)
paddle2 = Paddles(560, 240, 10, 60)
# xcoord, ycoord, size, move left, move right, move up, movedown, ballspeed
ball = Ball(185, 135, 15, False, True, True, False, 1)

def PaddleBallCollsion():
    #collision for the paddle on the right
    if ball.xcoord + ball.radius >= paddle2.xcoord:
        if paddle2.ycoord + paddle2.height >= ball.ycoord > paddle2.ycoord:
            ball.moveright = False
            ball.moveleft = True
    #collision for the paddle on the left
    if ball.xcoord - ball.radius <= paddle1.xcoord:
        if paddle1.ycoord + paddle1.height >= ball.ycoord > paddle1.ycoord:
            ball.moveright = True
            ball.moveleft = False

#event method
def Events():
    global IsOpen, KeyUp, KeyDown
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            IsOpen = False

        #control the paddles
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                KeyUp = True
            elif event.key == pygame.K_DOWN:
                KeyDown = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                KeyUp = False
                KeyDown = False

    #keeps the movment comtrols continuous 
    if KeyUp:
        paddle1.MovePaddle(False, True)
    elif KeyDown:
        paddle1.MovePaddle(True, False)

    ball.BallCollision()
    ball.BallMovement()
    PaddleBallCollsion()
    
    
#render method
def Render():
    #window color
    window.fill((0, 0, 0))
    #renders paddles
    paddle1.RenderPaddle()
    paddle2.RenderPaddle()
    #renders ball
    ball.RenderBall()
    #renders the score numbers
    window.blit(font.render("0", False, (255, 255, 255)), (ScreenWidth - 570, ScreenHeight - 420))
    window.blit(font.render("0", False, (255, 255, 255)), (ScreenWidth - 130, ScreenHeight - 420))
    #updates the display
    pygame.display.update()

#game loop
while IsOpen:
    clock.tick(FPS) 
    Events()
    Render()
pygame.quit()
