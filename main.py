import pygame # Importing Pygame module
from pygame.locals import * 
import random # To produce random variables
import sys # To exit Game
import time # To slowly increase speed of game as time passes

pygame.init() # Intializing PyGame

# GLOBAL VARIABLES
FPS = 32
SCREENWIDTH = 1100 # Setting Screen Width
SCREENHEIGHT = 600 # Setting Screen Height
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT)) # Setting Screen
GAME_SPRITES = {} # Blank Dictionary for Game Images
GAME_SOUNDS = {} # Blank Dictionary for Game Sounds
FPSCLOCK = pygame.time.Clock()
BLACK = (0,0,0)
FONT = pygame.font.SysFont(None, 55)
pygame.display.set_caption('TB Dino Game')

# Bird Images
GAME_SPRITES['bird'] = [
    pygame.image.load('gallery/sprites/Bird/Bird1.png'),
    pygame.image.load('gallery/sprites/Bird/Bird2.png')
]

# Large Cactus Images
GAME_SPRITES['largeCactus'] = [
    pygame.image.load('gallery/sprites/Cactus/LargeCactus1.png'),
    pygame.image.load('gallery/sprites/Cactus/LargeCactus2.png'),
    pygame.image.load('gallery/sprites/Cactus/LargeCactus3.png')
]

# Small Cactus Images
GAME_SPRITES['smallCactus'] = [
    pygame.image.load('gallery/sprites/Cactus/SmallCactus1.png'),
    pygame.image.load('gallery/sprites/Cactus/SmallCactus2.png'),
    pygame.image.load('gallery/sprites/Cactus/SmallCactus3.png')
]

# Dino Dead Image
GAME_SPRITES['dinoDead'] = pygame.image.load('gallery/sprites/Dino/DinoDead.png')

# Ducking Dino Images
GAME_SPRITES['dinoDuck'] = [
    pygame.image.load('gallery/sprites/Dino/DinoDuck1.png'),
    pygame.image.load('gallery/sprites/Dino/DinoDuck2.png')
]

# Jumping Dino Image
GAME_SPRITES['dinoJump'] = pygame.image.load('gallery/sprites/Dino/DinoJump.png')

# Running Dino Images
GAME_SPRITES['dinoRun'] = [
    pygame.image.load('gallery/sprites/Dino/DinoRun1.png'),
    pygame.image.load('gallery/sprites/Dino/DinoRun2.png')
]

# Dino Starting Image
GAME_SPRITES['dinoStart'] = pygame.image.load('gallery/sprites/Dino/DinoStart.png')

# Background Image
GAME_SPRITES['background'] = pygame.image.load('gallery/sprites/Other/blank-background.png')

# Dino Starting Image
GAME_SPRITES['cloud'] = pygame.image.load('gallery/sprites/Other/Cloud.png')

# Welcome Screen Image
GAME_SPRITES['welcomeScreen'] = pygame.image.load('gallery/sprites/Other/welcome-screen.png')

# Track Image
GAME_SPRITES['track'] = pygame.image.load('gallery/sprites/Other/Track.png')

# SETTING SOUNDS USED IN GAME

# Hit Sound
GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')

# Point Sound
GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')

# Wing Sound
GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')


class Dinosaur:
    ''' The main class where the game will be made '''
    def __init__(self):
        self.dinoImage = GAME_SPRITES['dinoStart'] # Setting Default Dino Image to tb Dino Starting Image
        self.dinoX = 60 # Setting Default X-Coordinate of the dino
        self.dinoY = 300 # Setting Default Y-Coordinate of the dino
        self.trackX = 0
        self.trackY = 370
        self.dinoRun = False # This variable will be True when dino will start running
        self.dinoDuck = False # This variable will be True when dino will start running
        self.dinoVelYIncreament = 0 # This is the increase in Y-velocity of dino
        self.dinoVelyValue = 6 + self.dinoVelYIncreament # Value of dino Velocity
        self.dinoVely = 0 # Velocity of dino
        self.obstacleVelXIncreament = 0
        self.obstacleVelX = -6 - self.obstacleVelXIncreament
        self.cloudVelX = -3
        self.gameOver = False
        self.score = 0
        self.dinoRunAnimationCount = 0 # This is the animation count that will help in animating the dino while its running
        self.dinoDuckAnimationCount = 0 # This is the animation count that will help in animating the dino while its ducking
        self.BirdAnimationCount = 0 # This is the animation count that will help in animating the bird

    
    def getRandomCloud(self):
        ''' This Function will return random coordinates of Clouds to blit '''
        self.cloudX = SCREENWIDTH + GAME_SPRITES['dinoJump'].get_width() + 10
        self.cloudY = random.randint(0,282)

        self.randomCloudCoordinatesList = [self.cloudX,self.cloudY]

        return self.randomCloudCoordinatesList
    
    def getRandomObstacle(self):
        ''' This function wll give a random obstacle '''
        self.randomObstacleChoiceVar = random.randint(0,1)
        self.randomObstacle = []
        if self.randomObstacleChoiceVar == 0:
            self.randomObstacle = ['b']
        
        elif self.randomObstacleChoiceVar == 1:
            self.radomCactusChoiceVar = random.randint(0,1)
            if self.radomCactusChoiceVar == 0:
                self.randomObstacle = ['lc',random.randint(0,2)]
            elif self.radomCactusChoiceVar == 1:
                self.randomObstacle = ['sc',random.randint(0,2)]
        
        return self.randomObstacle

    def getRadomObstacleCoordinates(self):
        ''' This function will return the coordinates of random obstacles '''
        self.randomObstacleFunc = self.getRandomObstacle()
        if self.randomObstacleFunc[0] == 'b':
            self.randomObstacleCoordinatesList = {'x':SCREENWIDTH+100,'y':self.trackY - 80 - GAME_SPRITES['bird'][1].get_height(),'obstacle':'bird'}
        else:
            if self.randomObstacleFunc[0] == 'lc':
                self.randomObstacleCoordinatesList = {'x':SCREENWIDTH+100,'y':self.trackY - GAME_SPRITES['largeCactus'][self.randomObstacleFunc[1]].get_height() + 10 ,'obstacle':'largeCactus', 'index':self.randomObstacleFunc[1]}
            
            elif self.randomObstacleFunc[0] == 'sc':
                self.randomObstacleCoordinatesList = {'x':SCREENWIDTH+100,'y':self.trackY - GAME_SPRITES['smallCactus'][self.randomObstacleFunc[1]].get_height() + 10 ,'obstacle':'smallCactus', 'index':self.randomObstacleFunc[1]}

        return self.randomObstacleCoordinatesList
    
    def textScreen(self,text, color, x, y):
        self.screen_text = FONT.render(text, True, color)
        SCREEN.blit(self.screen_text, [x,y])
        
    
    def welcomeScreen(self):
        ''' This function will display the welcome screen of the Game '''
        while True:
            for event in pygame.event.get():
                # The below condition will quit the game 
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                
                if event.type == KEYDOWN and event.key == K_RETURN:
                    return
            
            SCREEN.blit(GAME_SPRITES['welcomeScreen'],(0,0))
            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def mainGame(self):
        ''' Main Game Function '''
        self.markedTime = time.time()
        self.dinoVelyValue = 7 + self.dinoVelYIncreament # Value of dino Velocity

        self.newCloud = self.getRandomCloud()

        self.randomCLoud = [
            {'x' : self.newCloud[0], 'y' : self.newCloud[1] }
        ]
        self.newObstacleList = []

        self.newObstacleFunc = self.getRadomObstacleCoordinates()
        if self.newObstacleFunc['obstacle'] == 'bird':
            self.newObstacleList = [
                {'x':self.newObstacleFunc['x'] , 'y':self.newObstacleFunc['y'] , 'image':'bird' , 'imageVar' : GAME_SPRITES['bird'][0]}
            ]
        
        else :
            self.newObstacleList = [
                {'x':self.newObstacleFunc['x'] , 'y':self.newObstacleFunc['y'] , 'image':GAME_SPRITES[self.newObstacleFunc['obstacle']][self.newObstacleFunc['index']]}
            ]

        self.birdImage = GAME_SPRITES['bird'][1]
        self.gameOver = False
        self.score = 0
        self.dinoX = 60 # Setting Default X-Coordinate of the dino
        self.dinoY = 300 # Setting Default Y-Coordinate of the dino
        self.dinoVely = 0
        self.dinoImage = GAME_SPRITES['dinoStart']
        self.dinoRun = False
        self.dinoJump = False
        self.dinoDuck = False

        # if self.newObstacle

        while True:
            for event in pygame.event.get():
                # The below condition will quit the game 
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if not self.dinoRun and (event.key == K_UP or event.key == K_SPACE):
                        self.dinoRun = True # Starting Dino to move
                        self.dinoDuck = False
                    
                    if ( self.dinoRun) and (event.key == K_UP or event.key == K_SPACE) :
                        self.dinoVely = -self.dinoVelyValue # Making Velocity of dino
                        GAME_SOUNDS['wing'].play()
                    
                    if event.key == K_DOWN:
                        self.dinoDuck = True
                        self.dinoRun = False
            
            self.randomListAppendY = random.randint(SCREENWIDTH/4,SCREENHEIGHT)


            # Increasing Y of Dino with Velocity of Dino
            self.dinoY += self.dinoVely
            
            # crashTest = self.isCollide(self.dinoX,self.dinoY,self.dinoImage,self.newObstacleList)
            
            self.dinoMidPos = self.dinoX + self.dinoImage.get_width()/2
            for obstacle in self.newObstacleList:
                if obstacle['image'] == 'bird':
                    self.obstacleMidPos = obstacle['x'] + obstacle['imageVar'].get_width()/2

                    if (abs(obstacle['x'] - self.dinoX) < self.dinoImage.get_width() or abs(obstacle['x'] - self.dinoX) < obstacle['imageVar'].get_width()) and (abs(obstacle['y'] - self.dinoY) < self.dinoImage.get_height() or abs(obstacle['y'] - self.dinoY) < obstacle['imageVar'].get_height() ):
                        self.gameOver = True
                
                else:
                    self.obstacleMidPos = obstacle['x'] + obstacle['image'].get_width()/2
                    if (abs(obstacle['x'] - self.dinoX) < self.dinoImage.get_width() or abs(obstacle['x'] - self.dinoX) < obstacle['image'].get_width()) and (abs(obstacle['y'] - self.dinoY) < self.dinoImage.get_height() or abs(obstacle['y'] - self.dinoY) < obstacle['image'].get_height()):
                        self.gameOver = True
                    
                if self.obstacleMidPos<= self.dinoMidPos < self.obstacleMidPos + 15:
                    self.score += 10
                    print(f"Your score is {self.score}") 
                    GAME_SOUNDS['point'].play()
            
                

            if self.gameOver:
                GAME_SOUNDS['hit'].play()
                return

            for item in self.randomCLoud:
                item['x'] += self.cloudVelX
                # print(f"The X-Coordinate of Cloud is {item['x']}")
            
            for item2 in self.newObstacleList:
                item2['x'] += self.obstacleVelX
                # print(f"The X-Coordinate of Cloud is {item['x']}")
            
            # The Below Code will add Clouds
            if self.randomCLoud[len(self.randomCLoud) - 1]['x'] < 3*SCREENWIDTH/4:
                self.newCloud1 = self.getRandomCloud()
                self.newRandomCLoud = {'x':self.newCloud1[0] , 'y':self.newCloud1[1]}
                self.randomCLoud.append(self.newRandomCLoud)
            
            if self.randomCLoud[0]['x'] < -GAME_SPRITES['cloud'].get_width():
                self.randomCLoud.pop(0)

            if self.newObstacleList[len(self.newObstacleList) - 1]['x'] < self.randomListAppendY:
                self.newObstacle1 = self.getRadomObstacleCoordinates()
                if self.newObstacle1['obstacle'] == 'bird':
                    self.newObstacle1Dict = {'x':self.newObstacle1['x'] , 'y':self.newObstacle1['y'] , 'image':'bird' , 'imageVar' : GAME_SPRITES['bird'][1]}
                
                else:
                    self.newObstacle1Dict = {'x':self.newObstacle1['x'] , 'y':self.newObstacle1['y'] , 'image':GAME_SPRITES[self.newObstacle1['obstacle']][self.newObstacle1['index']]}
                
                self.newObstacleList.append(self.newObstacle1Dict)
            
            if self.newObstacleList[0]['x'] < -GAME_SPRITES['largeCactus'][2].get_width():
                self.newObstacleList.pop(0)

            if self.dinoRun:
                self.dinoRunAnimationCount += 1
            
            if self.dinoDuck:
                self.dinoDuckAnimationCount += 1

            if self.dinoRunAnimationCount == 9:
                self.dinoImage = GAME_SPRITES['dinoRun'][0]
            elif self.dinoRunAnimationCount == 18:
                self.dinoImage = GAME_SPRITES['dinoRun'][1]
                self.dinoRunAnimationCount = 0
            
            if self.dinoDuckAnimationCount == 9:
                self.dinoImage = GAME_SPRITES['dinoDuck'][0]
            elif self.dinoDuckAnimationCount == 18:
                self.dinoImage = GAME_SPRITES['dinoDuck'][1]
                self.dinoDuckAnimationCount = 0
            
            if self.dinoY < 40:
                self.dinoVely = self.dinoVelyValue
            
            if self.dinoY > 300:
                self.dinoVely = 0
            
            if self.markedTime - time.time() > 30:
                self.dinoVelYncreament += 3
                self.obstacleVelXIncreament += 3
                self.markedTime = time.time()
            
            if self.dinoY < 300:
                self.dinoImage = GAME_SPRITES['dinoJump']
                self.dinoJump = True
            
            SCREEN.blit(GAME_SPRITES['background'],(0,0)) # Blitting Blank Background Image
            SCREEN.blit(GAME_SPRITES['track'], (self.trackX,self.trackY))
            
            for i in self.randomCLoud:
                SCREEN.blit(GAME_SPRITES['cloud'], (i['x'],i['y']))
            
            for index in self.newObstacleList:
                if index['image'] == 'bird':
                    SCREEN.blit(index['imageVar'], (index['x'],index['y']))
                else:
                    SCREEN.blit(index['image'], (index['x'],index['y']))


            if self.dinoImage == GAME_SPRITES['dinoDuck'][0] or self.dinoImage == GAME_SPRITES['dinoDuck'][1]:
                SCREEN.blit(self.dinoImage, (self.dinoX,self.dinoY + 32)) # Blitting Dinosaur Image
            else:
                SCREEN.blit(self.dinoImage, (self.dinoX,self.dinoY)) # Blitting Dinosaur Image
            
            self.textScreen(f"Score: {self.score}", BLACK, SCREENWIDTH - 250, 12)
            pygame.display.update() # Updating Display
            # print(pygame.mouse.get_pos())

            # FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    dinosaurObject = Dinosaur()
    while True:
        dinosaurObject.welcomeScreen()
        dinosaurObject.mainGame()