import random
import numpy as np
import matplotlib.pyplot as plt
import copy

from game import Game


class Model():

    def __init__(self):
        self.genModel()
        self.fitScore = -1

    def indexNodes(self, nodes, lookingFor):
        for j, List in enumerate(nodes):
            for i, value in enumerate(List):
                if value == lookingFor:
                    return (i, j)
        return -1
    
    def randomNode(self, nodes, baseNode):
        """Chooses a random node out of the list"""
        rng = np.random.default_rng()

        if baseNode == None:
            return rng.choice(rng.choice(nodes[:len(nodes)-1])) 
        else:
            return rng.choice(rng.choice(nodes[self.indexNodes(nodes, baseNode)[1]+1:]))#Indexes startingNode and gives node in a later Layer
    
    def genModel(self):
        #Layer 1 Nodes 1-5: Input nodes
        #Layer 2 Node 8: Middle nodes, may mutate for more
        #Layer 3 Nodes 6-7: Output nodes, either 0 or 1 for states 0 or 1
        self.nodes = np.array([np.array([1, 2, 3, 4, 5]), np.array([8, 9]), np.array([10]), np.array([11]),np.array([6, 7])])
        self.connections = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8:[], 9: [], 10: [], 11: []}

        
        

        #Starting connections
        for i in range(6):
            self.newConnection()

    def newConnection(self):

        
        count = 0
        run = True
        startingNode = self.randomNode(self.nodes, None)

        endNode = self.randomNode(self.nodes,  startingNode)
        while endNode in [node[0] for node in self.connections[startingNode]] and run:
            startingNode = self.randomNode(self.nodes, None)

            endNode = self.randomNode(self.nodes,  startingNode)

            count += 1
            if count == 50:
                run = False

        if run:
            self.connections[startingNode].append([endNode, random.randint(-100,100)/100])

    def Summary(self):
        return [self.nodes, self.connections]


    def predict(self, enemyDistance, enemyState, enemy2Distance, enemy2State, selfState):

        #Setting up base dict to establish connections
        values = {}
        
        for key, value in self.connections.items():        
            if self.indexNodes(self.nodes, key)[1] == 0:
                values[key] = [enemyDistance, enemyState, enemy2Distance, enemy2State, selfState][key-1]
            else:
                values[key] = 0
  

       
        #Adding all connections together
        for i in range(len(self.nodes)-1):
            for key, value in self.connections.items():
                if self.indexNodes(self.nodes, key)[1] == i and len(value) != 0:
                    for subValue in value:
                        try:
                            values[subValue[0]] += values[key]*subValue[1]
                        except Exception as e:
                            
                            print(self.nodes, self.connections, values, value, key, subValue, e)

        return 1 if values[6] > values[7] else 0



    def crossover(self, parent2):
        #Breeds two brains with this one having dominant genes:
        babyModel = np.array([np.array([1, 2, 3, 4, 5]), np.array([]), np.array([]), np.array([]), np.array([6, 7])])
        babyConnections = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8:[], 9: [], 10: [], 11: []}



        #The only layer that changes, since Layer 0 is input and Layer 2 is output
        nodeList = self.nodes[1:-1]
        otherNodeList = parent2.nodes[1:-1]

        for i, nodes in enumerate(nodeList):
            for node in nodes:
                if node in nodes:
                    babyModel[1+i] = np.append(babyModel[1+i], node)
                    babyConnections[node] = []
                    
                if self.indexNodes(otherNodeList, node) == -1 and random.randint(0,100) >= 75 and self.indexNodes(babyModel, node) == -1:
                    babyModel[1+i] = np.append(babyModel[1+i], node)
                    babyConnections[node] = []

        for i, otherNodes in enumerate(otherNodeList):
            for node in otherNodes:
                if node not in nodes and random.randint(0,100) <= 25 and self.indexNodes(babyModel, node) == -1:
                    babyModel[1+i] = np.append(babyModel[1+i], node)
                    babyConnections[node] = []

        #Changing connections where necessary
        for key, value in babyConnections.items():
            if random.randint(0, 100) >= 75:
                if key in self.connections:
                    for value in self.connections[key]:
                        if self.indexNodes(babyModel, value[0]) != -1:
                            babyConnections[key].append(value)
            else:
                if key in parent2.connections:
                    for value in parent2.connections[key]:
                        if self.indexNodes(babyModel, value[0]) != -1:
                            babyConnections[key].append(value)

        return babyModel, babyConnections

    def findMaxOf2dArray(self, array):
        highest = -99999
        highestIndex = -1
        for j, row in enumerate(array):
            for i, num in enumerate(row):
                if num > highest:
                    highest, highestIndex = num, [i,j]
        return highest

    def mutate(self):
        num = random.randint(0, 100)

        if num <= 80: #Change Weights
            node = self.randomNode(self.nodes, None)

            for i, value in enumerate(self.connections[node]):
                if random.randint(0, 100) <= 10:
                    self.connections[node][i][1] = random.randint(-100, 100)/100
                else: 
                    self.connections[node][i][1] += max(min(random.gauss(0,1)/50,1),-1)

                    
                    
        elif num <= 85: #Add Connection
            self.newConnection()
        elif num <= 86: #New node
            layer = random.randint(1, len(self.nodes)-2)

        
            node = self.findMaxOf2dArray(self.nodes) + 1

            self.nodes[layer] = np.append(self.nodes[layer], node)
            self.connections[node] = []
            

class DodgeNN():
    def generateInitialPopulation(self):

        self.populationSize = 100
        models = np.empty((self.populationSize), Model)

        for i in range(self.populationSize):
            models[i] = Model()

        self.models = models
        nn.generations = 0
      

    def fitnessFunc(self):    
        for i, model in enumerate(self.models):
            model.fitScore = self.simulateGame(model, False)




    def killPopulation(self, percent):

        maxScore = max(node.fitScore for node in self.models)
        stop = False
        if nn.generations % 5 == 0:
            for model in self.models:
                if model.fitScore == maxScore and not stop:
                    self.simulateGame(model, True) #Visualizes a game every 5 games, bc I'm bored and it looks cool
                    stop = True
        
        movingOn = []

    
        for i in range(20):
            groups = []
     
            for j in range(5):
                groups.append(random.choice(self.models))
                self.models = np.delete(self.models, np.where(self.models==groups[j]))
            movingOn.append(groups[groups.index(max(groups, key=lambda x: x.fitScore))])

        for model in movingOn:
            self.models = np.append(self.models, model)

        
        for i in range(self.populationSize-len(self.models)):
            self.models = np.append(self.models, self.genBabyModel(1-percent)) #Baby making time


        


            
                
    def genBabyModel(self, percentOfAlivePopulation):

        if random.randint(0,100) <= 25:
            return copy.deepcopy(random.choice(self.models[:int(percentOfAlivePopulation*len(self.models))])) #Random duplicate of alive person
        else:

            #Baby making time between two parents
            parent1 = random.choice(self.models[:20])

            parent2 = random.choice(self.models[:20])
            while parent1 == parent2:
                parent2 = random.choice(self.models[:int(percentOfAlivePopulation*len(self.models))]) #I mean, you can't breed with yourself

            #Stronger parent get's priority in genes 75% to 25%
            if parent1.fitScore >= parent2.fitScore:
                babyModel, babyConnections = parent1.crossover(parent2)
            else:
                babyModel, babyConnections = parent2.crossover(parent1)
         

            baby = Model()
            baby.nodes, baby.connections = babyModel, babyConnections

     
            baby.mutate() #Make the baby interesting
            

            return baby
        
       

    def simulateGame(self, model, visualize):

        
  
        game = Game(visualize)
        enemyDistance, enemyState, enemy2Distance, enemy2State, selfState = game.start()

        game.model = model.Summary()
       
        
        count = 0
        score = 0

        while game.running:

            state = model.predict(enemyDistance, enemyState, enemy2Distance, enemy2State, selfState)
            
            if game.enemyChange:
                score += 1

            enemyDistance, enemyState, enemy2Distance, enemy2State, selfState = game.run(state)

            if score >= 200:
                game.running = False


        return score

    def saveModel(self):
        model = self.models[0]

        with open("checkpoint.txt", "w") as file:
            file.write(str(model.Summary()))
      

  

if __name__ == "__main__":
  

    nn = DodgeNN()


    nn.generateInitialPopulation()
    
    while True:
        nn.fitnessFunc()

        avg = sum(model.fitScore for model in nn.models)/len(nn.models)
        print("Generation " +str(nn.generations) + " Average: " + str(avg))
        
        nn.killPopulation(0.5)

        print("Generation " +str(nn.generations) + " Highest: " + str(max(node.fitScore for node in nn.models)))


        nn.generations += 1
        if nn.generations % 5 == 0:
            nn.saveModel()



    
        
                    

                
