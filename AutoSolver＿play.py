import time
import random
import sys
import pygame
from pygame.locals import *

from tkinter import *
from tkinter import messagebox
Tk().wm_withdraw() 

sys.setrecursionlimit(1000000)
mazesize = {"e":27, "n":51, "h":81, "vh":141, "g":201, "sg":301} #辞書型で迷路のサイズを管理


dificulty= "h" #ここを書き換えてください（難易度）


maze_Width = mazesize[dificulty]
maze_Height = mazesize[dificulty]
StartPoints = []
tile_w = 1000 / maze_Width
px = 1
py = 1
changed_tiles = []
white = (255, 255, 255)
brown = (62, 46, 40)
blue = (0, 103, 192)
red = (179, 66, 74)
green = (77, 181, 106)

maze = [[0 for j in range (maze_Height)] for i in range(maze_Width)] # 壁を生成
screen = pygame.display.set_mode((tile_w * maze_Width, tile_w * maze_Height))


#変更のあるタイルのみを配列に追加
def change_tile(x,y,new_value):
    maze[x][y] = new_value
    changed_tiles.append([x,y])
    
#変更のあるタイルのみを更新
def draw_changed_tiles():
    for x, y in changed_tiles:
        font1 = pygame.font.SysFont(None, int(tile_w / 2))
        text1 = font1.render(f"{maze[x][y] - 9}", True, (0,0,0))
        mazeColor = [brown, white, blue, red, green,red]
        v = maze[x][y]
        xx = tile_w * x
        yy = tile_w * y
        if v < 6:
            pygame.draw.rect(screen, mazeColor[v], (xx, yy ,tile_w+1, tile_w+1))
        '''else:
            pygame.draw.rect(screen, blue, (xx, yy ,tile_w+1, tile_w+1))
            screen.blit(text1, (xx, yy ,xx + tile_w, yy + tile_w)) #探索済みを青く着色'''
            
    changed_tiles.clear()
    

def MazeExproler():
    steps = 10 #あとで9引く
    notgorl = True
    queue = [[px,py]]
    
    #探索待ちの列がなくなるまで探索を続ける
    while((len(queue) != 0) & notgorl):
        #探索対象の座標を取得
        targetPoint = queue.pop(0)
        x = targetPoint[0]
        y = targetPoint[1]
        
        change_tile(x, y, steps)#探索ずみをフラグ
        
        if maze[x][y-1] == 1 or maze[x][y-1] == 3 or maze[x][y-1] == 4:
            queue.append([x,y-1])
        if maze[x][y+1]== 1 or maze[x][y+1]== 3 or maze[x][y+1] == 4:
            queue.append([x,y+1])
        if maze[x-1][y] == 1 or maze[x-1][y] == 3 or maze[x-1][y] == 4:
            queue.append([x-1,y])
        if maze[x+1][y] == 1 or maze[x+1][y] == 3 or maze[x+1][y] == 4:
            queue.append([x+1,y])
        
        if x == maze_Height - 2 and y == maze_Width - 2:
            change_tile(x, y, steps)
            SetGorlRoute()
            notgorl = False
            queue.clear
            break
            
        steps += 1
        
def SetGorlRoute():
    mazescore = maze[maze_Width - 2][maze_Height - 2]
    reverseRoute = []
    count = 0
    x = maze_Width - 2
    y = maze_Height - 2
    while True:
        if maze[x-1][y] < mazescore and maze[x-1][y]  > 9:
            mazescore = maze[x-1][y]
            reverseRoute.append([x-1,y])
            x = x-1
            count += 1
        elif maze[x+1][y] < mazescore and maze[x+1][y]  > 9:
            mazescore = maze[x+1][y]
            reverseRoute.append([x+1,y])
            x=x+1
            count += 1
        elif maze[x][y-1] < mazescore and maze[x][y-1]  > 9:
            mazescore = maze[x][y-1]
            reverseRoute.append([x,y-1])
            y=y-1
            count += 1
        elif maze[x][y+1] < mazescore and maze[x][y+1]  > 9:
            mazescore = maze[x][y+1]
            reverseRoute.append([x,y+1])
            y=y+1
            count += 1
            
        if (x == px) & (y == py):
            for n in range(count):
                ReverseRoute = reverseRoute[n]
                Rx = ReverseRoute[0]
                Ry = ReverseRoute[1]
                change_tile(Rx,Ry,5)
                change_tile(maze_Width - 2,maze_Height - 2,3)
            break 
    
    
    
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
    
        
                
                
def main():
    global px
    global py
    global maze
    
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
    maze[maze_Width - 2][maze_Height - 2] = 3 #Gorlを設定

    # pygame関連
    pygame.init()

    screen.fill(brown)

    for y in range(0, maze_Height):
            for x in range(0, maze_Width):
                font1 = pygame.font.SysFont(None, int(tile_w / 2))
                text1 = font1.render(f"{maze[x][y] - 9}", True, (0,0,0))
                v = maze[x][y]
                mazeColor = [brown, white, blue, red, green,red]
                xx = tile_w * x
                yy = tile_w * y
                if v < 6:
                    pygame.draw.rect(screen, mazeColor[v], (xx, yy ,xx + tile_w, yy + tile_w)) #タイルに変換
                else:
                    pygame.draw.rect(screen, blue, (xx, yy ,xx + tile_w, yy + tile_w))
                    screen.blit(text1, (xx, yy ,xx + tile_w, yy + tile_w))
                    
    start_time = time.time()
        
    while True:
        pygame.draw.circle(screen, red, (px * tile_w + tile_w / 2, py * tile_w + tile_w / 2), tile_w / 2) # 円を描画
        
        old_x, old_y = px, py
        
        key = pygame.key.get_pressed()
        if key[K_LEFT]:
            px -= 1
            change_tile(old_x, old_y, 4)
        elif key[K_RIGHT]:
            px += 1
            change_tile(old_x, old_y, 4)
        elif key[K_UP]:
            py -= 1
            change_tile(old_x, old_y, 4)
        elif key[K_DOWN]:
            py += 1
            change_tile(old_x, old_y, 4)
        elif key[K_0]:
            MazeExproler()
        elif key[K_x]:
            change_tile(px,py,2)
            TelPoint = [old_x, old_y]
        elif key[K_1]:
            px, py = TelPoint
            change_tile(old_x, old_y, 4)
            draw_changed_tiles()
        elif key[K_s]:
            change_tile(old_x, old_y, 4)
            draw_changed_tiles()
            px, py = 1, 1
            
        if maze[px][py] == 0:
            px, py = old_x, old_y

        if maze[px][py] == 3: # ゴール?
            end_time = time.time()
            time_dif = end_time - start_time
            
            messagebox.showinfo("ゴール", "ゴールしました！！\nタイム:" + str(round(time_dif,2)) + "秒")
            pygame.quit()
            sys.exit()
            
        pygame.display.update()
        pygame.time.wait(80)
        
        draw_changed_tiles()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

main()