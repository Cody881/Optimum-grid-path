import pygame
from grid import grid
from random import randint
from math import ceil, pow, cbrt
class individual:
    def __init__(self, grid):
        self.grid = grid
        self.move_num = 0
        self.path = [randint(1, 4) for _ in range(0, randint(len(self.grid.edges), ceil(len(self.grid.edges)*1.2)))]
        self.raw_fitness = 0
        self.scaled_fitness = 0
        self.overlaps = 0
        self.wall_moves = 0         #of moves that run into a wall and do nothing
        self.steps_taken = 0
        self.starting_index = 0
        self.traveled_edges = 0
        self.edges_crossed = []
        #player also for drawing onto screen mainly
        self.player = self.grid.vertices[0]
        self.player.color = [0, 255, 0]
        self.player_index = randint(0, len(self.grid.vertices) - 1)

    #add in finding the current / next vertexs 
    #also add logic to figure out what edge is being crossed
    def move_to_next(self):
        """
            We will initialize:
            1 = up
            2 = down
            3 = left
            4 = right
            
            indexing works in this order
                0  3  6
                1  4  7
                2  5  8
            This is for a 3x3 but the same concept is for larger or smaller grids.
        """
        if self.move_num >= len(self.path):
             return
        #local variables for clarity
        blue = [0, 0, 255]
        green = [0, 255, 0]
        vertices = self.grid.vertices
        player = self.player
        player_index = self.player_index
        row = self.grid.row
        col = self.grid.col

        #finding the prev vertex before moving
        prev_vertex = (player.x + 5, player.y + 5)
        next_vertex = (0, 0)
        #up
        if self.path[self.move_num] == 1:
            if player_index % row > 0:
                    new_index = player_index - 1
                    player.color = blue
                    player_index = new_index
                    player = vertices[player_index]
                    player.color = green
                    self.steps_taken += 1
        #down
        if self.path[self.move_num] == 2:
            if player_index % row < row - 1:
                    new_index = player_index + 1
                    player.color = blue
                    player_index = new_index
                    player = vertices[player_index]
                    player.color = green
                    self.steps_taken += 1
        #left
        if self.path[self.move_num] == 3:
            if player_index - row > - 1:
                    new_index = player_index - row
                    player.color = blue
                    player_index = new_index
                    player = vertices[player_index]
                    player.color = green
                    self.steps_taken += 1
        #right
        if self.path[self.move_num] == 4:
            if player_index + row < len(vertices):
                    new_index = player_index + row
                    player.color = blue
                    player_index = new_index
                    player = vertices[player_index]
                    player.color = green
                    self.steps_taken += 1
        self.move_num += 1

        next_vertex = (player.x + 5, player.y + 5)
        player.color = [0, 255, 0]
        for line in player.edges:
            if (line.from_vertex == prev_vertex and line.to_vertex == next_vertex or
                line.from_vertex == next_vertex and line.to_vertex == prev_vertex):                    
                if line not in self.edges_crossed:
                    line.color = [0, 255, 0]
                    self.traveled_edges += 1
                    self.edges_crossed.append(line)
                else:
                    self.overlaps += 1
                    break
        if prev_vertex == next_vertex:
             self.wall_moves += 1
        
        #setting player globally
        self.player = player
        self.player_index = player_index  

    def draw_changes(self, win):
        self.grid.draw_grid(win)
        self.player.draw_vertex(win)

    def evaluate(self):
        #coverage = self.traveled_edges / len(self.grid.edges)
        coverage = self.traveled_edges
        overlap = self.overlaps
        length = len(self.path)
        if 50 - length > -1:
             length_penalty = pow(50 - length, 1.5)
        else:
             length_penalty = -((50 - length)**2)
        self.raw_fitness = pow(coverage, 4.5) - pow(overlap, 4) - pow(length, 2) - pow(self.wall_moves, 5)
        self.scaled_fitness = self.raw_fitness **.1
    
    def mutate(self):
        for move in self.path:
            if randint(0, 100) < 15:
                    move = randint(1, 4)
        if randint(0, 100) < 7:
            i = randint(0, len(self.path) - 1)
            self.path.insert(i, randint(1, 4))
        if randint(0, 100) < 7 and len(self.path) > len(self.grid.edges):
            i = randint(0, len(self.path) - 1)
            self.path.pop(i)
        if randint(0, 100) < 10:
            self.player_index = randint(0, len(self.grid.vertices) - 1) 

    def draw_path(self, win):
       for move in self.path:
            self.draw_move(win)
            
    def draw_move(self, win):
         self.move_to_next()
         self.draw_changes(win)

    #reseting counting stats so we can reuse for next gen
    def reset(self):
        self.move_num = 0
        self.fitness = 0
        self.overlaps = 0
        self.steps_taken = 0
        self.starting_index = 0
        self.traveled_edges = 0
        self.edges_crossed.clear()
        self.player.color = [0, 255, 0]
        self.player_index = 0
             
    def copy(self):
        new = individual(self.grid)
        new.path = self.path.copy()
        return new