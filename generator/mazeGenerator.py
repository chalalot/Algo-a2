# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Base class for maze generator.
#
# __author__ = 'Jeffrey Chan' & 'Elham Naghizade'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze import Maze


from generator.recurBackGenerator import RecurBackMazeGenerator
from generator.kruskalGenerator import  KruskalMazeGenerator
from generator.noWallGenerator import NoWallMazeGenerator

class MazeGenerator:
	"""
	Base class for a maze generator.
	"""
	def __init__(self, genApproach):
		# This is used to indicate to program whether a maze been generated, or nothing has been done.
		# Need to set this to true once a maze is generated!
		self.m_mazeGenerated: bool = False

		if genApproach == 'recur':
			self.m_generator = RecurBackMazeGenerator()
		elif genApproach == 'kruskal':
			self.m_generator = KruskalMazeGenerator()
		elif genApproach == 'nowall':
			self.m_generator = NoWallMazeGenerator()
		else:
			raise ValueError(f"Unknown generation approach: {genApproach}")



	def generateMaze(self, maze:Maze):
		"""
	    Generates a maze.  Will update the passed maze.

		@param maze Maze which we update on to generate a maze. 
		"""
		
		self.m_generator.generateMaze(maze)
		self.m_mazeGenerated = True


	def isMazeGenerated(self):
		return self.m_mazeGenerated			

		