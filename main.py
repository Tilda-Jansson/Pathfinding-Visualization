import pygame
import math
from queue import PriorityQueue

SCREEN_SIZE = 800
WINDOW = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Pathfinding Visualizer of A* algorithm")

BROWN = (139, 69, 19)
LIGHT_BLUE = (135, 206, 250)
BLUE = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
PINK = (255, 105, 180)
GREY = (128, 128, 128)
LIME = (0, 255, 127)

class Node:
    def __init__(self, row, col, size, total_rows):
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.color = WHITE
        self.adjacent_nodes = []
        self.size = size
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col

    def is_visited(self): # already looked at
        return self.color == BROWN

    def is_unvisited(self): # in the open set
        return self.color == LIGHT_BLUE

    def is_obstacle(self):
        return self.color == BLACK

    def is_start_node(self):
        return self.color == PINK

    def is_end_node(self):
        return self.color == LIME

    def clear(self):
        self.color = WHITE

    def set_start(self):
        self.color = PINK

    def set_visited(self):
        self.color = BROWN

    def set_unvisited(self):
        self.color = LIGHT_BLUE

    def set_obstacle(self):
        self.color = BLACK

    def set_end(self):
        self.color = LIME

    def set_path(self):
        self.color = GOLD

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

    # Neighbours cannot be obstacles
    def update_adjacent_nodes(self, grid):
        self.adjacent_nodes = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for direction in directions:
            new_row = self.row + direction[0]
            new_col = self.col + direction[1]
            if 0 <= new_row < self.total_rows and 0 <= new_col < self.total_rows and not grid[new_row][new_col].is_obstacle():
                self.adjacent_nodes.append(grid[new_row][new_col])

    def __lt__(self, other):
        return False

# Chebyshev distance as the heuristic if diagonal movement is used
def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return max(abs(x1 - x2), abs(y1 - y2))


# Traverse back from the end node to the start node
def build_path(previous_nodes, current_node, draw_func):
    while current_node in previous_nodes:
        current_node = previous_nodes[current_node]
        current_node.set_path()
        draw_func()

def a_star(draw_func, grid, start_node, end_node):
    counter = 0 # when items were inserted into the queue - used as a tie-breaker
    open_set = PriorityQueue()
    open_set.put((0, counter, start_node)) # f score of start node is 0

    previous_nodes = {}

    g_score = {node: float("inf") for row in grid for node in row} # current shortest distance from start node to this node
    g_score[start_node] = 0

    f_score = {node: float("inf") for row in grid for node in row} # predicted distance from current node to end node
    f_score[start_node] = heuristic(start_node.get_position(), end_node.get_position())

    open_set_hash = {start_node} # keep track of items in priority queue

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = open_set.get()[2] # get node with lowest f score
        open_set_hash.remove(current_node)  # synchronize

        if current_node == end_node: # make path
            build_path(previous_nodes, end_node, draw_func)
            end_node.set_end()
            return True

        for neighbor in current_node.adjacent_nodes:
            # Cost for diagonal moves is sqrt(2) = 1.41421356, otherwise cost is 1
            move_cost = 1.41421356 if (neighbor.row != current_node.row) and (neighbor.col != current_node.col) else 1
            temp_g_score = g_score[current_node] + move_cost

            if temp_g_score < g_score[neighbor]: # find the shortest path to each node and update if needed
                previous_nodes[neighbor] = current_node
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_position(), end_node.get_position())

                if neighbor not in open_set_hash:
                    counter += 1
                    open_set.put((f_score[neighbor], counter, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_unvisited() # make Light blue

        draw_func()

        if current_node != start_node:
            current_node.set_visited() # make brown, node considered

    return False

def create_grid(rows, size):
    grid = []
    gap = size // rows  # width of each cube
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# called at the beginning of every frame
def draw(win, grid, rows, size):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win) # draws cube with its own color

    draw_grid_lines(win, rows, size)
    pygame.display.update()


def get_mouse_position(pos, rows, size):
    gap = size // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, size):
    ROWS = 50
    grid = create_grid(ROWS, size) #2D list

    start_node = None
    end_node = None

    running = True
    while running:
        draw(win, grid, ROWS, size) # Draw everything

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_position(pos, ROWS, size)
                node = grid[row][col]

                if not start_node and node != end_node: # Set start and end pos first
                    start_node = node
                    start_node.set_start()

                elif not end_node and node != start_node:
                    end_node = node
                    end_node.set_end()

                elif node != end_node and node != start_node:
                    node.set_obstacle()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_position(pos, ROWS, size)
                node = grid[row][col]
                node.clear()

                if node == start_node:
                    start_node = None
                elif node == end_node:
                    end_node = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_node and end_node: # RUN the algorithm
                    for row in grid:
                        for node in row:
                            node.update_adjacent_nodes(grid)

                    a_star(lambda: draw(win, grid, ROWS, size), grid, start_node, end_node)

                if event.key == pygame.K_c: # clear screen
                    start_node = None
                    end_node = None
                    grid = create_grid(ROWS, size)

    pygame.quit()

main(WINDOW, SCREEN_SIZE)