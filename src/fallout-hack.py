import sys, copy

def read_passwords():
	passwords = []

	print ('Enter the potential passwords.  When all the passwords have been entered, hit enter.')
	password = input('--> ')
	while password != '':
		passwords.append(password.upper())
		password = input('--> ')

	return passwords

def calculate_in_common(passwords):
	commonality = {}


	for outer in passwords:
		commonality[outer] = {}

		for inner in passwords:
			in_common = 0
			for i in range(0, len(outer)):
				if outer[i] == inner[i]:
					in_common += 1

			if in_common == len(outer):
				commonality[outer][inner] = None
			else:
				commonality[outer][inner] = in_common

	return commonality


def calculate_averages(commonality):
	averages = {}

	for password, others in commonality.items():
		sum = 0
		for inner, in_common in others.items():
			if in_common is None:
				continue
			sum += in_common
		if len(commonality.keys()) == 1:
			averages[password] = float(sum)
		else:
			averages[password] = float(sum) / float(len(commonality.keys()) - 1)

	return averages

def select_highest_average(averages):
	word = None
	max = None

	for password, avg in averages.items():
		if max is None or avg > max:
			word = password
			max = avg

	return word



def remove_impossible_matches(passwords, word, correct):
	new_passwords = []

	for password in passwords:
		in_common = 0
		for i in range(0, len(password)):
			if password[i] == word[i]:
				in_common += 1

		if in_common == correct:
			new_passwords.append(password)

	return new_passwords

def main():
	passwords = read_passwords()
	commonality = calculate_in_common(passwords)
	word = select_highest_average(calculate_averages(commonality))

	guesses_left = 4

	while guesses_left > 0:
		print ('Select', word, '(' + str(len(passwords)) + ' choices remaining)')
		correct = input('Number correct: ')

		if correct == '':
			print ('Done')
			sys.exit(0);
		else:
			correct = int(correct)
			if correct >= len(word):
				print ('Done')
				sys.exit(1)
			else:
				passwords = remove_impossible_matches(passwords, word, correct)
				if len(passwords) == 0:
					print ("All possibilities eliminated...")
					sys.exit(0)
				commonality = calculate_in_common(passwords)
				word = select_highest_average(calculate_averages(commonality))
				guesses_left -= 1


if __name__ == '__main__':
	main()
