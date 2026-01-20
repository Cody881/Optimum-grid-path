import pygame
class vertex:
    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.edges = []
        #this is needed for draw function in class
        self.w = w
        self.color = [0, 0, 255]
    def draw_vertex(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.w))

class edge:
    def __init__(self, from_vertex, to_vertex):
        #for determining which line is traveled
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.color = [255, 0, 0]
        #determining if edge has been crossed before (flag)
        self.crossed = 0
    def draw_edges(self, win):
        pygame.draw.line(win, self.color, self.from_vertex, self.to_vertex)
    
    def reset_edge(self):
        self.color = [255, 0, 0]
        self.crossed = 0
        
"""
the grid class is the only class that is used,
the edge and vertex class are used to help the grid class
"""
class grid:
    def __init__(self, rows, cols):
        #Saving the amount of rows / cols
        self.row = rows
        self.col = cols
        #this is used to store / create edges and vertices
        self.vertices = []
        self.edges = []
        self.create_edges()
        self.create_vertices()
        self.find_edges_for_point()
        self.total_edges = len(self.edges)
        #specifcally needed for printing stats
        self.font = pygame.font.SysFont(None, 25)
        
    
    def create_vertices(self):
        rectX = 50
        rectY = 50
        rectW = 10
        for x in range(0, self.col):
            rectY = 50
            for y in range(0, self.row):
                self.vertices.append(vertex(rectX, rectY, rectW))
                rectY += 50
            rectX += 50

    def create_edges(self):
        #this is creating the horizontal portion of edges
        rectX = 55
        for x in range(0, self.col - 1):
            rectY = 55
            for y in range(0, self.row):
                self.edges.append(edge((rectX, rectY), (rectX + 50, rectY)))
                rectY += 50
            rectX += 50
        #this is creating the vertical edges
        rectX = 55
        for x in range(0, self.col):
            rectY = 55
            for y in range(0, self.row - 1):
                self.edges.append(edge((rectX, rectY), (rectX, rectY + 50)))
                rectY += 50
            rectX += 50

    def find_edges_for_point(self):
        for point in self.vertices:
            for line in self.edges:
                if (point.x + 5, point.y + 5) == line.to_vertex or (point.x + 5, point.y + 5) == line.from_vertex:
                    point.edges.append(line)

    #This function draws the entire grid
    def draw_grid(self, win):
        #this draws just the edges
        for line in self.edges:
            line.draw_edges(win)
        #this draws the vertices ontop of edges
        for point in self.vertices:
            point.draw_vertex(win)

    def reset(self):
        for line in self.edges:
            line.reset_edge()
        for point in self.vertices:
            point.color = [0, 0, 255]
    
                

