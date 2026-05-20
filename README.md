# 8-puzzle-heuristic-solver

A Python command-line program that solves the classic 8-puzzle game using various Artificial Intelligence search algorithms. This project generates random, solvable starting states at specific difficulty depths and compares the efficiency and optimality of different search strategies.

## Features

* **State Generation:** Generates random starting board configurations at guaranteed solution depths using a reverse-BFS approach from the goal state.
* **Search Algorithms Implemented:**
  * **Breadth-First Search (BFS):** An uninformed search strategy that finds the optimal path but expands a massive number of nodes.
  * **Greedy Best-First Search:** An informed search strategy that prioritizes nodes closest to the goal, finding solutions quickly but not always optimally.
  * **A* Search (A-Star):** An optimal and complete informed search strategy combining the cost to reach the node and the estimated cost to the goal.
* **Heuristics Evaluated:**
  * **h1 (Misplaced Tiles):** Counts the number of tiles that are not in their goal position.
  * **h2 (Manhattan Distance):** Calculates the total grid distance each tile is away from its target position.
* **Performance Tracking:** Tracks and outputs the total number of node expansions (time complexity proxy) and final path lengths (optimality) for side-by-side comparison.

## How It Works

The board is represented as a 3x3 2D list, where `0` represents the blank space. The goal state is configured as:
```text
1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 0
