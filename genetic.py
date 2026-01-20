import pygame
import os
import matplotlib.pyplot as plt
from plots import plots
from random import randint
from grid import grid
from individuals import individual
from time import sleep
pygame.init()

def title_graphs():
    plot.label(0, Xtitle="Generation number", Ytitle="Best Fitness", PlotTitle="Generation tracker")
    plot.label(1, Xtitle="Individual number", Ytitle="Fitness (scaled)", PlotTitle="Fitness tracker")
    plot.label(2, Xtitle="Generation number", Ytitle="Generation stats", PlotTitle="Overlaps / Coverage / Path Length")



#columns vs rows in grid
row = 3
col = 3

#WIDTH and HEIGHT of screen + the colors we will need
WIDTH, HEIGHT = col*50 + 350, 600
font = pygame.font.SysFont(None, 30)
white = [255, 255, 255]
black = [0, 0, 0]
blue = [0, 0, 255]
green = [0, 255, 0]
red = [255, 0, 0]

#creating grid object
grid = grid(row, col)

#creating population
max_gen = 100
gen_num = 0
num_indiv = 100
best_fitness = 0
best_fitness_scaled = 0
gen_since_change = 0
pop = [individual(grid) for i in range(0, num_indiv)]
sorted_pop = []
best_in_gen = []
next_gen = []
stats = {
    "overlaps": [],
    "coverage": [],
    "path_len": []
}
indiv_index = 0         #counter for each individual to be shown
show_best = 0           #This is a flag to show the best attempt, after generations run

#This creates the display screen
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{25},{50}"
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Training Window")
WIN.fill(white)

#creating matplotlib window from graphing and analytics
plot = plots(3, 1, WIDTH + 20, 25)
title_graphs()
plot.set_ymin(1, 0)
plt.pause(0.001)

#loop to keep the window open
running = True
while running:
    #for i in player.edges:   
        #print(f"{i.from_vertex}, {i.to_vertex}")
    #this is specifically to handle in game events
    WIN.fill(white)
    text_surface = font.render("Press 'N' to see best attempt", False, black)
    WIN.blit(text_surface, ((col + 1)*50, 70))
    text_surface = font.render('Generation number: ' + str(gen_num), False, black)
    WIN.blit(text_surface, ((col + 2)*50 - 20, 100))
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            #evaluates and creates new generation
            if event.key == pygame.K_n:
                show_best = 1
    if running == False:
        break

    if indiv_index < len(pop):
        pop[indiv_index].grid.reset()
        #print(len(pop[indiv_index].path))      #debug statement
        for move in pop[indiv_index].path:
            pop[indiv_index].draw_move(WIN)
            pygame.display.update()
            #time.sleep(.005)
        indiv_index += 1
    elif gen_since_change < 10:
        #This is to eval / sort by fitness
            best_in_gen.clear() 
            for indiv in pop:
                indiv.evaluate()
            sorted_pop = sorted(pop, key=lambda indiv: indiv.raw_fitness, reverse=True)
            #This is for getting top 35% of last gen to repopulate the next gen
            #There is an issue with this, best in gen does not = sorted         FIXED (I think)
            for i in range(0, int(len(sorted_pop)*.2)):
                #print(f"sorted = {sorted_pop[i].fitness}")         #debug
                best_in_gen.append(sorted_pop[i])   
                #print(f"best in gen = {best_in_gen[i].fitness}")   #debug
            #once we have the best we put the top 10% into next gen without change, choose the rest randomly and mutate them
            pop.clear()
            for i in range(num_indiv):
                if i <= num_indiv*.05:
                    pop.append(best_in_gen[i].copy())
            while len(pop) < num_indiv:
                parent = best_in_gen[randint(0, len(best_in_gen) - 1)].copy()
                parent.mutate()
                pop.append(parent)
            #allowing next gen to run
            indiv_index = 0
            gen_num += 1
            for i in range(5):
                print(f"#{i}: Coverage: {best_in_gen[i].traveled_edges}    Overlaps: {best_in_gen[i].overlaps}      path_len: {len(best_in_gen[i].path)}    wall_moves: {best_in_gen[i].wall_moves}     fitness: {best_in_gen[i].raw_fitness}")
            
            if best_fitness < best_in_gen[0].raw_fitness:
                best_fitness = best_in_gen[0].raw_fitness
                best_fitness_scaled = best_in_gen[0].scaled_fitness
                stats['coverage'].append(best_in_gen[0].traveled_edges)
                stats['overlaps'].append(best_in_gen[0].overlaps)
                stats['path_len'].append(len(best_in_gen[0].path))
                gen_since_change = 0
                print("improved")
            else:
                best_fitness = best_in_gen[0].raw_fitness
                best_fitness_scaled = best_in_gen[0].scaled_fitness
                stats['coverage'].append(best_in_gen[0].traveled_edges)
                stats['overlaps'].append(best_in_gen[0].overlaps)
                stats['path_len'].append(len(best_in_gen[0].path))
                gen_since_change += 1
            for i in pop:
                i.reset()
            
            #This is where I will update the graphs
            best_fitness_vals = [ind.scaled_fitness for ind in sorted_pop]
            plot.add_point(0, Ydata=best_fitness_scaled, Xdata=gen_num)
            plot.plot_data(1, Ydata=best_fitness_vals, Xdata=[num_indiv - i for i in range(1, num_indiv+1)], Ymin=0)
            #plot.plot_data(2, Ydata=stats, Xdata= [i for i in range(1, gen_num + 1)], Ymin=0)

            title_graphs()

    else:
        if show_best:
            best_in_gen[0].reset()
            best_in_gen[0].grid.reset()
            for move in best_in_gen[0].path:
                best_in_gen[0].draw_move(WIN)
                pygame.display.update()
                sleep(.2)
            plt.pause(0.001)
            show_best = 0

pygame.quit()
