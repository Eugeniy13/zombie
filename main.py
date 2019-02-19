from random import randrange as rnd
from tkinter import *
import math


shoot_prob = 0.25
troop_size = 10
P = 1
P_h = P*0.1/(P+1)
P_z = 0.1/(P+1)



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
colors = ['red', 'cyan', 'green']

a = []
human = []
zombie = []
zombie_waitlist = []

#size_array = [1,2,4,5,8,10,20,40]
#P_array = [0.5, 1, 2]

def starting(): # геренируется начальное положение
    a_point = (1 + P_h - P_z) / (1 - P_h - P_z)
    b_point = (-1 + P_h - P_z) / (1 - P_h - P_z)
    for r in range(N):
        a.append([])
        for c in range(N):
            k = int(rnd(1000)*(a_point - b_point)/1000 + b_point)
            #формула обеспечивает правильное соотношение количества людей к зомби
            a[r].append(k)

# графическое отображение

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

            # да, знаю, лучше было написать функцию, а не копировать почти одикаровые куски кода

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
        elif -1 < x + movement[0] < N and -1 < y + movement[1] < N and (a[x + movement[0]][y + movement[1]] == -1 or a[x + movement[0]][y + movement[1]] == 3):
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

    if 0 < x + movement[0] < N and 0 < y + movement[1] < N:
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

starting()

for y in range(N):
    for x in range(N):
        Cell(x, y)
        # задаем начальную таблицу

human.append(count_human())
zombie.append(count_zombie())
#print(time, human[time], zombie[time])

def main():
    #global t
    #global won
    global time
    #global survived
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
        for y in range(N):
            for x in range(N):
               Cell(x, y)
    elif time > 100 and human[time] == human[time-100]:
        for y in range(N):
            for x in range(N):
                Cell(x, y)
        if human[time] > zombie[time]:
            print('Люди победили!!!!!!!!!!!!!!!!   t = ', time - 100)
            #won = won + 1

        else:
            print('Есть выжившие   t = ', time-100)
            #survived = survived + 1
            #t = time - 100
    elif zombie[time] == 0:
        print('Люди победили!!!!!!!!!!!!!!!!   t = ', time)
        #won = won + 1
        for y in range(N):
            for x in range(N):
                Cell(x, y)
    else:
        for y in range(N):
            for x in range(N):
                Cell(x, y)
        print('time = ',time,'human = ',human[time],'zombie = ', zombie[time])
        #main()
        for y in range(N):
            for x in range(N):
                Cell(x, y)
        root.after(500, main)
        # отрисовка текущей ситуации
'''
    for y in range(N):
        for x in range(N):
            Cell(x, y)
    root.after(300, main)
    # отрисовка текущей ситуации

ggg = 0



result_won = [[[None for k in range(8)] for j in range(10)] for i in range(20)]
result_time = [[[None for k in range(8)] for j in range(10)] for i in range(20)]
result_survived = [[[None for k in range(8)] for j in range(10)] for i in range(20)]

for i in range(5):
    # = i/30
    A = 0.30 + i/50
    shoot_prob = A
    for j in range(3):
        P = P_array[j]
        P_h = P*0.1/(P+1)
        P_z = 0.1/(P+1)
        for k in range(8):
            troop_size = size_array[k]

            starting()
            Sum = 0
            survived = 0
            N_global = 30
            won = 0
            for paralel in range(N_global):
                human.append(count_human())
                zombie.append(count_zombie())
                main()
                Sum = Sum + t
                t = 0
                time = 0
                a = []
                starting()
                human = []
                zombie = []


            won = won / N_global
            survived = survived / N_global
            Sum = Sum / (N_global-won)
            print(A, P_h, P_z, troop_size, Sum, won, survived)
            result_won[i][j][k] = won
            result_time[i][j][k] = Sum

            ggg = ggg + 1
        print(ggg)


f = open('t_time.txt', 'a')

for i in range(20):
    for j in range(10):
        for k in range(8):
            f.write(str(result_time[i][j][k]) + '\n')

f.close()

f = open('t_won.txt', 'a')

for i in range(20):
    for j in range(10):
        for k in range(8):
            f.write(str(result_won[i][j][k]) + '\n')

f.close()

f = open('t_survived.txt', 'a')

for i in range(20):
    for j in range(10):
        for k in range(8):
            f.write(str(result_survived[i][j][k]) + '\n')

f.close()


shoot_prob = 0.26
P_h = 0.06
P_z = 0.04
troop_size = 10

starting()

Sum = 0
survived = 0
N_global = 30
won = 0
human.append(count_human())
zombie.append(count_zombie())
main()

'''

root.after(1800, main)
root.mainloop()

