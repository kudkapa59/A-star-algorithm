import pygame
import math
from queue import PriorityQueue

WIDTH = 2000
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

def colors():
    """
    Defines colors of cells depending on their status.

    Returns:
        colors: Dictionary[*some color] = RGB representation. 
    """

    colors = dict()

    colors['RED'] = (255, 0, 0)
    colors['GREEN'] = (0, 255, 0)
    colors['BLUE'] = (0, 0, 255)
    colors['YELLOW'] = (255, 255, 0)
    colors['WHITE'] = (255, 255, 255)
    colors['BLACK'] = (0, 0, 0)
    colors['PURPLE'] = (128, 0, 128)
    colors['ORANGE'] = (255, 165 ,0)
    colors['GREY'] = (128, 128, 128)
    colors['TURQUOISE'] = (64, 224, 208)

    return colors

class Cube:
    """
    The grid's cube characterization.
    """

    def __init__(self, row, col, width, total_rows):
        """
        Args:
        row: Row of the cube.
        col: Column of the cube.
        width: Width of the cube.
        total_rows: Number of rows used. Equal in vertical and horizontal direction.
        """

        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = colors['WHITE']
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows


    def check_start(self):
        return self.color == colors['ORANGE']

    def check_end(self):
        return self.color == colors['PURPLE']

    def check_open(self):
        return self.color == colors['BLUE']

    def check_closed(self):
        """
        
        """
    
        return self.color == colors['RED']

    def check_block(self):
        """
        Checks if the cube can be gone through.
        """

        return self.color == colors['BLACK']

    def get_loc(self):
        """
        Returns: row and column of the cube.
        """
    
        return self.row, self.col

    def reset(self):
        """
        Cancels all the properties assigned to the cube.
        """

        self.color = colors['WHITE']

    def make_start(self):
        self.color = colors['ORANGE']

    def close(self):
        self.color = colors['RED']

    def open(self):
        self.color = colors['BLUE']

    def make_barrier(self):
        self.color = colors['BLACK']

    def make_end(self):
        self.color = colors['PURPLE']

    def make_path(self):
        self.color = colors['GREEN']

    def depict(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].check_block(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].check_block(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].check_block(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].check_block(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

class AStar():

    def __init__(self):
        pass 

    def h(self, p1, p2):
        """
        Heuristics score. Manhattan distance between the current node and the end node.

        Args:
            p1,p2: Positions of two points.

        Returns:
            Distance between two points.
        """

        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)


    def reconstruct_path(self, came_from, live, depict):
        """
        Draws the shortest path. 

        Args:
            came_from: the node we came from.
            live:      Cube we are on.
            depict:    depict function.
        """
        while live in came_from:
            live = came_from[live]
            live.make_path()
            depict()


    def algorithm(self, depict, grid, start, end):
        """
        Implements A* algorithm. If two spots have the same F score, we choose the one, which was 
        added earlier(whose count is lower).

        Args:
            depict: depict function. 
            grid:   grid matrix.
            start:  node we start on.
            end:    node we end on.
        """
        count = 0 #If two spots have the same F score, we choose the one, which was added earlier
        #(whose count is lower)

        open_set = PriorityQueue()
        open_set.put((0, count, start)) #push method, 0 - F score, start - the node
        came_from = {}                  #Which spots we came from
        g_score = {j: float("inf") for i in grid for j in i}
        g_score[start] = 0              #g_score of the start is zero
        f_score = {j: float("inf") for i in grid for j in i}
        f_score[start] = self.h(start.get_loc(), end.get_loc())  #heuristics from the end

        open_set_hash = {start}   #Checking what is in PriorityQueue and what's outside
        #We can pull something outside of the queue, but we can't check what's inside
        #Helps to understand what is in the open set

        while not open_set.empty():
            for event in pygame.event.get():
                #We have to quit the algorithm in case of the loop
                if event.type == pygame.QUIT:
                    pygame.quit()

            live = open_set.get()[2] #node
            open_set_hash.remove(live)  #to deal with duplicates

            if live == end: #If we finished
                #make path
                self.reconstruct_path(came_from, end, depict)
                end.make_end()
                return True

            for neighbor in live.neighbors:
                temp_g_score = g_score[live] + 1 #one more node over

                if temp_g_score < g_score[neighbor]: #If this path is better
                    came_from[neighbor] = live
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.h(neighbor.get_loc(), end.get_loc())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.open()  #Put it in the open

            depict()

            if live != start:
                live.close()

        return False


    def make_grid(self, rows, width):
        """
        Creates array of cubes.

        Args:
            width:  Width of the whole grid.
            rows:   Number of rows in the grid. Equal to columns.
        """

        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Cube(i, j, gap, rows)
                grid[i].append(spot)

        return grid


    def draw_grid(self, win, rows, width):
        """
        Draws the lines between the cubes.

        Args:
            win:    Pygame window.
            width:  Width of the whole grid.
            rows:   Number of rows in the grid. Equal to columns.
        """

        gap = width // rows
        for i in range(rows):
            pygame.draw.line(win, colors['GREY'], (0, i * gap), (width, i * gap))
            for j in range(rows):
                pygame.draw.line(win, colors['GREY'], (j * gap, 0), (j * gap, width))


    def depict(self, win, grid, rows, width):
        """
        Depicts the whole grid.
        Always draws the whole grid again after the clicking of the mouse.

        Args:
            win:    Pygame window.
            grid:   Our grid. The array of rows.
            width:  Width of the whole grid.
            rows:   Number of rows in the grid. Equal to columns.
        """

        win.fill(colors['WHITE'])

        for row in grid:
            for spot in row:
                spot.depict(win)

        self.draw_grid(win, rows, width)
        pygame.display.update()


    def get_clicked_pos(self, pos, rows, width):
        """
        Returns the row and column where the click was.

        Args:
            pos:    The place your mouse clicked.
            width:  Width of the whole grid.
            rows:   Number of rows in the grid. Equal to columns.
        """    

        gap = width // rows
        y, x = pos

        row = y // gap
        col = x // gap

        return row, col


    def main(self, win, width):
        """
        Does all the checks. Click - change the barrier.

        Args:
            win:   Pygame window.
            width: Width of the whole grid.
        """

        ROWS = 50 #Number of rows in a grid.
        grid = self.make_grid(ROWS, width) #array of all cubes

        start = None
        end = None

        run = True
        while run:
            self.depict(win, grid, ROWS, width)  #Draws the whole grid.
            for event in pygame.event.get():  #Checking all the events that happened.
                if event.type == pygame.QUIT:  #If X button is clicked, stop running the game.
                    run = False

                if pygame.mouse.get_pressed()[0]: #If the left button was pressed
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()

                    elif not end and spot != start:
                        end = spot
                        end.make_end()

                    elif spot != end and spot != start:
                        spot.make_barrier()

                elif pygame.mouse.get_pressed()[2]: # RIGHT
                    pos = pygame.mouse.get_loc()
                    row, col = self.get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)

                        self.algorithm(lambda: self.depict(win, grid, ROWS, width), grid, start,\
                            end)

                    if event.key == pygame.K_c:
                        start = None
                        end = None
                        grid = self.make_grid(ROWS, width)

        pygame.quit()

if __name__ == '__main__':
    colors = colors()
    A = AStar()
    A.main(WIN, WIDTH)
