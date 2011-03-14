import sys, copy

TOTAL_GUESSES_ALLOWED = 4

class NoGuessesRemainingError(Exception):
	def __repr__(self):
		return 'You have exceeded the number of allowed guesses'
	
class AllPasswordsEliminatedError(Exception):
	def __repr__(self):
		return 'All passwords have been eliminated'

class FalloutHackSolver():
	@staticmethod
	def calculateCharsInCommon(word1, word2):
		if len(word1) != len(word2):
			raise ValueError("The two words given must be identical length")
		
		inCommon = 0
		for i in range(0, len(word1)):
			if word1[i] == word2[i]:
				inCommon += 1
				
		return inCommon
	
	def __init__(self, passwords):
		self.passwords = passwords
		self.guessesRemaining = TOTAL_GUESSES_ALLOWED
		self.inCommonMatrix = None
		self.totalInCommonPerWord = None
		self._calculateTotalCharsInCommonPerWord()
		
	@property
	def passwords(self):
		return self._passwords
	
	@passwords.setter
	def passwords(self, newPasswords):
		if newPasswords is None:
			newPasswords = []
		
		self._passwords = []
		self.passwordsRemaining = []
		self.passwordsLength = None
		for password in newPasswords:
			if password is None or len(password) == 0:
				raise ValueError('Empty string or None passwords are not allowed')
			
			if self.passwordsLength is None:
				self.passwordsLength = len(password)
			elif len(password) != self.passwordsLength:
				raise ValueError('All of the passwords must have the same length')
			
			self._passwords.append(password.upper())
			self.passwordsRemaining.append(password.upper())
		
		self._calculateTotalCharsInCommonPerWord()
		
	def _addCharsInCommonForPasswordToMatrix(self, password1, password2=None, inCommon=None):
		if password1 not in self.inCommonMatrix:
			self.inCommonMatrix[password1] = {}
		
		if password2 is None:
			self.inCommonMatrix[password1][password1] = 0
		else:
			if password2 not in self.inCommonMatrix:
				self.inCommonMatrix[password2] = {}
		
			self.inCommonMatrix[password1][password2] = inCommon
			self.inCommonMatrix[password2][password1] = inCommon
		
	
	def _calculateCharsInCommonMatrix(self):
		self.inCommonMatrix = {}
		
		passwordsRemaining = copy.copy(self.passwordsRemaining)
		
		for password1 in self.passwordsRemaining:
			self._addCharsInCommonForPasswordToMatrix(password1)
	
			passwordsRemaining.remove(password1)
				
			for password2 in passwordsRemaining:
				inCommon = self.calculateCharsInCommon(password1, password2)
				self._addCharsInCommonForPasswordToMatrix(password1, password2, inCommon)
	
			if len(passwordsRemaining) == 0:
				break
	
	def _calculateTotalCharsInCommonPerWord(self):
		self._calculateCharsInCommonMatrix()
		
		self.totalInCommonPerWord = {}
	
		for password, others in self.inCommonMatrix.items():
			self.totalInCommonPerWord[password] = 0
			for inCommon in others.values():
				self.totalInCommonPerWord[password] += inCommon
					
	def _selectPasswordWithMostInCommon(self):
		word = None
		max = None
	
		for password, total in self.totalInCommonPerWord.items():
			if max is None or total > max:
				word = password
				max = total
	
		return word
	
	def _removeImpossibleMatches(self, word, correct):
		trimmedPasswords = []
	
		for password in self.passwordsRemaining:
			inCommon = self.calculateCharsInCommon(word, password)
			
			if inCommon == correct:
				trimmedPasswords.append(password)
	
		self.passwordsRemaining = trimmedPasswords
		self._calculateTotalCharsInCommonPerWord()
		
	def nextPasswordToChoose(self, wordChosen=None, correct=None):
		if wordChosen is not None:
			wordChosen = wordChosen.upper()
			if wordChosen not in self.passwords:
				raise ValueError("The password '" + wordChosen + "' is not one of the passwords")
			
			if correct < 0:
				raise ValueError("The number correct (" + str(correct) + ") must be a positive integer")
			
			if correct > self.passwordsLength:
				raise ValueError("The number correct (" + str(correct) + ") must be less than the passwords' length (" + str(self.passwordsLength) + ")")
			self._removeImpossibleMatches(wordChosen, correct)
			
			
		if len(self.passwordsRemaining) == 0:
			raise AllPasswordsEliminatedError()
			
		if not self.hasGuessesRemaining():
			raise NoGuessesRemainingError()
		
		self.guessesRemaining -= 1
		
		return self._selectPasswordWithMostInCommon()
		
	def hasGuessesRemaining(self):
		return self.guessesRemaining > 0
		
	def addGuess(self):
		self.guessesRemaining += 1
	
	def removePassword(self, password):
		self.passwordsRemaining.remove(password)
		self._calculateTotalCharsInCommonPerWord()
		
			
def readPasswords():
	passwords = []

	print ('Enter the potential password choices (leave blank when done)')
	password = input('--> ').strip()
	while password != '':
		passwords.append(password.upper())
		password = input('--> ').strip()

	return passwords

def main():
	passwords = readPasswords()
	
	solver = FalloutHackSolver(passwords)
	
	choice = solver.nextPasswordToChoose()
	while solver.hasGuessesRemaining():
		print ('Select', choice, '(' + str(len(solver.passwordsRemaining)) + ' choice(s) remaining)')
		
		correct = input('Number correct: ').strip()
		if correct == '':
			print ('Done')
			return 0
		
		
		
		try:
			correct = int(correct)
			
			if correct >= len(choice):
				print ('Done')
				return 0
			
			choice = solver.nextPasswordToChoose(choice, correct)
		except ValueError as inst:
			print(str(inst), file=sys.stderr)
			
if __name__ == '__main__':
	main()

