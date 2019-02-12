from random import randrange as rnd
from tkinter import *
import math

root = Tk()
root.geometry('800x600')

canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)

t = 0
m = 20  # размер ячеек
d = 2  # размер поля вокруг ячейки
N = 40
nr = N  # количество строк
nc = N  # количество столбцов
x0 = m // 2  # отступ от левого края
y0 = m // 2  # отступ от вернего края
colors = ['red', 'yellow', 'cyan', 'green']

a = []
human = []
zombie = []
troop_size = 10
P_h = 0.03
P_z = 0.03

shoot_prob = 0.25

zombie_waitlist = []
a_point = (1 + P_h - P_z)/(1 - P_h - P_z)
b_point = (-1 + P_h - P_z)/(1 - P_h - P_z)

def starting():
    for r in range(N):
        a.append([])
        for c in range(N):
            k = int(rnd(1000)*(a_point - b_point)/1000 + b_point)
            # k = int(rnd(100)/40 - 1.25)
            a[r].append(k)  # начальное положение

starting()

class Cell():

    def __init__(self, r, c):  # при создании указываем номер строки и столбца, в который помещаем
        self.n = rnd(10)  # значение, с которым будем работать
        self.r = r  # Номер сторки в двумерном списке.
        self.c = c  # Номер столбца ...
        if a[r][c] == 0:
            self.color = 'white'
        if a[r][c] == 1:
            self.color = 'green'
        if a[r][c] == -1:
            self.color = 'red'
        if a[r][c] == 5:
            self.color = 'cyan'
        self.id = canv.create_rectangle(-100, 0, -100, 0, fill=self.color)
        self.paint()



    def paint(self):
        x1 = x0 + self.c * m + d
        # рассчитать координаты левого верхнего угла.
        y1 = y0 + self.r * m + d
        # координаты правого нижнего угла.
        x2 = x1 + m - 2 * d  # - r
        y2 = y1 + m - 2 * d
        canv.coords(self.id, x1, y1, x2, y2)
        canv.itemconfig(self.id, fill=self.color)
# графическое отображение

'''
for y in range(N):
    for x in range(N):
        Cell(x, y)
        # задаем начальную таблицу
'''

def count_human():
    c_human = 0
    for y in range(N):
        for x in range(N):
            if a[x][y] == 1:
                c_human = c_human + 1
    return c_human


def count_zombie():
    count_zombie = 0
    for y in range(N):
        for x in range(N):
            if a[x][y] == -1:
                count_zombie = count_zombie + 1
    return count_zombie


def zombie_search(x, y):
    
    le = 1
    found = 0
    nearest_goal = None
    while found == 0 and le < 2*N:
        for i in range(2*le+1):
            if N > x+le > -1 and N > y-le+i > -1 and a[x+le][y-le+i] == 1:
                nearest_goal = [x+le, y-le+i]
                found = 1
            if N > x-le+i > -1 and N > y-le > -1 and a[x-le+i][y-le] == 1:
                nearest_goal = [x-le+i, y-le]
                found = 1
            if N > x-le > -1 and N > y+le-i > -1 and a[x-le][y+le-i] == 1:
                nearest_goal = [x-le, y+le-i]
                found = 1
            if N > x+le-i > -1 and N > y+le > -1 and a[x+le-i][y+le] == 1:
                nearest_goal = [x+le-i, y+le]
                found = 1
        le = le+1
    return nearest_goal
    # поиск ближайшего человека


def human_search(x, y):
    le = 1
    found = 0
    nearest_goal = None
    while found == 0 and le < 3:
        for i in range(2 * le + 1):
            if N > x + le > -1 and N > y - le + i > -1 and a[x + le][y - le + i] == -1:
                nearest_goal = [x + le, y - le + i]
                found = 1
            if N > x - le + i > -1 and N > y - le > -1 and a[x - le + i][y - le] == -1:
                nearest_goal = [x - le + i, y - le]
                found = 1
            if N > x - le > -1 and N > y + le - i > -1 and a[x - le][y + le - i] == -1:
                nearest_goal = [x - le, y + le - i]
                found = 1
            if N > x + le - i > -1 and N > y + 1 > -1 and a[x + le - i][y + 1] == -1:
                nearest_goal = [x + le - i, y + 1]
                found = 1
        le = le + 1
    return nearest_goal
    # поиск ближайшего зомби


def the_end():
    #raise SystemExit
    #print('Ok')
    sarcasm = 1


def zombie_move(x, y):
    global zombie_waitlist
    nearest_goal = zombie_search(x, y)
    if nearest_goal == None:
        the_end()
    elif abs(x - nearest_goal[0]) < 2 and abs(y - nearest_goal[1]) < 2:
        a[nearest_goal[0]][nearest_goal[1]] = 3
    else :
        dist = pow((nearest_goal[0] - x)*(nearest_goal[0] - x) + (nearest_goal[1] - y)*(nearest_goal[1] - y),0.5)
        cos = (nearest_goal[0] - x)/dist
        sin = (nearest_goal[1] - y)/dist
        #move_to = [(nearest_goal[0] - x)/dist),(nearest_goal[1] - y)/dist)]
        #print((nearest_goal[0] - x)/dist,(nearest_goal[1] - y)/dist)
        angl = 0.316
        movement = [0][0]
        if (-angl) < sin < angl:
            if cos > 0:
                movement = [1, 0]
            if cos < 0:
                movement = [-1, 0]
        if (-angl) < cos < angl:
            if sin > 0:
                movement = [0, 1]
            if sin < 0:
                movement = [0, -1]
        if sin > angl and cos > angl:
            movement = [1, 1]
        if sin < (-angl) and cos > angl:
            movement = [1, -1]
        if sin > angl and cos < (-angl):
            movement = [-1, 1]
        if sin < (-angl) and cos < (-angl):
            movement = [-1, -1]

            # обход препятствия
        if a[x + movement[0]][y + movement[1]] == 5 or a[x + movement[0]][y + movement[1]] == 3: #поворот направо
            if movement == [0,1]:
                movement = [1,1]
            elif movement == [1,1]:
                movement = [1,0]
            elif movement == [1,0]:
                movement = [1,-1]
            elif movement == [1,-1]:
                movement = [0,-1]
            elif movement == [0,-1]:
                movement = [-1,-1]
            elif movement == [-1,-1]:
                movement = [-1,0]
            elif movement == [-1,0]:
                movement = [-1,1]
            elif movement == [-1,1]:
                movement = [0,1]

        if 0 < x + movement[0] < N and 0 < y + movement[1] < N:
            if a[x + movement[0]][y + movement[1]] == 5 or a[x + movement[0]][y + movement[1]] == 3: #поворот налево
                if movement == [0,1]:
                    movement = [-1,1]
                elif movement == [1,1]:
                    movement = [0,1]
                elif movement == [1,0]:
                    movement = [1,1]
                elif movement == [1,-1]:
                    movement = [1,0]
                elif movement == [0,-1]:
                    movement = [1,-1]
                elif movement == [-1,-1]:
                    movement = [0,-1]
                elif movement == [-1,0]:
                    movement = [-1,-1]
                elif movement == [-1,1]:
                    movement = [-1,0]

        if 0 < x + movement[0] < N and 0 < y + movement[1] < N:
            if a[x + movement[0]][y + movement[1]] == 5 or a[x + movement[0]][y + movement[1]] == 3: #поворот налево
                if movement == [0,1]:
                    movement = [-1,1]
                elif movement == [1,1]:
                    movement = [0,1]
                elif movement == [1,0]:
                    movement = [1,1]
                elif movement == [1,-1]:
                    movement = [1,0]
                elif movement == [0,-1]:
                    movement = [1,-1]
                elif movement == [-1,-1]:
                    movement = [0,-1]
                elif movement == [-1,0]:
                    movement = [-1,-1]
                elif movement == [-1,1]:
                    movement = [-1,0]

        if 0 < x + movement[0] < N and 0 < y + movement[1] < N:
            if a[x + movement[0]][y + movement[1]] == 5 or a[x + movement[0]][y + movement[1]] == 3: #поворот налево
                if movement == [0,1]:
                    movement = [-1,1]
                elif movement == [1,1]:
                    movement = [0,1]
                elif movement == [1,0]:
                    movement = [1,1]
                elif movement == [1,-1]:
                    movement = [1,0]
                elif movement == [0,-1]:
                    movement = [1,-1]
                elif movement == [-1,-1]:
                    movement = [0,-1]
                elif movement == [-1,0]:
                    movement = [-1,-1]
                elif movement == [-1,1]:
                    movement = [-1,0]

        if 0 < x + movement[0] < N and 0 < y + movement[1] < N:
            if a[x + movement[0]][y + movement[1]] == 5 or a[x + movement[0]][y + movement[1]] == 3: #зеркально
                if movement == [0,1]:
                    movement = [0,-1]
                elif movement == [1,1]:
                    movement = [-1,-1]
                elif movement == [1,0]:
                    movement = [-1,0]
                elif movement == [1,-1]:
                    movement = [-1,1]
                elif movement == [0,-1]:
                    movement = [0,1]
                elif movement == [-1,-1]:
                    movement = [1,1]
                elif movement == [-1,0]:
                    movement = [1,0]
                elif movement == [-1,1]:
                    movement = [1,-1]

        #if -1 < x + movement[0] < N and -1 < y + movement[1] < N and a[x + movement[0]][y + movement[1]] == 5 or a[x + movement[0]][y + movement[1]] == 3:
            #print("stoped")
        if -1 < x + movement[0] < N and -1 < y + movement[1] < N and a[x + movement[0]][y + movement[1]] == 0:
            a[x + movement[0]][y + movement[1]] = 3
            a[x][y] = 0
        elif a[x + movement[0]][y + movement[1]] == -1 or a[x + movement[0]][y + movement[1]] == 3:
            zombie_waitlist.append([x,y])


def friend_search(x,y):
    center = [(int(x/troop_size)*troop_size + int(troop_size/2)), (int(y/troop_size)*troop_size + int(troop_size/2))]
    dist = pow((center[0] - x)*(center[0] - x) + (center[1] - y)*(center[1] - y),0.5)
    if dist == 0:
        return
    cos = (center[0] - x)/dist
    sin = (center[1] - y)/dist
    angl = 0.316
    movement = None
    if (-angl) < sin < angl:
        if cos > 0:
            movement = [1, 0]
        if cos < 0:
            movement = [-1, 0]
    if (-angl) < cos < angl:
        if sin > 0:
            movement = [0, 1]
        if sin < 0:
            movement = [0, -1]
    if sin > angl and cos > angl:
        movement = [1, 1]
    if sin < (-angl) and cos > angl:
        movement = [1, -1]
    if sin > angl and cos < (-angl):
        movement = [-1, 1]
    if sin < (-angl) and cos < (-angl):
        movement = [-1, -1]

    if a[x + movement[0]][y + movement[1]] == 5:  # поворот направо
        if movement == [0, 1]:
            movement = [1, 1]
        elif movement == [1, 1]:
            movement = [1, 0]
        elif movement == [1, 0]:
            movement = [1, -1]
        elif movement == [1, -1]:
            movement = [0, -1]
        elif movement == [0, -1]:
            movement = [-1, -1]
        elif movement == [-1, -1]:
            movement = [-1, 0]
        elif movement == [-1, 0]:
            movement = [-1, 1]
        elif movement == [-1, 1]:
            movement = [0, 1]

    if 0 < x + movement[0] < N and 0 < y + movement[1] < N:
        if a[x + movement[0]][y + movement[1]] == 5:  # поворот налево
            if movement == [0, 1]:
                movement = [-1, 1]
            elif movement == [1, 1]:
                movement = [0, 1]
            elif movement == [1, 0]:
                movement = [1, 1]
            elif movement == [1, -1]:
                movement = [1, 0]
            elif movement == [0, -1]:
                movement = [1, -1]
            elif movement == [-1, -1]:
                movement = [0, -1]
            elif movement == [-1, 0]:
                movement = [-1, -1]
            elif movement == [-1, 1]:
                movement = [-1, 0]

    if 0 < x + movement[0] < N and 0 < y + movement[1] < N:
        if a[x + movement[0]][y + movement[1]] == 5:  # поворот налево
            if movement == [0, 1]:
                movement = [-1, 1]
            elif movement == [1, 1]:
                movement = [0, 1]
            elif movement == [1, 0]:
                movement = [1, 1]
            elif movement == [1, -1]:
                movement = [1, 0]
            elif movement == [0, -1]:
                movement = [1, -1]
            elif movement == [-1, -1]:
                movement = [0, -1]
            elif movement == [-1, 0]:
                movement = [-1, -1]
            elif movement == [-1, 1]:
                movement = [-1, 0]

    if 0 < x + movement[0] < N and 0 < y + movement[1] < N:
        if a[x + movement[0]][y + movement[1]] == 5:  # поворот налево
            if movement == [0, 1]:
                movement = [-1, 1]
            elif movement == [1, 1]:
                movement = [0, 1]
            elif movement == [1, 0]:
                movement = [1, 1]
            elif movement == [1, -1]:
                movement = [1, 0]
            elif movement == [0, -1]:
                movement = [1, -1]
            elif movement == [-1, -1]:
                movement = [0, -1]
            elif movement == [-1, 0]:
                movement = [-1, -1]
            elif movement == [-1, 1]:
                movement = [-1, 0]

    if 0 < x + movement[0] < N and 0 < y + movement[1] < N:
        if a[x + movement[0]][y + movement[1]] == 5:  # зеркально
            if movement == [0, 1]:
                movement = [0, -1]
            elif movement == [1, 1]:
                movement = [-1, -1]
            elif movement == [1, 0]:
                movement = [-1, 0]
            elif movement == [1, -1]:
                movement = [-1, 1]
            elif movement == [0, -1]:
                movement = [0, 1]
            elif movement == [-1, -1]:
                movement = [1, 1]
            elif movement == [-1, 0]:
                movement = [1, 0]
            elif movement == [-1, 1]:
                movement = [1, -1]




    if -1 < x + movement[0] < N and -1 < y + movement[1] < N and a[x + movement[0]][y + movement[1]] == 0:
        a[x + movement[0]][y + movement[1]] = 4
        a[x][y] = 0
    #elif a[x + movement[0]][y + movement[1]] == 1 or a[x + movement[0]][y + movement[1]] == 4:
    #   human_waitlist.append([x,y])


def human_move(x, y):

    nearest_goal = human_search(x, y)
    temp_prob = rnd(1000)/1000
    if nearest_goal is not None:
        if abs(x - nearest_goal[0]) < 2 and abs(y - nearest_goal[1]) < 2:
            if temp_prob < 2*shoot_prob:
                a[nearest_goal[0]][nearest_goal[1]] = 5
        elif temp_prob < shoot_prob:
            a[nearest_goal[0]][nearest_goal[1]] = 5
    else:
        friend_search(x,y)


time = 0

human.append(count_human())
zombie.append(count_zombie())
#print(time, human[time], zombie[time])

def main():
    global time
    time = time + 1

    if time % 2 == 0 :# ход зомби
        zombie_waitlist = []
        for y in range(N):
            for x in range(N):
                if a[x][y] == -1:
                    zombie_move(x, y)
        i = 0
        while i < len(zombie_waitlist):
            zombie_move(zombie_waitlist[i])
            i = i+1
        # первый проход, людей едят

        for y in range(N):
            for x in range(N):
                if a[x][y] == 3:
                    a[x][y] = -1
        # второй проход, люди становятся зомби

    else: # ход людей
        for y in range(N):
            for x in range(N):
                if a[x][y] == 1:
                    human_move(x, y)

        for y in range(N):
            for x in range(N):
                if a[x][y] == 4:
                    a[x][y] = 1
        # второй проход

    human.append(count_human())
    zombie.append(count_zombie())
    #print(time, human[time], zombie[time])
    if human[time] == 0:
        t = time
        print('Конец цивилизации   t = ',time)
    elif time > 50 and human[time] == human[time-50]:
        t = time-50
        print('Есть выжившие   t = ', time-50)
    else:
        main()
        #for y in range(N):
        #    for x in range(N):
        #        Cell(x, y)
        #root.after(300, main)
        # отрисовка текущей ситуации
'''
    for y in range(N):
        for x in range(N):
            Cell(x, y)
    root.after(300, main)
    # отрисовка текущей ситуации
'''
starting()

for paralel in range(10):
    human.append(count_human())
    zombie.append(count_zombie())
    main()
    #print(t)
    t = 0
    time = 0
    a = []
    starting()
    human = []
    zombie = []

#root.after(4000, main)
#root.mainloop()
