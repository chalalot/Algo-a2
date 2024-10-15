# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Brute force maze solver for all entrance, exit pairs
#
# __author__ = Tran Tuan Trung
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.util import Coordinates
from maze.maze import Maze

from typing import List, Tuple
from itertools import product


class bruteForceSolver:
    def __init__(self):
        """
        Initialize the solver's state.
        """
        self.best_paths = None               # Best set of non-overlapping paths
        self.min_valid_distance = float('inf')  # Track the minimum total distance of valid paths
        self.all_solved = False                 # Flag to indicate whether a solution was found
        self.entrance_exit_paths = {}           # Dictionary of entrance-exit paths

    def solveMaze(self, maze, entrances, exits):
        """
        Solve the maze using brute-force to find non-overlapping paths from multiple entrances to exits.
        """
        passed_cells = set()  # Cells that have been passed
        all_pairs_paths = []  # To store all possible paths for each entrance-exit pair

        # Generate paths for all entrance-exit pairs
        for entrance, exit in zip(entrances, exits):
            paths = []
            
            # DFS helper to explore paths
            def dfs(current_cell, target_cell, path, dist):
                if current_cell == target_cell:
                    paths.append((path.copy(), dist))
                    return
                
                for neighbor in maze.neighbours(current_cell):
                    if neighbor not in passed_cells and not maze.hasWall(current_cell, neighbor) and neighbor not in path:
                        path.append(neighbor)
                        new_dist = dist + maze.edgeWeight(current_cell, neighbor)
                        dfs(neighbor, target_cell, path, new_dist)
                        path.pop()  # Backtrack
            
            # Start DFS from entrance to exit
            dfs(entrance, exit, [entrance], 0)

            if not paths:
                print(f"No valid path found for entrance [{entrance.getRow()}, {entrance.getCol()}] and exit [{exit.getRow()}, {exit.getCol()}] pair")
                return False
            
            all_pairs_paths.append(paths)

        # Brute-force check on all combinations of paths
        min_dist = float('inf')
        best_combination = None
        
        for combination in product(*all_pairs_paths):
            temp_passed_cells = set()
            total_dist = 0
            valid = True

            for path, dist in combination:
                if any(cell in temp_passed_cells for cell in path):  # Check for overlap
                    valid = False
                    break
                
                temp_passed_cells.update(path)
                total_dist += dist

            if valid and total_dist < self.min_valid_distance:
                min_dist = total_dist
                best_combination = combination

        # Update the best solution if found
        if best_combination:
            self.min_valid_distance = min_dist
            self.best_paths = best_combination
            self.entrance_exit_paths = {(entrances[i], exits[i]): path for i, (path, _) in enumerate(best_combination)}
            self.all_solved = True
            print(f"Valid paths found with total distance: {self.min_valid_distance}")
        
        return self.all_solved
