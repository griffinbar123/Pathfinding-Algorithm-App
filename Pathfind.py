import math
import pygame as pg
import sys
import random

from collections import OrderedDict 

pg.init()


info = pg.display.Info()
# WIDTH, HEIGHT = info.current_w, info.current_h-100
WIDTH, HEIGHT = 800, 600
bwidth = 0.5
rectsizex = 13
rectsizey = 13
totalrow = int((HEIGHT)/rectsizex)
totalcolumns = int((WIDTH)/rectsizey)
startrow = 0
startcol = 0
endrow = 0
endcol = 0
visited = []
totalwidth = totalcolumns*rectsizex+200
display = pg.display.set_mode((totalcolumns*rectsizex+200, totalrow*rectsizex))
pg.display.set_caption("A* Pathfinding Program")
sys.setrecursionlimit(6000)
font = pg.font.SysFont('Comic Sans MS', 15, bold=True)
sfont = pg.font.SysFont('Comic Sans MS', 11, bold=True)
acheck = False
startcheck = False
endcheck = False
clock = pg.time.Clock()
bcheck = False
dcheck = False
tickspeed = 60

class Node: 
    def __init__(self):
        super().__init__()
        self.neighbors = []
        self.gcost = 0
        self.hcost = 0
        self.fcost = 0
        self.obs = False
        self.parentsrow = -1
        self.parentscol = -1
        self.value = 1
        self.x = 0
        self.y = 0
        self.row = 0
        self.col = 0
        self.typ = "empty"
        self.check = False
        self.visited = False
        self.start = False
        self.end= False

    def isblack(self):
        self.obs = True
        self.typ = "black"
        self.rect()
        self.start = False
        self.end= False
        return True   
    
    def isempty(self):
        self.typ = "empty"
        self.rect()
        self.start = False
        self.end= False
        global startcheck
        startcheck = False
        global endcheck
        endcheck = False
        self.visited = False
        self.check = False
        return True
    
    def isgreen(self):
        self.typ = "green"
        self.rect()
        self.start = True
        global startcheck
        startcheck = True
        global startt
        startt= cells[self.row][self.col]
        self.obs = False
        return True
    
    def isred(self):
        self.typ = "red"
        self.rect()
        self.end = True
        global endcheck
        endcheck = True
        self.obs = False
        return True;  
    
    def isblue(self):
        self.typ = "blue"
        self.rect()
        return True
    
    def isorange(self):
        self.typ = "orange"
        self.rect()
        return True
    
    def ispink(self):
        self.typ = "pink"
        self.rect()
        return True
    
    def isaqua(self):
        self.typ = "aqua"
        self.rect()
        return True
    
    def isslightor(self):
        self.typ = "slightor"
        self.rect()
        return True
    
    def addneighbors(self, cells):
        if(self.row == 0 and self.col == 0):
            self.neighbors.append(cells[self.row][self.col+1])
            self.neighbors.append(cells[self.row+1][self.col+1])
            self.neighbors.append(cells[self.row+1][self.col])
        elif(self.row == 0 and self.col == totalcolumns - 1):
            self.neighbors.append(cells[self.row][self.col-1])
            self.neighbors.append(cells[self.row+1][self.col-1])
            self.neighbors.append(cells[self.row+1][self.col])
        elif(self.row == 0):
            self.neighbors.append(cells[self.row][self.col+1])
            self.neighbors.append(cells[self.row+1][self.col+1])
            self.neighbors.append(cells[self.row+1][self.col])
            self.neighbors.append(cells[self.row][self.col-1])
            self.neighbors.append(cells[self.row+1][self.col-1])
        elif(self.row == totalrow-1 and self.col == 0):
            self.neighbors.append(cells[self.row][self.col+1])
            self.neighbors.append(cells[self.row-1][self.col+1])
            self.neighbors.append(cells[self.row-1][self.col])
        elif (self.row == totalrow-1 and self.col == totalcolumns-1):
            self.neighbors.append(cells[self.row][self.col-1])
            self.neighbors.append(cells[self.row-1][self.col-1])
            self.neighbors.append(cells[self.row-1][self.col])
        elif (self.row == totalrow - 1):
            self.neighbors.append(cells[self.row][self.col+1])
            self.neighbors.append(cells[self.row-1][self.col+1])
            self.neighbors.append(cells[self.row-1][self.col])
            self.neighbors.append(cells[self.row][self.col-1])
            self.neighbors.append(cells[self.row-1][self.col-1])
        elif (self.col == 0):
            self.neighbors.append(cells[self.row][self.col+1])
            self.neighbors.append(cells[self.row-1][self.col])
            self.neighbors.append(cells[self.row+1][self.col])
        elif (self.col == totalcolumns-1):
            self.neighbors.append(cells[self.row][self.col-1])
            self.neighbors.append(cells[self.row-1][self.col])
            self.neighbors.append(cells[self.row+1][self.col])
        else:   
            self.neighbors.append(cells[self.row][self.col+1])
            self.neighbors.append(cells[self.row][self.col-1])
            self.neighbors.append(cells[self.row-1][self.col])
            self.neighbors.append(cells[self.row+1][self.col])
            
    def rect(self):
        if (self.typ == "closed"):
            rec = pg.Rect(self.x, self.y, rectsizex, rectsizex)
            pg.draw.rect(display, (0, 0, 0), rec)
            rec2 = pg.Rect(self.x+.5, self.y+.5, rectsizex-1, rectsizex-1)
            pg.draw.rect(display, (0, 0, 0), rec2)
        if (self.typ == "empty"):
            self.obs = False
            rec = pg.Rect(self.x, self.y, rectsizex, rectsizex)
            pg.draw.rect(display, (0, 0, 0), rec)
            rec2 = pg.Rect(self.x+.5, self.y+.5, rectsizex-1, rectsizex-1)
            pg.draw.rect(display, (250,250,250), rec2)
        elif (self.typ == "black"):
            self.obs = True
            rec = pg.Rect(self.x, self.y, rectsizex, rectsizex)
            pg.draw.rect(display, (0, 0, 0), rec)
            rec2 = pg.Rect(self.x+.5, self.y+.5, rectsizex-1, rectsizex-1)
            pg.draw.rect(display, (0, 0, 0), rec2)
        elif (self.typ == "green"):
            rec = pg.Rect(self.x, self.y, rectsizex, rectsizex)
            pg.draw.rect(display, (0, 0, 0), rec)
            rec2 = pg.Rect(self.x+.5, self.y+.5, rectsizex-1, rectsizex-1)
            pg.draw.rect(display, (0, 250, 0), rec2)
        elif (self.typ == "red"):
            rec = pg.Rect(self.x, self.y, rectsizex, rectsizex)
            pg.draw.rect(display, (0, 0, 0), rec)
            rec2 = pg.Rect(self.x+.5, self.y+.5, rectsizex-1, rectsizex-1)
            pg.draw.rect(display, (250, 0, 0), rec2)
        elif (self.typ == "blue"):
            rec = pg.Rect(self.x, self.y, rectsizex, rectsizex)
            pg.draw.rect(display, (0, 0, 0), rec)
            rec2 = pg.Rect(self.x+.5, self.y+.5, rectsizex-1, rectsizex-1)
            pg.draw.rect(display, (0, 0, 250), rec2)
        elif (self.typ == "orange"):
            rec = pg.Rect(self.x, self.y, rectsizex, rectsizex)
            pg.draw.rect(display, (0, 0, 0), rec)
            rec2 = pg.Rect(self.x+.5, self.y+.5, rectsizex-1, rectsizex-1)
            pg.draw.rect(display, (255, 209, 0), rec2)
        elif (self.typ == "slightor"):
            rec = pg.Rect(self.x, self.y, rectsizex, rectsizex)
            pg.draw.rect(display, (0, 0, 0), rec)
            rec2 = pg.Rect(self.x+.5, self.y+.5, rectsizex-1, rectsizex-1)
            pg.draw.rect(display, (25, 20, 0), rec2)
        elif (self.typ == "pink"):
            rec = pg.Rect(self.x, self.y, rectsizex, rectsizex)
            pg.draw.rect(display, (0, 0, 0), rec)
            rec2 = pg.Rect(self.x+.5, self.y+.5, rectsizex-1, rectsizex-1)
            pg.draw.rect(display, (230, 69, 210), rec2)
        elif (self.typ == "aqua"):
            rec = pg.Rect(self.x, self.y, rectsizex, rectsizex)
            pg.draw.rect(display, (0, 0, 0), rec)
            rec2 = pg.Rect(self.x+.5, self.y+.5, rectsizex-1, rectsizex-1)
            pg.draw.rect(display, (41, 234, 255), rec2)
        return 0

startt = Node()
endd = Node()

def distance(one, two):
    dis = math.sqrt(pow((one.x - two.x), 2) + pow((one.y - two.y), 2))
    return dis
def partition(arr, low, high):
    i = (low-1)        
    pivot = arr[high]     
    for j in range(low, high):
        if arr[j].fcost <= pivot.fcost:
            i = i+1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return (i+1)
  
def quickSort(arr, low, high):
    if len(arr) == 1:
        return arr
    if low < high:
        pi = partition(arr, low, high)
        quickSort(arr, low, pi-1)
        quickSort(arr, pi+1, high)


def getparent(current):
    parent = cells[current.parentsrow][current.parentscol]
    return parent

def deleterepeats(arr):
    arr2 = list(OrderedDict.fromkeys(arr))
    return arr2
                
def GetShortestPath(end):
    Shortestpat = []
    current = end
    while(True):
        Shortestpat.insert(0, current)
        if (current.parentscol == -1):
            break
        current = getparent(current)
    Shortestpat.pop(0)
    return Shortestpat


opened = set()
done = False

def GetShortestPathb(end, start):
    Shortestpat = []
    current = end
    while(True):
        Shortestpat.insert(0, current)
        if (current.parentscol == start.col and current.parentsrow == start.row):
            break
        current = getparent(current)
    Shortestpat.pop(-1)
    return Shortestpat

def breadthfirst(node, end):
    q = []
    q.append(node)
    while len(q)>0:
        x = q[0]
        q.pop(0)
        if x.typ == "empty":
            x.isorange()
        if x.visited == False:
            x.visited = True
            x.addneighbors(cells)
            for neighbor in x.neighbors:
                if neighbor.obs == True:
                    continue
                if neighbor in q:
                    continue
                if(neighbor.row == end.row and neighbor.col == end.col):
                    neighbor.parentsrow = x.row
                    neighbor.parentscol = x.col
                    j = GetShortestPathb(end, node)
                    for k in j:
                        k.isblue()
                    return j
                if neighbor.visited == False:
                    q.append(neighbor)
                if neighbor.typ =="empty":
                    neighbor.parentsrow = x.row
                    neighbor.parentscol = x.col
        
    return q

def disbreadthfirst(node, end):
    q = []
    j= []
    temp = []
    q.append(node)
    while len(q)>0:
        x = q[0]
        q.pop(0)
        if x.visited == False:
            temp.append(x)
            x.visited = True
            x.addneighbors(cells)
            for neighbor in x.neighbors:
                if neighbor.obs == True:
                    continue
                if neighbor in q:
                    continue
                if(neighbor.row == end.row and neighbor.col == end.col):
                    neighbor.parentsrow = x.row
                    neighbor.parentscol = x.col
                    j = GetShortestPathb(end, node)
                    temp.pop(0)
                    return j, temp
                if neighbor.visited == False:
                    q.append(neighbor)
                if neighbor.typ =="empty" and neighbor.visited == False:
                    neighbor.parentsrow = x.row
                    neighbor.parentscol = x.col
    temp.pop(0)
    return j, temp

            

def dodepth(opened, node, end):
    global done
    if not done:
        if node not in opened:
            if node.typ is not "green":
                    node.isaqua()
            opened.add(node)
            node.addneighbors(cells)
            for neighbor in node.neighbors:
                if neighbor.obs == True:
                    continue
                if neighbor in opened:
                    continue
                if(neighbor.row == end.row and neighbor.col == end.col):
                    done = True
                    return opened
                dodepth(opened, neighbor, end)



def A(start, end):
    ope = [start]
    closed = []
    current = Node()
    while(len(ope)>0):
        quickSort(ope, 0, len(ope)-1)
        current = ope[0]
        ope.pop(0)
        current.addneighbors(cells)
        for neighbor in current.neighbors:
            if (neighbor.typ == "empty"):
                neighbor.tag="path"
                neighbor.ispink()
            closedlower = True
            openlower = True
            if (neighbor.obs == True):
                continue

            neighbor.gcost = distance(current, neighbor)
            neighbor.value = distance(start, neighbor)
            neighbor.hcost = distance(neighbor, end)
            neighbor.fcost = neighbor.gcost + neighbor.hcost
            if(neighbor.row == end.row and neighbor.col == end.col):
                closed.append(current)
                closed.pop(0)
                path = GetShortestPath(closed[-1])
                for l in path:
                    l.isblue()
                return path
            for j in ope:
                if(neighbor.row == j.row and neighbor.col == j.col and j.value <= neighbor.value):
                    openlower = False

            
            for j in closed:
                if(neighbor.row == j.row and neighbor.col == j.col and j.value >= neighbor.value):
                    closedlower = False
                
            
            if (closedlower and openlower):
                    neighbor.parentsrow = current.row
                    neighbor.parentscol = current.col
                    ope.append(neighbor)
            start.parentscol = -1
        if len(closed)>0:
            current.isaqua()
        closed.append(current)
    path = GetShortestPath(closed[-1])
    return closed

def decA(start, end):
    ope = [start]
    closed = []
    current = Node()
    pink = []
    path = []
    while(len(ope)>0):
        quickSort(ope, 0, len(ope)-1)
        current = ope[0]
        ope.pop(0)
        current.addneighbors(cells)
        for neighbor in current.neighbors:
            if (neighbor.typ == "empty"):
                neighbor.tag="path"
                pink.append(neighbor)
            closedlower = True
            openlower = True
            if (neighbor.obs == True):
                continue

            neighbor.gcost = distance(current, neighbor)
            neighbor.value = distance(start, neighbor)
            neighbor.hcost = distance(neighbor, end)
            neighbor.fcost = neighbor.gcost + neighbor.hcost
            if(neighbor.row == end.row and neighbor.col == end.col):
                closed.append(current)
                closed.pop(0)
                path = GetShortestPath(closed[-1])
                return path, pink, closed
            for j in ope:
                if(neighbor.row == j.row and neighbor.col == j.col and j.value <= neighbor.value):
                    openlower = False

            
            for j in closed:
                if(neighbor.row == j.row and neighbor.col == j.col and j.value >= neighbor.value):
                    closedlower = False
                
            
            if (closedlower and openlower):
                    neighbor.parentsrow = current.row
                    neighbor.parentscol = current.col
                    ope.append(neighbor)
            start.parentscol = -1
        closed.append(current)
    path = GetShortestPath(closed[-1])
                # closed.pop(0)
    return path, pink, closed
#functions to check if, when a button is pressed, what should happen to a specfic node or what algorithm should it call
def startpressed():
    x, y = pg.mouse.get_pos()
    startrow = int(y/rectsizex)
    startcol = int(x/rectsizey)
    if cells[startrow][startcol] != endd and cells[startrow][startcol] != cells[endd.row-1][endd.col] and cells[startrow][startcol] != cells[endd.row+1][endd.col] and cells[startrow][startcol] != cells[endd.row][endd.col-1] and cells[startrow][startcol] != cells[endd.row][endd.col+1]:
        global startt 
        startt = cells[startrow][startcol]
        cells[startrow][startcol].isgreen()
def endpressed():
    x, y = pg.mouse.get_pos()
    endrow= int(y/rectsizex)
    endcol= int(x/rectsizey)
    if cells[endrow][endcol] != startt and cells[endrow][endcol] != cells[startt.row-1][startt.col] and cells[endrow][endcol] != cells[startt.row+1][startt.col] and cells[endrow][endcol] != cells[startt.row][startt.col-1] and cells[endrow][endcol] != cells[startt.row][startt.col+1]:
        global endd 
        endd = cells[endrow][endcol]
        cells[endrow][endcol].isred()
        global done
        done = False
def wall():
    x, y = pg.mouse.get_pos()
    temprow = int(y/rectsizex)
    tempcol = int(x/rectsizey)
    cells[temprow][tempcol].isblack()
def goA():
    global acheck
    acheck = True
    path =A(startt, endd)
    return path
def godecA():
    global acheck
    acheck = True
    path, pink, closed =decA(startt, endd)
    return path, pink, closed

def godepth():
    global opened
    opened = set()
    global dcheck
    dcheck = True
    global done
    done = False
    path =dodepth(opened, startt, endd)
    return path

def gobreadth():
    global bcheck
    bcheck = True
    startt.visited = False
    endd.visited = False
    path =breadthfirst(startt, endd)
    return path 

def disgobreadth():
    global bcheck
    bcheck = True
    startt.visited = False
    endd.visited = False
    path, route =disbreadthfirst(startt, endd)
    return path, route

def gotwo():
    path =walls(startt, endd)
    return path;     
            
def delete():
    global acheck
    acheck = False
    global done
    done = False
    global opened
    global dcheck
    dcheck = False
    global bcheck
    bcheck = False
    opened = set()
    for cellrow in cells:
        for cell in cellrow:
            cell.isempty()
            cell.check = False
            cell.visited = False

def pathdelete():
    global acheck
    acheck = False
    global done
    done = False
    global opened
    global dcheck
    dcheck = False
    global bcheck
    bcheck = False
    opened = set()
    for cellrow in cells:
        for cell in cellrow:
            if cell.typ != "black":
                cell.isempty()
                cell.check = False
                cell.visited = False

def onlypathdelete():
    global acheck
    acheck = False
    global done
    done = False
    global opened
    global dcheck
    dcheck = False
    global bcheck
    bcheck = False
    global opened
    opened = set()
    for cellrow in cells:
        for cell in cellrow:
            if cell.typ != "black" and cell.typ != "red" and cell.typ != "green" :
                cell.isempty()
                cell.check = False
                cell.visited = False

def erase():
    x, y = pg.mouse.get_pos()
    temprow = int(y/rectsizex)
    tempcol = int(x/rectsizey)
    cells[temprow][tempcol].isempty()

def generate():
    global acheck
    acheck = False
    global done
    done = False
    global opened
    global dcheck
    dcheck = False
    global bcheck
    bcheck = False
    global opened
    opened = set()
    for i in cells:
        for j in i:
            randnum = random.randint(1, 100)
            if randnum < 40:
                j.isblack()
            else:
                j.isempty()

class sidebar():
    def __init__(self):
        global totalwidth
        self.hite = totalrow*rectsizex
        self.witdh = 200
        self.sx = totalcolumns*rectsizex
        self.sy = 0
        self.base = pg.Rect(self.sx, self.sy, self.witdh, self.hite)
        pg.draw.rect(display, (233, 233, 233), self.base)

        self.text = font.render("Visualize Path: " , False, (0, 0, 0), (233, 233, 233))
        display.blit(self.text, [totalcolumns*rectsizex+5, self.hite-35])
        self.gorect = pg.Rect(totalwidth - 60, self.hite-35, 20, 20)
        self.go2rect = pg.Rect(totalwidth - 60, self.hite-35, 20, 20)



        self.text2 = font.render("Pick Algorithm " , False, (0, 0, 0), (233, 233, 233))
        display.blit(self.text2, [totalcolumns*rectsizex+40, 13])
        self.textsmall = sfont.render("(right click to deselect)" , False, (0, 0, 0), (233, 233, 233))
        display.blit(self.textsmall, [totalcolumns*rectsizex+26, 29])


        self.text3 = font.render("A*: " , False, (0, 0, 0), (233, 233, 233))
        display.blit(self.text3, [totalcolumns*rectsizex+17, 45])
        self.Arect = pg.Rect(totalwidth - 50, 46, 20, 20)
        self.A2rect = pg.Rect(totalwidth - 50, 46, 20, 20)
    

        self.text4 = font.render("Breadth-First: " , False, (0, 0, 0), (233, 233, 233))
        display.blit(self.text4, [totalcolumns*rectsizex+17, 70])
        self.Brect = pg.Rect(totalwidth - 50, 71, 20, 20)
        self.B2rect = pg.Rect(totalwidth - 50, 71, 20, 20)

        self.text5 = font.render("Depth-First: " , False, (0, 0, 0), (233, 233, 233))
        display.blit(self.text5, [totalcolumns*rectsizex+17, 95])
        self.Drect = pg.Rect(totalwidth - 50, 96, 20, 20)
        self.D2rect = pg.Rect(totalwidth - 50, 96, 20, 20)

        pg.draw.line(display, (0,0,0), (self.sx, 130), (self.sx+200, 130))


        self.text6 = font.render("Delete Everything: " , False, (0, 0, 0), (233, 233, 233))
        display.blit(self.text6, [totalcolumns*rectsizex+5, 140])
        self.ddrect = pg.Rect(totalwidth - 30, 141, 20, 20)
        self.dd2rect = pg.Rect(totalwidth - 30, 141, 20, 20)


        self.text7 = font.render("Keep only walls: " , False, (0, 0, 0), (233, 233, 233))
        display.blit(self.text7, [totalcolumns*rectsizex+5, 165])
        self.prect = pg.Rect(totalwidth - 30, 166, 20, 20)
        self.p2rect = pg.Rect(totalwidth - 30, 166, 20, 20)

        self.text8 = font.render("Delete only path: " , False, (0, 0, 0), (233, 233, 233))
        display.blit(self.text8, [totalcolumns*rectsizex+5, 190])
        self.porect = pg.Rect(totalwidth - 30, 191, 20, 20)
        self.po2rect = pg.Rect(totalwidth - 30, 191, 20, 20)
        

        pg.draw.line(display, (0,0,0), (self.sx, 225), (self.sx+200, 225))

        self.text9 = font.render("Random walls: " , False, (0, 0, 0), (233, 233, 233))
        display.blit(self.text9, [totalcolumns*rectsizex+5, 235])
        self.wrect = pg.Rect(totalwidth - 30, 236, 20, 20)
        self.w2rect = pg.Rect(totalwidth - 30, 236, 20, 20)


        pg.draw.line(display, (0,0,0), (self.sx, 275), (self.sx+200, 275))

        text11 = font.render("Hit 'S' when mouse over " , False, (0, 0, 0), (233, 233, 233))
        display.blit(text11, [totalcolumns*rectsizex+2, 290])
        text12 = font.render("desired node to turn it " , False, (0, 0, 0), (233, 233, 233))
        display.blit(text12, [totalcolumns*rectsizex+2, 310])
        text13 = font.render("into start node. Hit 't' " , False, (0, 0, 0), (233, 233, 233))
        display.blit(text13, [totalcolumns*rectsizex+2, 330])
        text14 = font.render("to turn it into target " , False, (0, 0, 0), (233, 233, 233))
        display.blit(text14, [totalcolumns*rectsizex+2, 350])
        text15 = font.render("node. Hit 'e' to turn " , False, (0, 0, 0), (233, 233, 233))
        display.blit(text15, [totalcolumns*rectsizex+2, 370])
        text16 = font.render("node empty. Hit 'w' to " , False, (0, 0, 0), (233, 233, 233))
        display.blit(text16, [totalcolumns*rectsizex+2, 390])
        text16 = font.render("draw wall. " , False, (0, 0, 0), (233, 233, 233))
        display.blit(text16, [totalcolumns*rectsizex+2, 410])

    def drawa(self):
        pg.draw.rect(display, (36, 248, 41), self.Arect)
    def drawa2(self):
        pg.draw.rect(display, (246, 45, 36), self.A2rect)

    def drawd(self):
        pg.draw.rect(display, (36, 248, 41), self.Drect)
    def drawd2(self):
        pg.draw.rect(display, (246, 45, 36), self.D2rect)

    def drawb(self):
        pg.draw.rect(display, (36, 248, 41), self.Brect)
    def drawb2(self):
        pg.draw.rect(display, (246, 45, 36), self.B2rect)

    def drawdd(self):
        pg.draw.rect(display, (36, 248, 41), self.ddrect)
    def drawbdd2(self):
        pg.draw.rect(display, (246, 45, 36), self.dd2rect)

    def drawp(self):
        pg.draw.rect(display, (36, 248, 41), self.prect)
    def drawp2(self):
        pg.draw.rect(display, (246, 45, 36), self.p2rect)
    
    def drawpo(self):
        pg.draw.rect(display, (36, 248, 41), self.porect)
    def drawpo2(self):
        pg.draw.rect(display, (246, 45, 36), self.po2rect)

    def draww(self):
        pg.draw.rect(display, (36, 248, 41), self.wrect)
    def draww2(self):
        pg.draw.rect(display, (246, 45, 36), self.w2rect)

    def drawgo(self):
        pg.draw.rect(display, (36, 248, 41), self.gorect)
    def drawgo2(self):
        pg.draw.rect(display, (246, 45, 36), self.go2rect)

#makes 2d array of cell Nodes
cells = []
for i in range(0, totalrow):
    cellrow = []
    for j in range(0, totalcolumns):
        x = rectsizex * j
        y = rectsizey * i
        node = Node()
        node.x = x
        node.y = y
        node.row = int(y/rectsizex)
        node.col = int(x/rectsizey)
        cellrow.append(node)
    cells.append(cellrow)
emousedown = False
endacheck = False
startacheck = False
smousedown = False

iterpath = 0
iterroute = 0 
iterpink = 0
breadthflag = False
pathh = []
route = []
pink = []
aflag = False

while True:



    siderbar = sidebar()
    mx, my = pg.mouse.get_pos()
    pos = pg.mouse.get_pos()
    mrow= int(my/rectsizex)
    mcol= int(mx/rectsizey)
    siderbar.drawdd()
    siderbar.drawp()
    siderbar.drawpo()
    siderbar.draww()
    siderbar.drawgo()

    if acheck:
        siderbar.drawa2()
    elif not acheck:
        siderbar.drawa()
    if bcheck:
        siderbar.drawb2()
    elif not bcheck:
        siderbar.drawb()
    if dcheck:
        siderbar.drawd2()
    elif not dcheck:
        siderbar.drawd()
    

    for i in range(0, totalrow):
        for j in range(0, totalcolumns):
            cells[i][j].rect()

    keys = pg.key.get_pressed() 
    if keys[pg.K_w]:
        wall()
    if keys[pg.K_e]:
        erase()
    if emousedown and endacheck and mx<totalcolumns*rectsizex and acheck:
        for i in cells:
            for j in i:
                if not j.start and not j.obs:
                    j.isempty()           
        aflag = False
        endpressed()
        goA()
    if smousedown and startacheck and mx<totalcolumns*rectsizex and acheck:
        for i in cells:
            for j in i:
                if not j.end and not j.obs:
                    j.isempty()
        aflag = False
        startpressed()
        goA()
    if emousedown and endacheck and mx<totalcolumns*rectsizex and bcheck:
        for i in cells:
            for j in i:
                if not j.start and not j.obs:
                    j.isempty()
                    j.visited = False
        endpressed()
        gobreadth()
    if smousedown and startacheck and mx<totalcolumns*rectsizex and bcheck:
        for i in cells:
            for j in i:
                if not j.end and not j.obs:
                    j.isempty()
        startpressed()
        gobreadth()
    if emousedown and endacheck and mx<totalcolumns*rectsizex and dcheck:
        for i in cells:
            for j in i:
                if not j.start and not j.obs:
                    j.isempty()
        endpressed()
        godepth()
    if smousedown and startacheck and mx<totalcolumns*rectsizex and dcheck:
        for i in cells:
            for j in i:
                if not j.end and not j.obs:
                    j.isempty()
        startpressed()
        godepth()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:   
            mouse = pg.mouse.get_pressed()
            if mouse[2] and emousedown == True:
                emousedown = False
                endacheck = False
            if mouse[0] and endd.row == mrow and endd.col == mcol:
                emousedown = True
                endacheck = True
                
            if mouse[2] and smousedown == True:
                smousedown = False
                startacheck = False
            if mouse[0] and startt.row == mrow and startt.col == mcol:
                smousedown = True
                startacheck = True
    
            if siderbar.ddrect.collidepoint(mx, my):
                if mouse[0]:
                    siderbar.drawbdd2()
                    delete()
            elif siderbar.prect.collidepoint(mx, my):
                if mouse[0]:
                    siderbar.drawp2()
                    pathdelete()
            elif siderbar.porect.collidepoint(mx, my):
                if mouse[0]:
                    siderbar.drawpo2()
                    onlypathdelete()
            elif siderbar.wrect.collidepoint(mx, my):
                if mouse[0]:
                    siderbar.draww2()
                    generate()
            elif siderbar.gorect.collidepoint((pos)) and (acheck or bcheck or dcheck):
                if mouse[0] and acheck:
                    onlypathdelete()
                    siderbar.drawgo2()
                    pathh, pink, route = decA(startt, endd)
                    pink = deleterepeats(pink)
                    acheck = True
                    aflag = True
                elif mouse[0] and bcheck:
                    onlypathdelete()
                    siderbar.drawgo2()
                    pathh, route = disgobreadth()
                    breadthflag = True
                elif mouse[0] and dcheck:
                    onlypathdelete()
                    siderbar.drawgo2()
                    godepth()
            elif siderbar.Arect.collidepoint(mx, my):
                if mouse[0] and acheck == False:
                    acheck = True
                    bcheck = False
                    dcheck = False
                elif mouse[2] and acheck == True:
                    acheck = False
            elif siderbar.Brect.collidepoint(mx, my):
                if mouse[0] and bcheck == False:
                    bcheck = True
                    acheck = False
                    dcheck = False
                elif mouse[2] and bcheck == True:
                    bcheck = False
            elif siderbar.Drect.collidepoint(mx, my):
                if mouse[0] and dcheck == False:
                    dcheck = True
                    bcheck = False
                    acheck = False
                elif mouse[2] and dcheck == True:
                    dcheck = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                startpressed()
            if event.key == pg.K_t:
                endpressed()


    if breadthflag:
        tickspeed = 90
        if iterroute == len(route):
            if iterroute > 0:
                route[iterroute-1].isorange()
            tickspeed = 20
            route = []
            iterroute = 0
            pathh[iterpath].isslightor()
            if iterpath > 0:
                pathh[iterpath-1].isblue()
            iterpath += 1
            if iterpath == len(pathh):
                pathh[iterpath-1].isblue()
                tickspeed = 60
                pathh = []
                iterpath = 0
                breadthflag = False
                continue
            clock.tick(tickspeed)
            pg.display.update()
            continue
        route[iterroute].isslightor()
        if iterroute > 0:
            route[iterroute -1].isorange()
        iterroute +=1
        clock.tick(tickspeed)
        pg.display.update()
        continue
   
    if aflag:
        tickspeed = 70
        if iterpink == len(pink):
            if iterpink > 0:
                pink[iterpink-1].ispink()
            tickspeed = 60
            pink = []
            iterpink = 0
            if iterroute > 0 and iterroute < len(route):
                route[iterroute-1].isaqua()
            if iterroute > 0 and iterroute < len(route):
                route[iterroute].isslightor()
            if iterroute == len(route):
                if iterroute > 0:
                    route[iterroute-1].isaqua()
                tickspeed = 30
                route = []
                iterroute = 0
                pathh[iterpath].isslightor()
                if iterpath > 0:
                    pathh[iterpath-1].isblue()
                iterpath += 1
                clock.tick(tickspeed)
                pg.display.update()
                if iterpath == len(pathh):
                    if iterpath > 0:
                        pathh[iterpath-1].isblue()
                    tickspeed = 60
                    pathh = []
                    iterpath = 0
                    # acheck = True
                    aflag = False   
                continue
            iterroute += 1
            clock.tick(tickspeed)
            pg.display.update()
            continue
        pink[iterpink].isslightor()
        if iterpink > 0:
            pink[iterpink -1].ispink()
        iterpink +=1
        clock.tick(tickspeed)
        pg.display.update()
        continue


    clock.tick(tickspeed)
    pg.display.update()