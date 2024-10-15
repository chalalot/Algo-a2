# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Dijkstra's maze solver.
#
# __author__ =  Tran Tuan Trung
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from maze.util import Coordinates
from maze.maze import Maze
from typing import List
import heapq
import itertools
from collections import defaultdict
class DijkstraSolver:

    def __init__(self):
        """
        Initialize the state for the Dijkstra maze solver.
        """
        self.m_solverPath = []  # The full path visited by the solver, including backtracking
        self.m_cellsExplored = 0  # Count of cells explored during the solving process, excluding backtracking
        self.m_entranceUsed = None  # Entrance cell used by the solver
        self.m_exitUsed = None  # Exit cell found by the solver
        self.counter = itertools.count()  # Tie-breaker for priority queue with equal distances

    def solveMaze(self, maze, entrance):
        """
        Solve the maze using Dijkstra's algorithm, starting from 'entrance'.
        """
        exits = maze.getExits()
        pq = []
        self.m_entranceUsed = entrance  # Mark the entrance used
        heapq.heappush(pq, (0, next(self.counter), entrance))  # Push entrance into the priority queue

        distances = defaultdict(lambda: float('inf'))  # Dictionary to store the shortest distance to each cell
        distances[entrance] = 0  # Distance to the entrance is zero

        # To track the previous cell for path reconstruction
        previous_cell = {cell: None for cell in maze.getVetrices()}

        while pq:
            current_dist, _, current_cell = heapq.heappop(pq)

            # Stop if the current cell is an exit
            if current_cell in exits:
                self.m_exitUsed = current_cell
                break

            # Explore neighbors of the current cell
            for neighbor in maze.neighbours(current_cell):
                if not maze.hasWall(current_cell, neighbor):
                    new_dist = current_dist + maze.edgeWeight(current_cell, neighbor)

                    # Update distance if a shorter path is found
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        previous_cell[neighbor] = current_cell
                        heapq.heappush(pq, (new_dist, next(self.counter), neighbor))

            self.m_cellsExplored += 1  # Increment the explored cells count

        # Reconstruct the path from entrance to the exit
        self.m_solverPath = self.__reconstruct_path__(previous_cell, entrance, self.m_exitUsed)

    def __reconstruct_path__(self, previous_cell, start, end):
        """
        Reconstruct the path from the start to the end using the previous_cell tracking.
        """
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous_cell[current]
        return list(reversed(path))  # Return the path from start to end
