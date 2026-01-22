# Genetic Algorithm inspired by the Chinese Postman Problem
This is a Python implementation of a non-state-aware genetic algorithm that 
intends to create approximate traversal solutions on unweighted graph edges, 
relating to the Chinese Postman Problem

## Why this project?
This project started around Christmas time when my brother was telling me that he
wanted to figure out how to run the streets of the city he lives in as efficiently
as possible, which is largely in a grid layout. We could not find a
Concrete solution online, so I decided to use programming to attempt to solve this 
problem.  What started as a small experiment evolved into an ongoing 
project that I have continued to refine through discussion with classmates and 
independent iteration.

## How it Works
- The graph is represented as an unweighted grid
- Individuals attempt to cover all edge pieces of the grid
- Fitness is calculated mainly by the number of unique edges traveled and the number of overlaps
- A basic selection algorithm is then applied after every generation, and then each individual is mutated
- Basic stats are tracked through every generation
  

## Current Limitations
- graphs are unweighted (edges have equal "costs")
- Performance gets worse on larger graphs (Longer training for less impressive results)
- Individuals are not state-aware, and all movement is random, which results in worse performance and possibly longer training periods

## Future improvements
- Extend graph representation to support weighted edges, and adapt the fitness function for this
- Improve convergence speed and solution quality, probably through state awareness
- Improve graphing of fitness statistics

## Project structure
- 'Genetic.py' is the core genetic algorithm logic
- 'Individual.py' holds the class for all the logic and data each Individual needs
- 'grid.py' has the class that deals with graph representation
- 'plot.py' deals with the visualization of data from the genetic algorithm
- 'manual.py' allows for entry and manual execution for experimentation
