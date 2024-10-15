# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Kruskal's maze generator.
#
# __author__ = Tran Tuan Trung
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze import Maze
from maze.util import Coordinates
import random

class KruskalMazeGenerator():
    """
    Kruskal's algorithm maze generator
    """
    def generateMaze(self, maze):
        """
        Generate a maze using Kruskal's algorithm with a disjoint set.
        """

        # Initialize the parent and rank for each vertex
        vertices = maze.getVetrices()
        parent = {v: v for v in vertices}
        rank = {v: 0 for v in vertices}

        # Helper function: Find the root of the set containing 'vertex' with path compression
        def find(vertex):
            if parent[vertex] != vertex:
                parent[vertex] = find(parent[vertex])  # Path compression
            return parent[vertex]

        # Helper function: Union two sets based on rank
        def union(vert1, vert2):
            root1 = find(vert1)
            root2 = find(vert2)

            if root1 != root2:
                if rank[root1] > rank[root2]:
                    parent[root2] = root1
                elif rank[root1] < rank[root2]:
                    parent[root1] = root2
                else:
                    parent[root2] = root1
                    rank[root1] += 1

        # Get non-boundary edges within the maze
        edges = [edge for edge in maze.getEdges()
                if all(0 <= v.getRow() < maze.rowNum() and 0 <= v.getCol() < maze.colNum()
                        for v in edge[:2])]

        # Sort edges by their weights
        sortedEdges = sorted(edges, key=lambda e: maze.edgeWeight(e[0], e[1]))

        # Process edges in sorted order and create the maze
        for edge in sortedEdges:
            vert1, vert2, _ = edge

            # If vertices are in different sets, remove the wall between them and union them
            if find(vert1) != find(vert2):
                maze.removeWall(vert1, vert2)
                union(vert1, vert2)
            # If already connected, no action is taken
