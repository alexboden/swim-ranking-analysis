
class Team:
	"""
	Team class
 	"""

	def __init__(self, name):
		self.name = name
		self.swimmers = []
		self.points = 0
	
	def add_swimmer(self, swimmer):
		self.swimmers += [swimmer]
		self.points += swimmer.points
