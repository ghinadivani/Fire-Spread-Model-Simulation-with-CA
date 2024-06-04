import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import random
from math import *
from matplotlib.widgets import Slider, Button


col_dict = {
    0:"grey",
    1:"green",
    2:"yellow"
}
cm = ListedColormap([col_dict[x] for x in col_dict.keys()])



class FireSpreadModel():

    def __init__(self, n, probTree, probBurning, probLightning, probImmune, time=0, mode='random', ver='simple', wind=False, windDir='N', windLevel=0, varyDirection=False) -> None:
        self.n = n
        self.probTree = probTree
        self.probBurning = probBurning
        self.probLightning = probLightning
        self.probImmune = probImmune
        self.t = 0
        self.mode = mode
        
        self.time = time

        self.ver = ver
        self.grid = np.array([[0 for i in range(n)] for j in range(n)])
        self.StepsToBurn = 1

        self.wind = wind
        self.windDir = windDir
        self.windLevel = windLevel
        self.varyDirection = varyDirection
        self.varyDirectionAfter = floor(np.random.uniform(0,5))
        self.waitToVary = 0
        self.windDirArr = [self.windDir]

    def initRandomForest(self):
        #init trees
        for i in range(self.n):
            for j in range(self.n):
                p = np.random.uniform(0,1)
                if(p<self.probTree):
                    self.grid[i][j] = 1
        #init fire
        for i in range(self.n):
            for j in range(self.n):
                p = np.random.uniform(0,1)
                if(p<self.probBurning):
                    if(self.grid[i][j] == 1):
                        self.burn(i,j)
                        

    def burn(self,x,y):
        if (self.ver == 'simple'):
            self.grid[x][y] = 2
        elif(self.ver == 'better'):
            self.grid[x][y] = 2 + self.StepsToBurn

    def initAllTree(self):
        for i in range(self.n):
            for j in range(self.n):
                self.grid[i][j] = 1

    def BurningNeighbour(self, x, y, gridPrev):
        count = 0
        if gridPrev[(x)%self.n][(y - 1)%self.n] >= 2:
            count += 1
        if gridPrev[(x)%self.n][(y + 1)%self.n] >= 2:
            count += 1
        if gridPrev[(x + 1)%self.n][(y)%self.n] >= 2:
            count += 1
        if gridPrev[(x - 1)%self.n][(y)%self.n] >= 2:
            count += 1
            
        return count
    
    def BurnWithWind(self, x, y, gridPrev, p):
        if  (self.windDir == 'N' and gridPrev[(x)%self.n][(y + 1)%self.n] >= 2) or \
            (self.windDir == 'S' and gridPrev[(x)%self.n][(y - 1)%self.n] >= 2) or \
            (self.windDir == 'E' and gridPrev[(x-1)%self.n][(y)%self.n] >= 2) or \
            (self.windDir == 'W' and gridPrev[(x+1)%self.n][(y)%self.n] >= 2):
            tempImmune = self.probImmune**(self.windLevel+1)
            if p > tempImmune:
                return True
        else:
            if p > self.probImmune:
                return True
        return False

    def ApplyDiffusion(self):     
        gridPrev = self.grid.copy()
        for x in range(self.n):
            for y in range(self.n):
                if gridPrev[x][y] == 1:
                        
                    p = np.random.uniform(0,1)
                    burninCount = self.BurningNeighbour(x,y, gridPrev)
                    if burninCount != 0:
                        if p>self.probImmune:
                            if self.ver == 'simple':
                                    self.burn(x,y)
                            elif self.ver == 'better':
                                if self.wind:
                                    if self.BurnWithWind(x,y,gridPrev,p):
                                        self.burn(x,y)
                                else:
                                    if(p>(self.probImmune/burninCount)):
                                        self.burn(x,y)   
                        if x == 0 or x == self.n - 1 or y == 0 or y == self.n - 1:
                            self.grid[x][y] = 0                            
                    if p < self.probLightning:
                        self.burn(x,y)
            
        for x in range(self.n):
            for y in range(self.n):
                if(gridPrev[x][y] == 2):
                    self.grid[x][y]=0
                elif(gridPrev[x][y] > 2):
                    self.grid[x][y]-=1


    def run(self):
        if (self.mode == 'random'):
            self.initRandomForest()
        elif (self.mode == 'center'):
            self.initAllTree()
            self.grid[int(self.n/2)][int(self.n/2)] = 2
            

        self.grids=[np.array(self.grid)]
        self.sim()
    
    def sim(self):
        if self.time == 0:
            self.ApplyDiffusion()
            self.t += 1
            self.ApplyDiffusion()
            self.grids.append(np.array(self.grid))
            self.t += 1
            self.windDirArr.append(self.windDir)
            while self.comprGrids():
                self.ApplyDiffusion()
                self.windDirArr.append(self.windDir)
                if self.varyDirection & (self.waitToVary >= self.varyDirectionAfter):
                    self.varyDirectionAfter = floor(np.random.uniform(0,5))
                    self.waitToVary = 0
                    direciton = floor(np.random.uniform(0,4))
                    if (direciton== 0):
                        self.windDir = 'N'
                    elif (direciton == 1):
                        self.windDir = 'E'
                    elif (direciton == 2):
                        self.windDir == 'S'
                    elif (direciton == 3):
                        self.windDir = 'W'

                self.grids.append(np.array(self.grid))
                self.t += 1
                self.waitToVary += 1
            self.time = self.t
        else:
            for t in range(self.time):
                self.ApplyDiffusion()
                self.grids.append(np.array(self.grid))


    def comprGrids(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.grids[-1][i][j] != self.grids[-2][i][j]:
                    return True
        return False
    
    def view(self):
    
        fig, ax = plt.subplots(figsize=[5,5])
        plt.subplots_adjust(bottom=0.35)

        ani = plt.imshow(self.grids[0], cmap=cm)

        timeSlider = Slider(plt.axes([0.1,0.9,0.8,0.04]), 'time', 0, self.t, valstep=1)

        def update(val):
            ani.set_data(self.grids[timeSlider.val])

        timeSlider.on_changed(update)
        plt.show()

