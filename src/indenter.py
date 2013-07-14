"""
  indenter.py
  by David Weinman
  6/22/13, 12:05p
"""

"""
indentation object for net printout
"""
class indenter():
	indenterUnit = ''
	outputString = ''

	def __init__(self, unit):
		self.indenterUnit = unit
		self.outputString = ''

	# makes it bigger
	def increment(self):
		self.outputString = self.outputString + self.indenterUnit
		return self.outputString

	# returns current string
	def currentString(self):
		return self.outputString

	# makes it smaller
	def decrement(self):
		self.outputString = self.outputString[0:(len(self.outputString) - len(self.indenterUnit))]
		return self.outputString

