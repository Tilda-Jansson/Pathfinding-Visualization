# Pathfinding-Visualization

This project is a visual demonstration of the A* pathfinding algorithm, which searches for the shortest path between two points in a grid while avoiding obstacles. The visualizer is built using the Pygame library and displays the progress of the algorithm as it explores the grid.


## Features

* Interactive grid for placing start and end points, as well as obstacles
* Visual representation of the algorithm's progress as it searches for the shortest path
* Supports diagonal movement with proper cost calculation
* Clear and reset functionality for multiple runs

## How to Run

1. Install the Pygame library: pip install pygame
2. Run the script: python pathfinding_visualizer.py

## Controls

* Left-click: Place the start point, end point, or obstacles on the grid
* Right-click: Remove points or obstacles from the grid
* Spacebar: Run the A* algorithm
* 'C' key: Clear the grid and reset the visualizer

## Colors

* White: Empty grid cell
* Pink: Start point
* Lime: End point
* Black: Obstacle
* Light Blue: Unvisited node/node is in the open set
* Brown: Visited node
* Gold: Path

*This project was inspired by a [YouTube video](https://youtu.be/jl5yUEdekEM?t=331).*
