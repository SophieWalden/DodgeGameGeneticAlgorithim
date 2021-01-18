import sys
 
import pygame
from pygame.locals import *
import random


#if __name__ == "__main__":
if True == True:
    pygame.init()
     
    fps = 60
    fpsClock = pygame.time.Clock()
     
    width, height = 600, 700
    gameDisplay = pygame.display.set_mode((width, height))





class Game:
    def __init__(self, gui=False):
        self.gui = gui #Rendering: bool
        self.stage = 0 #Player on left or right side: Integer
        self.enemy = () #Enemies raining down: Tuple: (Int, Int)
        self.enemy2 = () #Second enemy for more challenge: Tuple: (Int, Int)
        self.running = True #Declares whether the game should still run: Bool
        self.speed = 1 #How fast the enemies are going: Integer
        self.enemyChange = False #The frame the enemy changes
        self.changeState = False
        self.model = []

    def start(self):
        self.gen_enemy(1, 0)
        self.gen_enemy(2, -350)

        return self.generateObservation()

    def gen_enemy(self, num, offset):
        if num == 1:
            self.enemy = [offset, random.randint(0, 1)]
        else:
            self.enemy2 = [offset, random.randint(0, 1)]

    def generateObservation(self):
        return float(self.enemy[0]/700), self.enemy[1], float(self.enemy2[0]/700), self.enemy2[1], self.stage
    
    def run(self, step):

        if self.gui:
            self.draw()

        self.changeState = False
        prevStage = self.stage
        self.stage = step
        if prevStage != self.stage:
            self.changeState = True

        #First enemy
        self.enemyChange = False
        if self.enemy[0] > 700:
            self.gen_enemy(1, 0)
            self.enemyChange = True
    
        self.enemy[0] += self.speed


        #Second enemy
        if self.enemy2[0] > 700:
            self.gen_enemy(2, 0)
            self.enemyChange = True
  
        self.enemy2[0] += self.speed

        self.speed += 0.01

        if self.collided() == 1:
            self.running = False

        return self.generateObservation()

    def indexNodes(self, nodes, lookingFor):
        for j, List in enumerate(nodes):
            for i, value in enumerate(List):
                try:
                    if value == lookingFor[0]:
                        return (i, j)
                except Exception as e:
                    if value == lookingFor:
                        return (i, j)
                    #print(value, lookingFor, e, "This is in game.py under index Nodes")

    def draw(self):
        """Draws everything, if gui == True"""

        gameDisplay.fill((200, 200, 200))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        #Draws player
        pygame.draw.rect(gameDisplay, (200, 0, 0), (int(50+250*self.stage), 600, 50, 50), 0)
        pygame.draw.rect(gameDisplay, (0, 0, 0), (int(50+250*self.stage), 600, 50, 50), 3)

        #Draws enemy
        pygame.draw.rect(gameDisplay, (0, 0, 200), (int(50+250*self.enemy[1]), int(self.enemy[0]), 50, 50), 0)
        pygame.draw.rect(gameDisplay, (0, 0, 0), (int(50+250*self.enemy[1]), int(self.enemy[0]), 50, 50), 3)
        
        pygame.draw.rect(gameDisplay, (0, 0, 200), (int(50+250*self.enemy2[1]), int(self.enemy2[0]), 50, 50), 0)
        pygame.draw.rect(gameDisplay, (0, 0, 0), (int(50+250*self.enemy2[1]), int(self.enemy2[0]), 50, 50), 3)

        
        if self.model != []:
            model, connections = self.model[0], self.model[1]

            for key, value in connections.items():
                startCords = self.indexNodes(model, key)
                for subValue in value:
                    endCords = self.indexNodes(model, subValue)

            
                   
                    pygame.draw.line(gameDisplay, (max(min(255 * subValue[1], 255), 0) if subValue[1] >= 0 else 0, 0, max(min(255 * subValue[1] * -1, 255), 0) if subValue[1] < 0 else 0), (400+50*startCords[1], int(100+25*startCords[0]+75-(len(model[startCords[1]])*12.5))),
                                     (400+50*endCords[1], int(100+25*endCords[0]+75-(len(model[endCords[1]])*12.5))), 5)
            
            for j, layer in enumerate(model):
                for i, node in enumerate(layer):
                        
                    pygame.draw.circle(gameDisplay, (255, 255, 255), (400+50*j, int(100+25*i+75-(len(layer)*12.5))), 10) 
                    

            
        pygame.display.flip()
        fpsClock.tick(120)
        

    def collided(self):
        if 600 <= self.enemy[0] <= 650+self.speed and self.stage == self.enemy[1]:
            return 1
        if 600 <= self.enemy2[0] <= 650+self.speed and self.stage == self.enemy2[1]:
            return 1
        return 0


if __name__ == "__main__":
    while True:
        game = Game(gui=True)

        game.start()


        state = 0
        while game.running:
            keys = pygame.key.get_pressed()
            if keys[ord('a')]:
                state = 0
            if keys[ord('d')]:
                state = 1
            observation = game.run(state)
        
