import sys
import time
import numpy as np
import tkinter as Mazegame
from termcolor import colored
from PIL import ImageTk, Image
from tkinter import ttk, Canvas, Label
from queue import Queue
from queue import LifoQueue

#This function initializes lion and meat positions
def startend_postion(n):
    start = 0
    end = n*n-1
    return start, end

#This function randomly create walls in maze
def randomize(n):
    limit = np.random.randint(n*n/4,n*n/2)
    checklist = list()

    for i in range(limit):
        hold = np.random.randint(n*n-1)
        chk = 0
        for j in range(len(checklist)):
            if checklist[j] == hold or hold == 0:
                chk = 1
        if chk == 0:
            checklist.append(hold)
    return checklist

#This function prepares full maze layout
def prepare_maze(n, checklist, start, end):
    maze = [[0 for i in range(n)] for j in range(n)]
    for i in range(len(checklist)):
        maze[checklist[i]//n][checklist[i]%n] = 1

    maze[start//n][start%n] = 0
    maze[end//n][end%n] = 0

    return maze

#
def display_maze(n, maze, pos):
    print("")
    for i in range(n):
        for j in range(n):
            if pos == i*n+j:
                print(colored("[8]", "blue"), end="")
            elif maze[i][j] == 0:
                print(colored("[0]", "green"), end="")
            elif maze[i][j] == 1:
                print(colored("[1]", "red"), end="")
            elif maze[i][j] == -1:
                print(colored("[3]", "yellow"), end="")
            elif maze[i][j] == 2:
                print(colored("[3]", "cyan"), end="")
        print("")

def make_screen(n):
    if n in range(2,9):
       size = 300
    elif n in range(9,43):
       size = 640
    elif n in range(43, 75):
       size = 750
    else:
        print("Invalid Maze size")
        sys.exit()

    cell_width = int(size/n)
    cell_height = int(size/n)

    screen = Mazegame.Tk()
    screen.title("Will lion find meat??")
    grid = Canvas(screen, width = cell_width*n, height = cell_height*n, highlightthickness=0)
    grid.pack(side="top", fill="both", expand="true")

    rect = {}
    for col in range(n):
        for row in range(n):
            x1 = col * cell_width
            y1 = row * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            rect[row, col] = grid.create_rectangle(x1,y1,x2,y2, fill="red", tags="rect")
    return grid, rect, screen, cell_width

def load_img(size, path, end):
    xcod = end//n
    ycod = end%n
    load = Image.open(path)
    load = load.resize((size, size), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render
    img.place(x = ycod*size, y = xcod*size)
    return img

# This function redraws maze and updates the maze according to the traversal at 'delay' time interval
def redraw_maze(grid, rect, screen, n, maze, pos, delay, size, end):
    grid.itemconfig("rect", fill="green")
    path2 = "./meat.png"
    for i in range(n):
        for j in range(n):
            item_id = rect[i,j]
            if pos == i*n+j:
                grid.itemconfig(item_id, fill="blue")
            elif maze[i][j] == 0:                       # positions where lion can move
                grid.itemconfig(item_id, fill="salmon")
            elif maze[i][j] == 1:                       # blocked positions/walls
                grid.itemconfig(item_id, fill="black")
            elif maze[i][j] == -1:                      # positions visited    
                grid.itemconfig(item_id, fill="DeepSkyBlue2")
            elif maze[i][j] == 2:
                grid.itemconfig(item_id, fill="SpringGreen2")

    load_img(size, path2, end)
    screen.update_idletasks()
    screen.update()
    time.sleep(delay)
    return

def button(text, win, window):
    b = ttk.Button(window, text=text, command = win.destroy)
    b.pack()

def popup_win(msg, title, path ,screen):
    popup = Mazegame.Tk()
    popup.wm_title(title)
    label = ttk.Label(popup, text = msg, font=("Times", 20))
    label.pack(side="top", fill="x", pady=50, padx=50)
    button("Close Maze", screen, popup)
    button("Close popup", popup, popup)
    popup.mainloop()


# This function will contain all your search algorithms
# maze[row][col] should be used to refer to any position of maze
# pos is the starting position of maze and end is ending position
# pos//n will give row index and pos%n will give col index
# you can use list as stack or any other data structure to traverse the positions of the maze.
@profile
def search_algo(n, maze, start, end):
  pos = start
  cost=0 
  delay = 0.1
  grid, rect, screen, wid = make_screen(n)
  q=LifoQueue()
  q.put(pos)
  hash={pos:(pos,'S')}
  visited={pos:1}
  #print(hash)
  while ((pos!=end)):

       

      if(q.empty()):
           break
      current=q.get()
      
      row=current//n
      col=(current%n)
      maze[row][col]=-1
      cost=cost+3
      visited.update({current:1})
      #print("Current node is {0}".format(current))
      if(row in range(n) and col+1 in range(n) and maze[row][col+1]==0 ):
        #print(row)
        #print(col+1)
        nei=row*n+(col+1)
        if(nei in visited.keys()):
           hash.update({nei:(current,'R')})
        else:   
           q.put(nei)
           hash.update({nei:(current,'R')})
           visited.update({nei:1})
        #print("\n")
      if(row+1 in range(n) and col in range(n) and maze[row+1][col]==0):
        #print(row+1)
        #print(col)
        nei=(row+1)*n+col
        if(nei in visited.keys()):
           hash.update({nei:(current,'D')})
        else:   
           q.put(nei)
           hash.update({nei:(current,'D')})
           visited.update({nei:1})
        #print("\n")
      if(row in range(n) and col-1 in range(n) and maze[row][col-1]==0):
        #print(row)
        #print(col-1)
        nei=row*n+(col-1)
        if(nei in visited.keys()):
           hash.update({nei:(current,'L')})
        else:   
           q.put(nei)
           hash.update({nei:(current,'L')})
           visited.update({nei:1})
        #print("\n")
      if(row-1 in range(n) and col in range(n) and maze[row-1][col]==0):
        #print(row-1)
        #print(col)
        nei=(row-1)*n+(col)
        if(nei in visited.keys()):
           hash.update({nei:(current,'U')})
        else:   
           q.put(nei)
           hash.update({nei:(current,'U')})
           visited.update({nei:1})
       # print("\n")     
      pos=current
  #print(hash)
  #print(maze)
  lst=[]
  print("The cost incurred during the search is = "+ str(cost))
  print_path_cost(hash,end,lst)
  endTime = time.time()
  print("Time taken:", endTime-startTime, "secs")      

  redraw_maze(grid, rect, screen, n, maze, pos, delay, wid, end)
  popup_win("   ", "   ", "./final.png" , screen)

def print_path_cost(hash,node,lst):
 if(node in hash.keys()):
   t=hash[node]
   if(t[1]=='S'):
      lst.reverse()
      print("The path taken from start to goal is  "+str(lst))
      
      return
   else:
      parent=t[0]
      
      lst.append(t[1])
      
      print_path_cost(hash,parent,lst)
 else:
  print("Meat Unreachable")
 
  
if __name__ == "__main__":
    n =10 # size of maze
    start, end = startend_postion(n)
    randno = randomize(n)
    maze = prepare_maze(n, randno, start, end)
    startTime = time.time()
    search_algo(n, maze, start, end)
   

