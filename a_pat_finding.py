"""
We are implementing A* path finding algorithm to find the smallest route.
The route needs to be found between two given nodes. We find this route
by ranking according to F = G + H 
1)its heuristic distance(which is guessed) H from the end node
2)its distance G from the initial point.
We also remember the previous node of the current one.
In the beginning we assign infinity to G and H to all the nodes
we have in the graph except for the initial node. 
G and H of original point is equal to 0. 
Then we begin by taking the next to the initial point. We know its G 
and we guess its H. Then we add this node to the openset as (F,node_name)

After that we go to the next node and do the same operation. 
We'll add it to the open set.
We will take its F and node_name as the smallest one if it's smaller
than all the others in the open set.
As we reached the final point we find its F and nodes which led us to it
"""
import pygame
import math
from queue import PriorityQueue

width = 800
win = pygame.display.set_mode((width,width))
pygame.display.set_caption('A* Path Finding')

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
white = (255,255,255)
black = (0,0,0)
purple = (128,0,128)
orange = (255,165,0)
grey = (128,128,128)
turquiose = (64,224,208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = white
        self.neighbors = []
        self.width = width   #width of the cube
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == red
    
    def is_open(self):
        return self.color == green

    def is_barrier(self):
        return self.color == black

    def is_start(self):
        return self.color == orange

    def is_end(self):
        return self.color == turquiose
    
    def reset(self):
        self.color == white #(?)
    
    def make_start(self):
        self.color = orange

    def make_closed(self):
        self.color = red
    
    def make_open(self):
        self.color = green

    def make_barrier(self):
        self.color = black
    
    def make_end(self):
        self.color = turquiose

    def make_path(self):
        self.color = purple

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.x, self.width, self.width)) #?
    
    def update_neighbours(self, grid):
        pass

    def __lt__(self,other):
        return False

def h(p1,p2):
    """
    Manhattan distance.
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
    
def make_grids(rows,width):
    """
    Create cubes.
    width - width of the whole grid
    rows - number of rows in the grid. Equal to columns
    """
    grid = []
    gap = width // rows  #width of a single cube
    for i in range(rows):
        grid.append([]) #create a row
        for j in range(rows):
            spot = Spot(i, j, gap, rows)  #create a cube
            grid[i].append(spot)

    return grid

def draw_grid(win,rows,width):
    """
    Draws the lines between the cube.
    """
    gap = width // rows #width of a single cube
    for i in range(rows):
        pygame.draw.line(win,grey, (0,i*gap),(width,i*gap)) #draws horizontal lines
        for j in range(rows):
            pygame.draw.line(win,grey, (j*gap,0),(j*gap,width)) #draws vertical lines

def draw(win,grid,rows,width):
    """
    We always draw the whole grid again after the clicking of the mouse.
    """
    win.fill(white)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win,rows,width)
    pygame.display.update()

def get_clicked_pos(pos,rows,width):
    """
    Returns the row and column the click was.
    pos - the place your mouse clicked.
    """
    y,x = pos
    gap = width // rows
    row = y // gap
    col = x // gap
    return row, col

def main(win,width):
    ROWS = 50
    grid = make_grids(ROWS, width) #cube

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]: #left button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width) #row and column of the click
                spot = grid[row][col]

                if not start:
                    start = spot
                    start.make_start()

                elif not end:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pass

    pygame.quit()

main(win,width)