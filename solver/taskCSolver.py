# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Greedy maze solver for all entrance, exit pairs
#
# __author__ = Tran Tuan Trung
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.util import Coordinates
from maze.maze import Maze
import heapq
from typing import List
import itertools
from collections import defaultdict

class greedySolver:
    
    def __init__(self):
        """
        Initialize the solver's state.
        """
        self.all_solved = True                 # Flag to indicate if a solution was found
        self.entrance_exit_paths = {}           # Store entrance-exit paths
        self.blocked_cells = set()              # Track blocked cells to prevent overlapping paths
        self.counter = itertools.count()        # Tie-breaker for priority queue

    def solveMaze(self, maze, entrances, exits):
        """
        Solve the maze using a greedy approach (A*) to find non-overlapping paths.
        """
        distances = []

        # Solve the maze for each entrance-exit pair
        for entrance, exit in zip(entrances, exits):
            path = []
            priority_q = []
            parent = {}
            distance_map = defaultdict(lambda: float('inf'))
            distance_map[entrance] = 0

            # Push the entrance to the priority queue
            def heuristic(current_cell, target_cell):
                """Heuristic function (Manhattan distance) for A*."""
                return abs(current_cell.getRow() - target_cell.getRow()) + abs(current_cell.getCol() - target_cell.getCol())

            heapq.heappush(priority_q, (0 + heuristic(entrance, exit), next(self.counter), entrance))

            # Priority queue based A* search
            while priority_q:
                _, _, current = heapq.heappop(priority_q)

                # If goal is reached, reconstruct the path
                if current == exit:
                    curr_cell = exit
                    while curr_cell is not None:
                        path.append(curr_cell)
                        curr_cell = parent.get(curr_cell)
                    path.reverse()  # Reverse the path to go from start to end
                    break

                # Explore neighbors of the current cell
                for neighbor in maze.neighbours(current):
                    if neighbor not in self.blocked_cells and not maze.hasWall(current, neighbor):
                        g = distance_map[current] + maze.edgeWeight(current, neighbor)

                        if g < distance_map[neighbor]:
                            distance_map[neighbor] = g
                            parent[neighbor] = current
                            f = g + heuristic(neighbor, exit)
                            heapq.heappush(priority_q, (f, next(self.counter), neighbor))

            # If a valid path was found, mark the path and calculate its distance
            if path:
                total_dist = sum(maze.edgeWeight(path[i], path[i + 1]) for i in range(len(path) - 1))

                # Mark cells used in the path as blocked to prevent future paths from overlapping
                for cell in path:
                    self.blocked_cells.add(cell)

                self.entrance_exit_paths[(entrance, exit)] = path
                distances.append(total_dist)
            else:
                # No valid path found for this entrance-exit pair
                print(f"No valid path found for entrance [{entrance.getRow()}, {entrance.getCol()}] and exit [{exit.getRow()}, {exit.getCol()}] pair")
                self.all_solved = False
                break

        # If all paths were found, print the total distance
        if self.all_solved:
            print(f"Valid paths found with total distance: {sum(distances)}")

        return self.all_solved
