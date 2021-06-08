from tkinter import *
import sys

root = Tk()
root.resizable(0, 0)

rows = 5
cols = 5

pixelVirtual = PhotoImage( width = 1, height = 1 )
BTN_S = 70
field = []

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



def click(c, i, j):
    def r(s):
        field[i][j].cell_status = (field[i][j].cell_status + 1)%3
        field[i][j]['background'] = status_clr[field[i][j].cell_status]
        if field[i][j].cell_status == 2:
            for b in range(rows + cols):
                parse()

    return r
def parse():
    global field, new_w
    new_w = False
    funk = water
    for ii in range(rows):
        for jj in range(cols):
            if field[ii][jj].cell_status == 2:
                funk(ii,jj)

def CreateField():
    global field
    f = open('save.txt', 'r')
    for i in range(rows):
        field.append([])
        for j in range(cols):
            cell = Cell()
            stat = f.read(1)
            if stat == '' or int(stat) > 2:
                stat = '0'
            cell.cell_status = int(stat)
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
            f.write(str(j.cell_status))
    f.close()
    sys.exit()

class Cell(Button):
    def __init__(self, master = None, **kw):
        kw.update({
            'image': pixelVirtual,
            'width': BTN_S,
            'height': BTN_S,
            'compound': CENTER
        })
        Button.__init__( self, master, kw)
        #0 - empty
        #1 - wall
        #2 - water
        self.cell_status = 0

SaveBut = Button(text = 'Save and exit',width = 1 ,height=4,bg = '#CCCCCC',command = save)
CreateField()




root.mainloop()
