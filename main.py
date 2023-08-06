import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* algorithm visualiser")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 , 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.colour = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows
    def get_pos(self):
        return self.row,self.col
    def is_closed(self):
        return self.colour == RED
    def is_open(self):
        return self.colour == GREEN
    def is_barrier(self):
        return self.colour == BLACK
    def is_start(self):
        return self.colour == ORANGE


    def is_end(self):
        return self.colour == TURQUOISE
    def reset(self):
        self.colour = WHITE
    def close(self):
        self.colour = RED
    def open(self):
        self.colour = GREEN
    def barrier(self):
        self.colour = BLACK
    def start(self):
        self.colour = ORANGE
    def end(self):
        self.colour = TURQUOISE
    def path(self):
        self.colour = PURPLE
    def draw(self, win):
        pygame.draw.rect(win, self.colour,(self.x, self.y, self.width, self.width))
    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows -1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row-1][self.col])

        if self.col < self.total_rows -1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbours.append(grid[self.row][self.col+1])

        if self.col > 0  and not grid[self.row][self.col - 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col-1])
    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2)+abs(y1-y2)




def reconstructPath(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.path()
        draw()



def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {Spot: float("inf") for row in grid for Spot in row}
    g_score[start] = 0
    f_score = {Spot: float("inf") for row in grid for Spot in row}
    f_score[start] = h(start.get_pos(),end.get_pos())
    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            reconstructPath(came_from,end,draw)
            end.end()
            return True
        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.open()
        draw()

        if current != start:
            current.close()
    return False





def make_grid(rows, width):
    grid = []
    gap = width//rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows, )
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    gap = width//rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0,i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_position(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y// gap
    col = x // gap

    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    End = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != End:
                    start = spot
                    start.start()
                elif not End and spot != start:
                    End = spot
                    End.end()
                elif spot != End and spot != start:
                    spot.barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == End:
                    End = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and End:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, End)
                if event.key == pygame.K_c:
                    start = None
                    End = None
                    grid = make_grid(ROWS, WIDTH)
    pygame.quit()

main(WIN, WIDTH)