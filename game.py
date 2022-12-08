import pygame
import time
import numpy as np

class game():
    def __init__(self,broad_size=11,batch_size=32):
        self.broad_size = broad_size
        self.batch_size = batch_size
    def delay(second):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()           
        time.sleep(second)

    def display(self,all_action,p):
        pygame.init()

        DISPLAY_WIDTH = 800
        DISPLAY_HEIGHT = 600

        gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("Draw Shapes")

        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        board_size = 6
        clock = pygame.time.Clock()

        playing = True
        
        while playing:
            for i in range(board_size):
                for j in range(board_size):
                    #pygame.draw.rect(gameDisplay, WHITE, pygame.Rect((10+18*j)+36*i, 100+36*j, 30, 30)) #位於100,100 長度為40
                    pygame.draw.rect(gameDisplay, WHITE, pygame.Rect((10+40*j)+80*i, 100+80*j, 70, 70)) #位於100,100 長度為40
            
            #pygame.draw.circle(gameDisplay, RED, (((10+18*0)+36*0)+15, (100+36*0)+15), 11)
            times=0
            player=-1
            state = np.zeros((board_size,board_size))
            for i in range(len(all_action)):
                pygame.event.get()
                if(player==-1):
                    player=1
                    pygame.draw.circle(gameDisplay, RED, (((10+40*all_action[i][1])+80*all_action[i][0])+34, (100+80*all_action[i][1])+35), 25)
                    state[all_action[i][0]][all_action[i][1]] = 1
                    pygame.time.delay(1500) 
                    pygame.display.update()
                    for j in range(board_size):
                        for k in range(board_size):
                            if(state[j][k])==1:
                                pygame.draw.rect(gameDisplay, WHITE, pygame.Rect((10+40*k)+80*j, 100+80*k, 70, 70))
                                pygame.display.update()
                                pygame.draw.circle(gameDisplay, RED, (((10+40*k)+80*j)+34, (100+80*k)+35), 25)
                                pygame.display.update()
                            elif(state[j][k]==-1):
                                pygame.draw.rect(gameDisplay, WHITE, pygame.Rect((10+40*k)+80*j, 100+80*k, 70, 70))
                                pygame.display.update()
                                pygame.draw.circle(gameDisplay, BLUE, (((10+40*k)+80*j)+34, (100+80*k)+35), 25)
                                pygame.display.update()
                            else:
                                pygame.draw.rect(gameDisplay, WHITE, pygame.Rect((10+40*k)+80*j, 100+80*k, 70, 70))
                                pygame.display.update()
                    pygame.display.update()
                else:
                    player=-1
                    pygame.draw.circle(gameDisplay, BLUE, (((10+40*all_action[i][1])+80*all_action[i][0])+34, (100+80*all_action[i][1])+35), 25)
                    state[all_action[i][0]][all_action[i][1]] = -1
                    for j in range(board_size):
                        for k in range(board_size):
                            myfont = pygame.font.SysFont('cn', 30)
                            p[times][j*6+k] = format(float(p[times][j*6+k]),'.2f')
                            title = myfont.render(str(p[times][j*6+k]), True, GREEN)
                            gameDisplay.blit(title, (((10+40*k)+80*j)+5, (100+80*k)+35))
                    times=times+1
                    pygame.time.delay(1500) 
                    pygame.display.update()
                    pygame.time.delay(1500) 
                    pygame.display.update()

                    
            #pygame.draw.rect(gameDisplay, RED, pygame.Rect(28, 136, 30, 30))
            #pygame.time.delay(1000) 
            #pygame.display.update()
            #pygame.draw.circle(gameDisplay, RED, (28+15, 136+15), 11)
            #pygame.time.delay(1000) 
            pygame.display.update()

            clock.tick(30)

        pygame.quit()
        quit()

