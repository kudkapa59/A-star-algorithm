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

width = 1400
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

class Spot:  #May be we need to begin writing from a smaller letter
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
        self.color = white #(?)
    
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
        self.neighbors = []

        #Checking if we can go down and the down cell isn't a barrier
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        #Checking if we can go up and the down cell isn't a barrier
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        #Checking if we can go right and the down cell isn't a barrier
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        #Checking if we can go left and the down cell isn't a barrier
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])

    def __lt__(self,other):
        return False

def h(p1,p2):
    """
    Heuristics score. Manhattan distance.

    Args:
        p1,p2: Positions of two points.
    """

    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
    
def make_grids(width,rows):
    """
    Creates array of cubes.

    Args:
        width:  Width of the whole grid.
        rows:   Number of rows in the grid. Equal to columns.
    """

    grid = []
    gap = width // rows  #width of a single cube
    for i in range(rows):
        grid.append([]) #create a row
        for j in range(rows):
            spot = Spot(i, j, gap, rows)  #create a cube
            grid[i].append(spot)

    return grid

def draw_grid(win,width,rows):
    """
    Draws the lines between the cubes.

    Args:
        win:    
        width:  Width of the whole grid.
        rows:   Number of rows in the grid. Equal to columns.
    """

    gap = width // rows #width of a single cube
    for i in range(rows):
        pygame.draw.line(win,grey, (0,i*gap),(width,i*gap)) #draws horizontal lines
        for j in range(rows):
            pygame.draw.line(win,grey, (j*gap,0),(j*gap,width)) #draws vertical lines

def draw(win,grid,width,rows):
    """
    Draws the whole grid.
    Always draws the whole grid again after the clicking of the mouse.

    Args:
        win:    
        grid:   Our grid. The array of rows.
        width:  Width of the whole grid.
        rows:   Number of rows in the grid. Equal to columns.
    """

    win.fill(white)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win,width,rows)
    pygame.display.update()

def get_clicked_pos(pos,width,rows):
    """
    Returns the row and column where the click was.

    Args:
        pos - the place your mouse clicked.
        width:  Width of the whole grid.
        rows:   Number of rows in the grid. Equal to columns.
    """

    y,x = pos
    gap = width // rows
    row = y // gap
    col = x // gap
    return row, col


def algorithm(draw, grid, start, end):
    """
    """

    count = 0 #If two spots have the same F score, we choose the one, which was added earlier
    #(whose count is lower)

    open_set = PriorityQueue()
    open_set.put(0, count, start) #push method, 0 - F score, start - the node
    came_from = {}  #Whic spots we came from

    #First spot is infinity. 
    g_score = {spot: float{'inf'} for row in grid for spot in row}
    g_score[start] = 0 #g_score of the start is zero

    f_score = {spot: float{'inf'} for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos()) #heuristics from the end

    open_set_hash = {start} #Checking what is in PriorityQueue and what's outside
    #We can pull something outside of the queue, but we can't check what's inside

    while not open_set.empty():
        for event in pygame.event.get():
            #We have to quit the algorithm in case of the loop
            if event.type == pygame.QUIT():
                pygame.quit()

        current = open_set.get()[2] #node


def main(win,width):
    """
    Does all the checks. Click - change the barrier.

    Args:
        win:
        width: Width of the whole grid.
    """

    ROWS = 50 #Number of rows in a grid.
    grid = make_grids(width, ROWS) #array of all cubes

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, width, ROWS)     #Draws the whole grid.
        for event in pygame.event.get(): #Checking all the events that happened.
            if event.type == pygame.QUIT: #If X button is clicked, stop running the game.
                run = False

            if started: #Player won't be able to change obstacles or do developer's work.
                continue

            if pygame.mouse.get_pressed()[0]: #If the left button was pressed
                pos = pygame.mouse.get_pos() #x,y of the mouse
                row, col = get_clicked_pos(pos, width, ROWS) #row and column where the click was
                spot = grid[row][col]  #cube

                if not start and spot != end: #If start isn't yet defined, thic cube is the start.
                    start = spot #The start is the first cube we click on. 
                    start.make_start()

                elif not end and spot != start: #End is the second cube we choose.
                    end = spot
                    end.make_end()

                elif spot != end and spot != start: #If we don't click on start or end
                    spot.make_barrier()             #Then we define the barrier.

            elif pygame.mouse.get_pressed()[2]: #If the right button was pressed
                pos = pygame.mouse.get_pos() #x,y of the mouse
                row, col = get_clicked_pos(pos, width, ROWS) #row and column where the click was
                spot = grid[row][col]  #cube
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            
            if event.type == pygame.KEYDOWN: #By clicking Space button we begin the algorithm.
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours()
                    algorithm(lambda: draw(win,grid, width, ROWS), grid, start, end)

    pygame.quit()

main(win,width)