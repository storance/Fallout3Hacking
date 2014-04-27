function FalloutSolver(passwords) {
    this.passwords = _.map(passwords, function(password) {
        return password.toUpperCase();
    });
    this.passwordsRemaining = _.clone(this.passwords);
    this.guessesRemaining = 4;
    this.finished = false;

    this.calculateCharsInCommonMatrix();
    this.calculateTotalCharsInCommonPerWord();
}

FalloutSolver.prototype.calculateCharsInCommonMatrix = function() {
    this.inCommonMatrix = {};

    _.each(this.passwords, function(password1, index) {
        this.addCharsInCommonForPasswordToMatrix(password1, password1, 0);

        _.each(_.rest(this.passwords, index+1), function (password2) {
            var inCommon = this.calculateCharsInCommon(password1, password2);
            this.addCharsInCommonForPasswordToMatrix(password1, password2, inCommon);
        }, this);
    }, this);
}

FalloutSolver.prototype.addCharsInCommonForPasswordToMatrix = function(password1, password2, inCommon) {
    inCommon = inCommon || 0;

    if (!(password1 in this.inCommonMatrix)) {
        this.inCommonMatrix[password1] = {};
    }
        
    if (!(password2 in this.inCommonMatrix)) {
        this.inCommonMatrix[password2] = {};
    }
        
    this.inCommonMatrix[password1][password2] = inCommon;
    this.inCommonMatrix[password2][password1] = inCommon;
}

FalloutSolver.prototype.calculateTotalCharsInCommonPerWord = function() {
    this.totalInCommonPerWord = {};
    _.each(this.passwordsRemaining, function (password) {
        this.totalInCommonPerWord[password] = _.reduce(this.passwordsRemaining, function(acc, otherPassword) {
            return acc + this.inCommonMatrix[password][otherPassword];
        }, 0, this);
    }, this);
}       

FalloutSolver.prototype.calculateCharsInCommon = function(word1, word2) {
    if (word1.length != word2.length) {
        return null;
    }
    
    var inCommon = 0;
    _.each(word1, function(ch, index) {
        if (ch == word2[index]) {
            inCommon++;
        }
    });

    return inCommon;
}

FalloutSolver.prototype.isActivePassword = function(word) {
    return this.passwordsRemaining.indexOf(word.toUpperCase()) > -1;
}

FalloutSolver.prototype.isFinished = function() {
    return this.finished;
}

FalloutSolver.prototype.firstChoice = function() {
    return this.selectPasswordWithMostInCommon();
}
        
FalloutSolver.prototype.nextChoice = function(wordChosen, correct) {
    this.removeImpossibleMatches(wordChosen.toUpperCase(), correct);

    this.guessesRemaining--;

    if (this.guessesRemaining == 0) {
        throw "All guesses have been used.";
    } else if (this.passwordsRemaining.length == 0) {
        throw "All passwords have been eliminated.";
    } else if (this.passwordsRemaining.length == 1) {
        this.finished = true;
        return this.passwordsRemaining[0];
    } else {
        return this.selectPasswordWithMostInCommon();
    }
}

FalloutSolver.prototype.removeImpossibleMatches = function (word, correct) {
    this.passwordsRemaining = _.filter(this.passwordsRemaining, function(password) {
        var inCommon = this.calculateCharsInCommon(word, password);

        return inCommon === correct;
    }, this);
    this.calculateTotalCharsInCommonPerWord();
}

FalloutSolver.prototype.selectPasswordWithMostInCommon = function() {
    return _.max(_.pairs(this.totalInCommonPerWord), function(entry) {
        return entry[1];
    })[0];
}