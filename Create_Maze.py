import random
import sys
import pygame
from pygame.locals import *

from tkinter import *
from tkinter import messagebox
Tk().wm_withdraw() 

sys.setrecursionlimit(1000000)
maze_Width = 51
maze_Height = 51
StartPoints = []
tile_w = 1050 / maze_Width
global px, py
px = 1
py = 1

#プレイヤーの移動を管理
'''def PlayerControll(key):
    global px, py
    old_x, old_y = px, py
    
    key = pygame.key.get_pressed()
    if key[K_LEFT]:
        px -= 1
    elif key[K_RIGHT]:
        px += 1
    elif key[K_UP]:
        py -= 1
    elif key[K_DOWN]:
        py += 1

    if maze[px][py] == 0:
        px, py = old_x, old_y

    if maze[px][py] == 3: # ゴール?
        messagebox.showinfo("ゴール", "ゴールしました！")
        pygame.quit()
        sys.exit()
        
    maze[old_x][old_y] = 4'''
    
    
# 穴掘りと奇数座標の通路にフラグ立て
def SetPathPoint(x,y):
    maze[x][y] = 1
    if x % 2 == 1 & y % 2 == 1:
        StartPoints.append([x, y])
        
# 座標(x,y)に穴を掘る
def dig(x,y):
    
    while True:
        # 掘ることができる方向を取得
        directions = []
        if maze[x][y-1] == 0:
            if maze[x][y-2] == 0:
                directions.append(1) # Up
        if maze[x][y+1]== 0:
            if maze[x][y+2] == 0:
                directions.append(2) # Down
        if maze[x-1][y] == 0:
            if maze[x-2][y] == 0:
                directions.append(3) # Left
        if maze[x+1][y] == 0:
            if maze[x+2][y] == 0:
                directions.append(4) # Right
        
        # どの方向にも掘ることができなければbreak
        if(len(directions) == 0):
            break
        
        maze[1][1] = 2
        
        #得られた移動方向から１つ選ぶ
        Directions = random.choice(directions)
        #指定方向に穴掘り
        if Directions == 1:
            maze[x][y-1] = 1
            SetPathPoint(x,y-2)
            y -= 2
        elif Directions == 2:
            maze[x][y+1] = 1
            SetPathPoint(x,y+2)
            y += 2
        elif Directions == 3:
            maze[x-1][y] = 1
            SetPathPoint(x-2,y)
            x -= 2
        else:
            maze[x+1][y] = 1
            SetPathPoint(x+2,y)
            x += 2
            
    # StartPointの候補がなければNoneを返す
    if len(StartPoints) == 0:
        Point = None
    else:
    # StartPointsから１つStartPointを選ぶ
        num = random.randint(0, len(StartPoints) - 1)
        Point = StartPoints.pop(num) # 値をランダムに１つ取得し該当要素を削除
    
    if Point != None:
        X = Point[0]
        Y = Point[1]
        dig(X, Y)

maze = [[0 for j in range (maze_Height)] for i in range(maze_Width)] # 壁を生成

 #外壁を通路にする
for n in range(maze_Height):
    maze[0][n] = 1
    maze[maze_Width - 1][n] = 1
    n += 1
    
for m in range(maze_Width):
    maze[m][0] = 1
    maze[m][maze_Height - 1] = 1
    m += 1 

dig(1, 1)

#外壁を壁に戻す
for n in range(maze_Height):
    maze[0][n] = 0
    maze[maze_Width - 1][n] = 0
    n += 1
    
for m in range(maze_Width):
    maze[m][0] = 0
    maze[m][maze_Height - 1] = 0
    m += 1 
maze[maze_Width - 2][maze_Height - 2] = 3
        
# pygame関連
pygame.init()
screen = pygame.display.set_mode((tile_w * maze_Width, tile_w * maze_Height))
white = (255, 255, 255)
brown = (62, 46, 40)
blue = (0, 103, 192)
red = (179, 66, 74)
green = (77, 181, 106)
mazeColor = [brown, white, blue, red, green]

screen.fill(brown)
while True:
    pygame.draw.circle(screen, red, (px * tile_w + tile_w / 2, py * tile_w + tile_w / 2), tile_w / 2) # 円を描画
    
    old_x, old_y = px, py
    
    #プレイヤーの移動を管理
    key = pygame.key.get_pressed()
    if key[K_LEFT]:
        px -= 1
    elif key[K_RIGHT]:
        px += 1
    elif key[K_UP]:
        py -= 1
    elif key[K_DOWN]:
        py += 1

    if maze[px][py] == 0:
        px, py = old_x, old_y

    if maze[px][py] == 3: # ゴール?
        messagebox.showinfo("ゴール", "ゴールしました！！")
        pygame.quit()
        sys.exit()
        
    maze[old_x][old_y] = 4
    
    pygame.display.update()
    pygame.time.wait(80)
    
    for y in range(0, maze_Height):
        for x in range(0, maze_Width):
            v = maze[x][y]
            xx = tile_w * x
            yy = tile_w * y
            pygame.draw.rect(screen, mazeColor[v], (xx, yy ,xx + tile_w, yy + tile_w)) #タイルに変換
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

