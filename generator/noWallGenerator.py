from maze.maze import Maze

class NoWallMazeGenerator():
    """
    Algorithm to generate a maze with no walls
    """
    def generateMaze(self, maze:Maze):
        # Get non-boundary edges 
        edges = [edge for edge in maze.getEdges() 
            if all(0 <= v.getRow() < maze.rowNum() and 0 <= v.getCol() < maze.colNum() 
                   for v in edge[:2])]
        
        for edge in edges:
            vert1, vert2, _ = edge
            maze.removeWall(vert1, vert2)
