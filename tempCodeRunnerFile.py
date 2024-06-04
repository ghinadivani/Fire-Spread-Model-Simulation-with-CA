from tkinter import font

from matplotlib.pyplot import text
from FireSpreadModel import FireSpreadModel
import pygame
import time
from pygame.locals import *
import numpy as np

WHITE = (255,255,255)
GREY = (105,105,105)
BURNING = (255,0,0)
TREE = (0,120,0)
BLACK = (0,0,0)


pygame.init()
pygame.font.init()

sideBar = 500
font = pygame.font.Font('./font.ttf', 32)

class Simulator():
    def __init__(self) -> None:
        self.running = True
        self.n = 100
        self.cellSize = 5
        self.windowWidth = self.n * self.cellSize
        self.play = False  
        self.start = time.time()  
        self.fps = float(7)
        self.start = time.time()
        self.playBackSpeed = float(1 / self.fps)  
        self.frame = 0  
        self.frame = 0
        self.screen = pygame.display.set_mode((self.windowWidth + sideBar, self.windowWidth))      
        pygame.display.set_caption('Simulasi Penyebaran Kebakaran Hutan')  
        self.backgroundColor = BLACK
        
        # User inputs untuk parameter
        wind_input = input("Masukkan angin (Y/N): ").upper()
        wind_dir_input = input("Masukkan arah angin (N, S, E, W): ").upper()
        wind_level_input = int(input("Masukkan level/kecepatan angin (0 : tidak ada, 1 : rendah, 2 : sedang, 3 : tinggi): "))
        vary_direction_input = input("Apakah arah angin bervariasi? (Y/N): ").upper()

        wind = True if wind_input == 'Y' else False
        wind_dir = wind_dir_input if wind else 'N' 
        wind_level = wind_level_input if wind else 0  
        vary_direction = True if vary_direction_input == 'Y' else False
        self.fireModel = FireSpreadModel(self.n, 0.8, 0.5, 0.00, 0.4, 0, 'center', 'simple', wind, wind_dir, wind_level, vary_direction)
        self.fireModel.run()
        self.frameMax = self.fireModel.time

    def run(self):
        while self.running:
            self.event()
            self.Update()
            self.Render()

        self.save_results()

    def Render(self):
        self.drawGrid()
        self.Text('t = {}  (t_max = {})'.format(self.frame, self.frameMax), 0)
        self.Text('Speed: {}'.format(self.fps), 1)

        if self.play:
            self.Text('status: putar', 2)
        else:
            self.Text('status: jeda', 2)
        
        if self.fireModel.wind:
            if(self.fireModel.windDirArr[self.frame] == 'N'):
                self.Text('Angin: N (Atas)', 3)
            elif(self.fireModel.windDirArr[self.frame] == 'S'):
                self.Text('Angin: S (Bawah)', 3)
            elif(self.fireModel.windDirArr[self.frame] == 'E'):
                self.Text('Angin: E (Kanan)', 3)
            elif(self.fireModel.windDirArr[self.frame] == 'W'):
                self.Text('Angin: W (Kiri)', 3)
        else:
            self.Text('Angin: Tidak Ada', 3)
        pygame.display.update()
        self.screen.fill(self.backgroundColor)
    
    def Update(self):
        if(self.play & (time.time()-self.start >= self.playBackSpeed)):
            self.start = time.time()
            self.frame = min(self.frame + 1, self.frameMax-1)
            if self.frame == self.frameMax-1:
                self.play = not self.play

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.frame = max(self.frame - 1, 0)
                if event.key == pygame.K_RIGHT:
                    self.frame = min(self.frame + 1, self.frameMax)
                if event.key == pygame.K_SPACE:
                    self.start = time.time()
                    self.play = not self.play
                if event.key == pygame.K_p:
                    self.fps += 1
                    self.fps = min(self.fps, 60)
                    self.playBackSpeed = 1/self.fps
                if event.key == pygame.K_o:
                    self.fps -= 1
                    self.fps = max(self.fps, 1)
                    self.playBackSpeed = 1/self.fps
                if event.key == pygame.K_r:
                    self.frame = 0
            if event.type == pygame.QUIT:
                self.running = False
    
    def Text(self, tex, line):
        text = font.render(tex, True, WHITE)
        textRect = text.get_rect()
        textRect.x = self.windowWidth + 5
        textRect.y += line*textRect.height
        self.screen.blit(text, textRect)

    def drawGrid(self):
        for i in range(self.fireModel.n):
            for j in range(self.fireModel.n):
                rect = pygame.Rect(i*self.cellSize, j*self.cellSize, self.cellSize, self.cellSize)
                currentCellState = self.fireModel.grids[self.frame][i][j]
                if (currentCellState == 0):
                    pygame.draw.rect(self.screen, BLACK, rect)
                elif (currentCellState == 1):
                    pygame.draw.rect(self.screen, TREE, rect)
                elif (currentCellState >= 2):
                    pygame.draw.rect(self.screen, BURNING, rect)
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(0, 0, self.windowWidth,self.windowWidth),1)

    def save_results(self):
        with open('simulation_results.txt', 'w') as f:
            f.write(f"Nilai Probabilitas: \n")
            f.write(f"Probabilitas Pohon Tumbuh: {self.fireModel.probTree}\n")
            f.write(f"Probabilitas Pohon Terbakar: {self.fireModel.probBurning}\n")
            f.write(f"Probabilitas Sambaran Petir: {self.fireModel.probLightning}\n")
            f.write(f"Probabilitas Kekebalan Pohon: {self.fireModel.probImmune}\n\n")
            f.write("Parameter simulasi:\n")
            f.write(f"Angin: {'Ya' if self.fireModel.wind else 'Tidak'}\n")
            f.write(f"Arah Angin: {self.fireModel.windDir}\n")
            f.write(f"Tingkat Angin: {self.fireModel.windLevel}\n")
            f.write(f"Arah Angin Bervariasi: {'Ya' if self.fireModel.varyDirection else 'Tidak'}\n\n")

            f.write("Hasil simulasi:\n")
            f.write(f"Jumlah sel: {self.n * self.n}\n")
            for t in range(0, self.frameMax, 5):
                unburned_cells = np.count_nonzero(self.fireModel.grids[t] == 1)
                burning_cells = np.count_nonzero(self.fireModel.grids[t] == 2)
                f.write(f"t = {t}: {unburned_cells} sel tidak terbakar, {burning_cells} sel terbakar\n")
            final_unburned_cells = np.count_nonzero(self.fireModel.grids[-1] == 1)
            final_burning_cells = np.count_nonzero(self.fireModel.grids[-1] == 2)
            f.write(f"t = {self.frameMax}: {final_unburned_cells} sel tidak terbakar, {final_burning_cells} sel terbakar\n")

sim = Simulator()
sim.run()
