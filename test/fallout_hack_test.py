'''
Created on Mar 13, 2011

@author: AgmMaverick
'''
import unittest
import fallout_hack

class FalloutHackTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testCalculateCharsInCommon(self):
        self.assertEqual(1, fallout_hack.FalloutHackSolver.calculateCharsInCommon("REPRIMANDING", "PARTNERSHIPS"))
        self.assertEqual(3, fallout_hack.FalloutHackSolver.calculateCharsInCommon("REPRIMANDING", "APPRECIATION"))
        self.assertEqual(1, fallout_hack.FalloutHackSolver.calculateCharsInCommon("REPRIMANDING", "CONVERSATION"))
        self.assertEqual(12, fallout_hack.FalloutHackSolver.calculateCharsInCommon("REPRIMANDING", "REPRIMANDING"))


    def testcalculateCharsInCommonMatrix(self):
        passwords = ['PARTNERSHIPS',
                     'REPRIMANDING',
                     'APPRECIATION',
                     'CONVERSATION']
        
        expectedInCommonMatrix = {
            'PARTNERSHIPS' : {
                     'PARTNERSHIPS' : 0,
                     'REPRIMANDING' : 1,
                     'APPRECIATION' : 1,
                     'CONVERSATION' : 1},
            'REPRIMANDING' : {
                     'PARTNERSHIPS' : 1,
                     'REPRIMANDING' : 0,
                     'APPRECIATION' : 3,
                     'CONVERSATION' : 1},
             'APPRECIATION' : {
                     'PARTNERSHIPS' : 1,
                     'REPRIMANDING' : 3,
                     'APPRECIATION' : 0,
                     'CONVERSATION' : 6},
             'CONVERSATION' : {
                     'PARTNERSHIPS' : 1,
                     'REPRIMANDING' : 1,
                     'APPRECIATION' : 6,
                     'CONVERSATION' : 0}}
        
        solver = fallout_hack.FalloutHackSolver(passwords)
        solver._calculateCharsInCommonMatrix()

        self.assertDictEqual(expectedInCommonMatrix, solver.inCommonMatrix)
        
    def testCalculateTotalCharsInCommonPerWord(self):
        expectedTotalInCommonByPassword = {
                     'PARTNERSHIPS' : 3,
                     'REPRIMANDING' : 5,
                     'APPRECIATION' : 10,
                     'CONVERSATION' : 8}
        
        passwords = ['PARTNERSHIPS',
                     'REPRIMANDING',
                     'APPRECIATION',
                     'CONVERSATION']
        
        solver = fallout_hack.FalloutHackSolver(passwords)
                
        self.assertDictEqual(expectedTotalInCommonByPassword, solver.totalInCommonPerWord)
        
    def testSelectPasswordWithMostInCommon(self):
        passwords = ['PARTNERSHIPS',
                     'REPRIMANDING',
                     'APPRECIATION',
                     'CONVERSATION']
        
        solver = fallout_hack.FalloutHackSolver(passwords)
        selectedPassword = solver._selectPasswordWithMostInCommon()
        
        self.assertEqual('APPRECIATION', selectedPassword)
        
    def testSelectPasswordWithMostInCommonWithPasswordsTied(self):
        passwords = ['PARTNERSHIPS',
                     'REPRIMANDING',
                     'APPRECIATION',
                     'CONVERSATION',
                     'PURIFICATION']
        
        solver = fallout_hack.FalloutHackSolver(passwords)
        
        solver.totalInCommonPerWord = {
                     'PARTNERSHIPS' : 3,
                     'REPRIMANDING' : 5,
                     'CONVERSATION' : 8,
                     'PURIFICATION' : 10,
                     'APPRECIATION' : 10,}
        
        # This should select the first one encountered in the dictionary
        selectedPassword = solver._selectPasswordWithMostInCommon()
        
        self.assertEqual('PURIFICATION', selectedPassword)
        
    def testRemoveImpossibleMatches(self):
        passwords = ['PARTNERSHIPS',
                     'REPRIMANDING',
                     'APPRECIATION',
                     'CONVERSATION',
                     'PURIFICATION']
        
        expectedRemainingPasswords = [
                     'APPRECIATION',
                     'CONVERSATION']
        
        solver = fallout_hack.FalloutHackSolver(passwords)
        solver._removeImpossibleMatches('PURIFICATION', 5)
        
        self.assertListEqual(expectedRemainingPasswords, solver.passwordsRemaining)
        
    def testSolver(self):
        passwords = ['PARTNERSHIPS',
             'REPRIMANDING',
             'APPRECIATION',
             'CONVERSATION',
             'CIRCUMSTANCE',
             'PURIFICATION',
             'SECLUSIONIST',
             'CONSTRUCTION',
             'DISAPPEARING',
             'TRANSMISSION',
             'APPREHENSIVE',
             'ENCOUNTERING']
        
        solver = fallout_hack.FalloutHackSolver(passwords)
        choice = solver.nextPasswordToChoose()
        
        self.assertEquals('APPRECIATION', choice)
        self.assertEquals(3, solver.guessesRemaining)
        
        choice = solver.nextPasswordToChoose(choice, 4)
        
        self.assertEquals(['CONSTRUCTION', 'TRANSMISSION'], solver.passwordsRemaining)
        self.assertEquals('TRANSMISSION', choice)
        self.assertEquals(2, solver.guessesRemaining)
        
        
    def testSolverWithRemoveChoice(self):
        passwords = ['PARTNERSHIPS',
             'REPRIMANDING',
             'APPRECIATION',
             'CONVERSATION',
             'CIRCUMSTANCE',
             'PURIFICATION',
             'SECLUSIONIST',
             'CONSTRUCTION',
             'DISAPPEARING',
             'TRANSMISSION',
             'APPREHENSIVE',
             'ENCOUNTERING']

        solver = fallout_hack.FalloutHackSolver(passwords)
        
        solver.removePassword('ENCOUNTERING')
        
        choice = solver.nextPasswordToChoose()
        
        self.assertEquals('APPRECIATION', choice)
        self.assertEquals(3, solver.guessesRemaining)
        
        choice = solver.nextPasswordToChoose(choice, 4)
        
        self.assertEquals(['CONSTRUCTION', 'TRANSMISSION'], solver.passwordsRemaining)
        self.assertEquals('TRANSMISSION', choice)
        self.assertEquals(2, solver.guessesRemaining)
        
    def testNextPasswordToChooseUppercasesWordChosen(self):
        passwords = ['PARTNERSHIPS',
             'REPRIMANDING',
             'APPRECIATION',
             'CONVERSATION',
             'CIRCUMSTANCE',
             'PURIFICATION',
             'SECLUSIONIST',
             'CONSTRUCTION',
             'DISAPPEARING',
             'TRANSMISSION',
             'APPREHENSIVE',
             'ENCOUNTERING']

        solver = fallout_hack.FalloutHackSolver(passwords)
        
        solver.removePassword('ENCOUNTERING')
        
        choice = solver.nextPasswordToChoose()
        
        self.assertEquals('APPRECIATION', choice)
        self.assertEquals(3, solver.guessesRemaining)
        
        choice = solver.nextPasswordToChoose(choice.lower(), 4)
        
        self.assertEquals(['CONSTRUCTION', 'TRANSMISSION'], solver.passwordsRemaining)
        self.assertEquals('TRANSMISSION', choice)
        self.assertEquals(2, solver.guessesRemaining)
        
    def testNextPasswordToChooseWithNoGuessesRemaining(self):
        passwords = ['PARTNERSHIPS',
             'REPRIMANDING',
             'APPRECIATION',
             'CONVERSATION',
             'CIRCUMSTANCE',
             'PURIFICATION',
             'SECLUSIONIST',
             'CONSTRUCTION',
             'DISAPPEARING',
             'TRANSMISSION',
             'APPREHENSIVE',
             'ENCOUNTERING']

        solver = fallout_hack.FalloutHackSolver(passwords)
        
        solver.nextPasswordToChoose()
        self.assertEquals(3, solver.guessesRemaining)
        solver.nextPasswordToChoose('REPRIMANDING', 4)
        self.assertEquals(2, solver.guessesRemaining)
        solver.nextPasswordToChoose('REPRIMANDING', 4)
        self.assertEquals(1, solver.guessesRemaining)
        solver.nextPasswordToChoose('REPRIMANDING', 4)
        self.assertEquals(0, solver.guessesRemaining)
        
        try:
            solver.nextPasswordToChoose('REPRIMANDING', 4)
            self.fail("Expected NoGuessesRemainingError to be thrown")
        except fallout_hack.NoGuessesRemainingError:
            #expected
            pass
        
    def testNextPasswordToChooseWithInvalidPassword(self):
        passwords = ['PARTNERSHIPS',
             'REPRIMANDING',
             'APPRECIATION',
             'CONVERSATION',
             'CIRCUMSTANCE',
             'PURIFICATION',
             'SECLUSIONIST',
             'CONSTRUCTION',
             'DISAPPEARING',
             'TRANSMISSION',
             'APPREHENSIVE',
             'ENCOUNTERING']

        solver = fallout_hack.FalloutHackSolver(passwords)
                
        try:
            solver.nextPasswordToChoose('WAFFLES', 4)
            self.fail("Expected ValueError to be thrown")
        except ValueError as inst:
            self.assertEqual("The password 'WAFFLES' is not one of the passwords", str(inst))
        
    def testNextPasswordToChooseWithNegativeCorrectValue(self):
        passwords = ['PARTNERSHIPS',
             'REPRIMANDING',
             'APPRECIATION',
             'CONVERSATION',
             'CIRCUMSTANCE',
             'PURIFICATION',
             'SECLUSIONIST',
             'CONSTRUCTION',
             'DISAPPEARING',
             'TRANSMISSION',
             'APPREHENSIVE',
             'ENCOUNTERING']

        solver = fallout_hack.FalloutHackSolver(passwords)
                
        try:
            solver.nextPasswordToChoose('REPRIMANDING', -1)
            self.fail("Expected ValueError to be thrown")
        except ValueError as inst:
            self.assertEqual("The number correct (-1) must be a positive integer", str(inst))
            
    def testNextPasswordToChooseWithTooLongCorrectValue(self):
        passwords = ['PARTNERSHIPS',
             'REPRIMANDING',
             'APPRECIATION',
             'CONVERSATION',
             'CIRCUMSTANCE',
             'PURIFICATION',
             'SECLUSIONIST',
             'CONSTRUCTION',
             'DISAPPEARING',
             'TRANSMISSION',
             'APPREHENSIVE',
             'ENCOUNTERING']

        solver = fallout_hack.FalloutHackSolver(passwords)
                
        try:
            solver.nextPasswordToChoose('REPRIMANDING', 13)
            self.fail("Expected NoGuessesRemainingError to be thrown")
        except ValueError as inst:
            self.assertEqual("The number correct (13) must be less than the passwords' length (12)", str(inst))
            
    def testPasswordPropertyWithPasswordsOfDifferingLengths(self):
        try:
            fallout_hack.FalloutHackSolver(['THE', 'QUICK', 'BROWN', 'FOX'])
            self.fail("Expected ValueError to be thrown")
        except ValueError as inst:
            self.assertEqual("All of the passwords must have the same length", str(inst))
            
    def testPasswordPropertyWithEmptyPassword(self):
        try:
            fallout_hack.FalloutHackSolver(['THE', '', 'BROWN', 'FOX'])
            self.fail("Expected ValueError to be thrown")
        except ValueError as inst:
            self.assertEqual("Empty string or None passwords are not allowed", str(inst))
            
    def testPasswordPropertyWithNonePassword(self):
        try:
            fallout_hack.FalloutHackSolver(['THE', None, 'BROWN', 'FOX'])
            self.fail("Expected ValueError to be thrown")
        except ValueError as inst:
            self.assertEqual("Empty string or None passwords are not allowed", str(inst))
            
    def testPasswordPropertyUppercasesAllPassword(self):
        expectedPasswords = ['PARTNERSHIPS',
                             'REPRIMANDING',
                             'APPRECIATION',
                             'CONVERSATION',
                             'PURIFICATION']
        
        passwords = ['pARtNErsHiPS',
                     'REpRimANdINg',
                     'APpREcIaTIoN',
                     'CoNvERsATiON',
                     'purification']

        solver = fallout_hack.FalloutHackSolver(passwords)
        
        self.assertListEqual(expectedPasswords, solver.passwords)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()