"""
  indenter.py
  by David Weinman
  6/22/13, 12:05p

---
Contains a class for indenting training
printouts to the command line.
"""

"""
This file is licensed under the MIT License, see LICENSE for details.
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

