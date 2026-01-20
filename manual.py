import pygame
from grid import grid
from individuals import individual
pygame.init()

#WIDTH and HEIGHT of screen + the colors we will need
WIDTH, HEIGHT = 800, 600
white = [255, 255, 255]
blue = [0, 0, 255]
green = [0, 255, 0]
red = [255, 0, 0]

#columns vs rows in grid
row = 5
col = 5

#creating grid object
grid = grid(row, col)

#This creates the display screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN.fill(white)

#creating the player
#the player just uses one of the vertex objects and turns it green to indicate that the player is on that square
#any changes to the player object are by association given to the given vertex object
player = grid.vertices[0]
player_index = 0
"""
indexing works in this order
    0  3  6
    1  4  7
    2  5  8
This is for a 3x3 but the same concept is for larger or smaller grids.
"""
player.color = green

#loop to keep the window open
running = True
while running:
    WIN.fill(white)
    #for i in player.edges:   
        #print(f"{i.from_vertex}, {i.to_vertex}")
    #this is specifically to handle in game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            prev_vertex = (player.x + 5, player.y + 5)
            next_vertex = (0, 0)
            #handles reset press
            if event.key == pygame.K_s:
                starting_index = player_index
            if event.key == pygame.K_r:
                player.color = blue
                player_index = starting_index
                player = grid.vertices[player_index]
                player.color = green
                grid.steps_taken = 0
                grid.overlaps = 0
                grid.traveled_edges = 0
                for line in grid.edges:
                    if line.crossed == 1:
                        line.crossed = 0
            #handles LEFT press
            if event.key == pygame.K_LEFT:
                if player_index - row > - 1:
                    new_index = player_index - row
                    player.color = blue
                    player_index = new_index
                    player = grid.vertices[player_index]
                    player.color = green
                    grid.steps_taken += 1
            #handles RIGHT press
            if event.key == pygame.K_RIGHT:
                if player_index + row < len(grid.vertices):
                    new_index = player_index + row
                    player.color = blue
                    player_index = new_index
                    player = grid.vertices[player_index]
                    player.color = green
                    grid.steps_taken += 1
            #handles UP press
            if event.key == pygame.K_UP:
                if player_index % row > 0:
                    new_index = player_index - 1
                    player.color = blue
                    player_index = new_index
                    player = grid.vertices[player_index]
                    player.color = green
                    grid.steps_taken += 1
            #handles DOWN press
            if event.key == pygame.K_DOWN:
                if player_index % row < row - 1:
                    new_index = player_index + 1
                    if new_index < len(grid.vertices):
                        #this code just sets prev vertex back to normal and new vertex to player vertex
                        player.color = blue
                        player_index = new_index
                        player = grid.vertices[player_index]
                        player.color = green
                        grid.steps_taken += 1
            next_vertex = (player.x + 5, player.y + 5)
            for line in player.edges:
                if (line.from_vertex == prev_vertex and line.to_vertex == next_vertex or
                    line.from_vertex == next_vertex and line.to_vertex == prev_vertex):
                    if not line.crossed:
                        line.crossed = 1
                        grid.traveled_edges += 1
                    else:
                        grid.overlaps += 1
                        break

    #drawing edges and vertices every frame
    grid.draw_grid(WIN)
    grid.print_stats(WIN)

    player.draw_vertex(WIN)
    pygame.display.update()

pygame.quit()
