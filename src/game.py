import pygame
from random import randint

pygame.init()


class MainGame(object):
    def __init__(self):
        self.background_color = (85, 153, 204)
        self.colors = [(153, 204, 238), (255, 255, 255), (255, 34, 62), (72, 255, 34), (33, 226, 217), (255, 255, 0)]
        self.grid = []
        self.initGrid()
        self.width = 50
        self.height = 50
        self.margin = 3
        self.window_size = [1100, 900]
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption('Ball game')
        self.clock = pygame.time.Clock()
        self.alive = True
        self.score = 0
        self.sec = 0
        self.font1 = pygame.font.SysFont('comicsans', 40)
        self.font2 = pygame.font.SysFont('comicsans', 60)
        self.font3 = pygame.font.SysFont('comicsans', 120)
        self.flag = False
        self.randomed = [0, 0]
        self.randomColor()
        self.startBall()
        while self.alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[0] > 820:
                        continue
                    column = (pos[0] - 25) // (self.width + self.margin)
                    row = (pos[1] - 20) // (self.height + self.margin)
                    if self.flag is False and self.grid[row][column] != 0:
                        row1 = row
                        cl1 = column
                        self.flag = True
                    if self.flag:
                        if self.grid[row][column] == 0:
                            self.flag = False
                            self.grid[row][column] = self.grid[row1][cl1]
                            self.grid[row1][cl1] = 0
                            self.addBall(self.randomed[0])
                            self.addBall(self.randomed[1])
                            self.randomColor()
                            self.drawNext()
            self.checkWin()
            self.sec = (int(pygame.time.get_ticks() / 1000))
            self.drawGrid()
            self.drawScore()
            self.drawTime()
            self.drawNext()
            self.checkDefeat()
            pygame.display.flip()

    def initGrid(self):
        for row in range(16):
            self.grid.append([])
            for column in range(15):
                self.grid[row].append(0)
        for x in range(10):
            pass

    def drawGrid(self):
        self.screen.fill(self.background_color)
        for row in range(16):
            for column in range(15):
                pygame.draw.rect(self.screen, self.colors[0],
                                 [(self.margin + self.width) * column + self.margin + 25,
                                  (self.margin + self.height) * row + self.margin + 20,
                                  self.width, self.height])
                if self.grid[row][column] != 0:
                    pos = [((self.margin + self.width) * column + self.margin + 25) + 25,
                           ((self.margin + self.height) * row + self.margin + 20) + 25]
                    pygame.draw.circle(self.screen, self.colors[self.grid[row][column]],
                                       pos, 20)


    def drawScore(self):
        pygame.draw.rect(self.screen, self.colors[0], [860, 150, 200, 600])
        pygame.draw.rect(self.screen, self.background_color, [860, 350, 200, 10])
        message1 = "Wynik :"
        text = self.font2.render(message1, 1, (255, 255, 255))
        self.screen.blit(text, (885, 385))
        text1 = self.font1.render(str(self.score), 1, (255, 255, 255))
        self.screen.blit(text1, (950, 480))

    def drawTime(self):
        if self.sec - ((self.sec // 60) * 60) < 10:
            message = str(self.sec // 60) + ":0" + str(self.sec - ((self.sec // 60) * 60))
        else:
            message = str(self.sec // 60) + ":" + str(self.sec - ((self.sec // 60) * 60))
        message1 = "Czas :"

        text2 = self.font2.render(message1, 1, (255, 255, 255))
        text = self.font1.render(message, 1, (255, 255, 255))
        self.screen.blit(text, (925, 275))
        self.screen.blit(text2, (895, 175))

    def checkDefeat(self):
        counter = 0
        for x in range(16):
            if 0 in self.grid[x]:
                counter += 1
        if counter == 0 or counter == 1:
            self.drawDefeat()
            pygame.display.flip()
            pygame.time.delay(3000)
            exit()

    def drawDefeat(self):
        message = "PRZEGRANA !"
        text = self.font3.render(message, 1, (255, 0, 0))
        self.screen.blit(text, (250, 400))

    def addBall(self, color):
        flag = False
        while not flag:
            row = randint(0, 15)
            column = randint(0, 14)
            if self.grid[row][column] == 0:
                flag = True

        self.grid[row][column] = color

    def startBall(self):
        for x in range(5):
            color = randint(1, 5)
            self.addBall(color)

    def checkWinRight(self):
        for x in range(16):
            counter = 0
            for i in range(14):
                if self.grid[x][i] == self.grid[x][i + 1] and self.grid[x][i] != 0:
                    counter += 1
                else:
                    counter = 0
                if counter == 4:
                    self.play(self.grid[x][i])
                    for j in range(i + 1, i - 4, -1):
                        self.grid[x][j] = 0
                    self.score += 5

    def checkWinDown(self):
        for x in range(15):
            counter = 0
            for i in range(15):
                if self.grid[i][x] == self.grid[i + 1][x] and self.grid[i][x] != 0:
                    counter += 1
                else:
                    counter = 0
                if counter == 4:
                    self.play(self.grid[x][i])
                    for j in range(i + 1, i - 4, -1):
                        self.grid[j][x] = 0
                    self.score += 5

    def checkWinDiagonallyRight(self):
        counter = 0
        for x in range(11):
            for i in range(11):
                if self.grid[x][i] == self.grid[x + 1][i + 1] and self.grid[x][i] != 0:
                    for j in range(4):
                        if self.grid[x + j][i + j] == self.grid[x + j + 1][i + j + 1]:
                            counter += 1
                        else:
                            counter = 0
                    if counter == 4:
                        self.play(self.grid[x][i])
                        for k in range(5):
                            self.grid[x + k][i + k] = 0
                        self.score += 5

    def checkWinDiagonallyLeft(self):
        counter = 0
        for x in range(5, 16):
            for i in range(11):
                if self.grid[x][i] == self.grid[x - 1][i + 1] and self.grid[x][i] != 0:
                    for j in range(4):
                        if self.grid[x - j][i + j] == self.grid[x - j - 1][i + j + 1]:
                            counter += 1
                        else:
                            counter = 0
                    if counter == 4:
                        self.play(self.grid[x][i])
                        for k in range(5):
                            self.grid[x - k][i + k] = 0
                        self.score += 5

    def drawNext(self):
        pygame.draw.rect(self.screen, self.background_color, [860, 550, 200, 10])
        message1 = "Nastepne:"
        text = self.font2.render(message1, 1, (255, 255, 255))
        self.screen.blit(text, (860, 585))
        pygame.draw.circle(self.screen, self.colors[self.randomed[0]],
                           (920, 700), 20)

        pygame.draw.circle(self.screen, self.colors[self.randomed[1]],
                           (1000, 700), 20)

    def randomColor(self):
        self.randomed[0] = randint(1, 5)
        self.randomed[1] = randint(1, 5)

    def play(self, grid):
        if grid == 1:
            self.sound.play()

    def checkWin(self):
        self.checkWinDiagonallyLeft()
        self.checkWinDiagonallyRight()
        self.checkWinRight()
        self.checkWinDown()


if __name__ == "__main__":
    game = MainGame()
