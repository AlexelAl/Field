from tkinter import *
import sys

root = Tk()
root.resizable(0, 0)

rows = 5
cols = 5

pixelVirtual = PhotoImage( width = 1, height = 1 )

# 1. Не ленись дописывать названия. BTN_S - и save и size подходит
BTN_SIZE = 70
field = []

# 2. Состояния должно быть 2, вода это не состояние клетки, на неё должно быть нельзя переключиться просто так.
# 3. Нужна отдельная кнопочка типо начать разлив и тыкать с какой ячейки разлив начинается
status_clr = ['#FFFFFF', '#000000', '#0000FF']
border = [[1,0],[-1,0],[0,1],[0,-1]]

def water(i,j):
    global field
    for k in border:
        newi = i + k[0]
        newj = j + k[1]
        if not(0 > newi or newi >= rows or 0 > newj or newj >= cols) and not field[newi][newj].cell_status == 1:
            field[newi][newj].cell_status = 2
            field[newi][newj]['background'] = status_clr[field[i][j].cell_status]


# 4. Это должно быть методом клетки, т.к. это именно способность клетки менять состояние
def click(c, i, j):
    def r(s):
        # 5. Смену статуса лучше скрыть, Сделать метод типа changeStatus, а расчеты проводить внутри клетки
        field[i][j].cell_status = (field[i][j].cell_status + 1)%3

        # СМ. Внизу
        field[i][j]['background'] = status_clr[field[i][j].cell_status]

        # 6. Это лишнее, см пункт 3
        if field[i][j].cell_status == 2:
            for b in range(rows + cols):
                parse()

    return r

def parse():
    global field, new_w
    new_w = False

    # 7. Не понял зачем выносить функцию в отдельнуб переменную
    funk = water
    for ii in range(rows):
        for jj in range(cols):
            if field[ii][jj].cell_status == 2:
                funk(ii,jj)

def CreateField():
    global field

    # 8. Давай сделаем отдельно кнопку загрузить из файла
    # 9. Плюс хотелось бы выбирать из какого именно файла загружать, т.е. возможность сохранить несколько уровней
    f = open('save.txt', 'r')
    for i in range(rows):
        field.append([])
        for j in range(cols):
            cell = Cell()
            stat = f.read(1)
            if stat == '' or int(stat) > 2:
                stat = '0'
            cell.cell_status = int(stat)

            # СМ. Внизу
            cell['background'] = status_clr[cell.cell_status]
            color = '#FFFF00'

            cell.grid( row = i, column = j, sticky = 'nsew' )
            cell.bind(
                '<Button-1>',
                click(cell,i,j)
            )
            field[i].append( cell )
    f.close()
    SaveBut.grid(row = rows,column = 0, columnspan = 5 ,sticky = 'nsew')

    return field
def save():
    global field
    f = open('save.txt', 'w')
    for i in field:
        for j in i:
            # 10. Лучше добавить разделитель между статусами, вдруг будет больше 10 статусов?
            f.write(str(j.cell_status))
    f.close()
    sys.exit()

class Cell(Button):
    def __init__(self, master = None, **kw):
        kw.update({
            'image': pixelVirtual,
            'width': BTN_SIZE,
            'height': BTN_SIZE,
            'compound': CENTER
        })
        Button.__init__( self, master, kw)
        #0 - empty
        #1 - wall
        #2 - water
        self.cell_status = 0

# 11. Кнопка создается тут, но ставится на месте в функции? странно
SaveBut = Button(text = 'Save and exit',width = 1 ,height=4,bg = '#CCCCCC',command = save)
CreateField()

root.mainloop()


# В целом хорошо, а главное работает!, молодец, скорость у тебя конечно огонь)
# Смотри, я отметил некоторые пункты СМ.ВНИЗУ Все эти пнуты относятся к визуальноя состовляющей.
# Предлагаю разделить визуал и модель.
# Предлагаю, сделать отдельный класс, например app или render или еще что то что ты придумаешь.
# В начале приложения, создавать его, и он будет прорисовывать поле в методе инит.
# А затем либо при смене состояния, либо раз в какое то время например раз в 1000милисекунд / 60 fps
# вызывать его метод update, который будет перерисовывать поле
