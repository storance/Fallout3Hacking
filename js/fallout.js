var app = angular.module('Fallout3Hacking',[]);
app.directive('xngFocus', function($timeout) {
    return function(scope, element, attrs) {
        scope.$watch(attrs.xngFocus, 
            function (newValue) {
                if (newValue) {
                    $timeout(function() {
                        element.focus()
                    });
                }
            },true);
        };    
});

app.controller("FalloutCtrl", function($scope, $timeout, $filter) {
    $scope.error = "";
    $scope.words = [];
    $scope.wordsLength = 0;
    $scope.addWordText = "";
    $scope.addWordError = "";
    $scope.solver = null;
    $scope.choice = {
        value : "",
        correct: "",
        recommended : "",
        error : ""
    };
    $scope.choiceHistory = [];

    $scope.focusAddButton = function() {
        $('#addWord').focus();
    }

    $scope.addWord = function() {
        if ($scope.addWordText.length > 0) {
            if ($scope.wordsLength > 0 && $scope.addWordText.length != $scope.wordsLength) {
                $scope.addWordError = "Must be the same length (" + $scope.wordsLength + ") as all other words.";
                return;
            }

            $scope.words.push({ value: $scope.addWordText, active: true, edit: false, error: ""})
            $scope.wordsLength = $scope.addWordText.length;
            $scope.addWordText = "";
            $scope.addWordError = "";
            $scope.focusAddButton();
        }
    }

    $scope.editWord = function(index, $event) {
        $scope.disableWordEditing();

        $scope.words[index].edit = true;
    }

    $scope.disableWordEditing = function() {
        _.each($scope.words, function(word) {
            word.edit = false;
        });
    }

    $scope.deleteWord = function(index) {
        $scope.words.splice(index, 1)
    }

    $scope.clearWords = function() {
        $scope.words = [];
    }

    $scope.validateWord = function(index) {
        if ($scope.words[index].value.length != $scope.wordsLength) {
            $scope.words[index].error = "Must be the same length (" + $scope.wordsLength + ") as all other words.";
        } else {
            $scope.words[index].error = "";
        }
    }

    $scope.validateChoice = function() {
        if ($scope.choice.correct === "") {
            $scope.choice.error = "Enter a valid number a valid number between 0 and " + $scope.wordsLength + ".";
        }

        var correct = parseInt($scope.choice.correct);
        if (isNaN(correct)) {
            $scope.choice.error = "Enter a valid number a valid number between 0 and " + $scope.wordsLength + ".";
        } else if (correct < 0 || correct > $scope.wordsLength) {
            $scope.choice.error = "Enter a valid number a valid number between 0 and " + $scope.wordsLength + ".";
        } else {
            $scope.choice.error = "";
        }
    }

    $scope.callOnEnter = function(event, func) {
        if (event.keyCode == 13) {
            func();
        }
    }

    $scope.startSolve = function() {
        $scope.solver = new FalloutSolver(_.pluck($scope.words, 'value'));
        var choice = $scope.solver.firstChoice();
        $scope.setChoice(choice, true);
    }

    $scope.nextChoice = function() {
        $scope.validateChoice();
        if ($scope.choice.error !== "") {
            return;
        }

        var correct = parseInt($scope.choice.correct)
        $scope.choiceHistory.push({value : $scope.choice.value, correct: correct});

        var choice = $scope.solver.nextChoice($scope.choice.value, correct);
        $scope.setChoice(choice, true);

        _.each(this.words, function(word) {
            if (!this.solver.isActivePassword(word.value)) {
                word.active = false;
            }
        }, this);
    }

    $scope.isSelectedChoice = function(word) {
        if (!$scope.solver || !$scope.choice) {
            return false;
        }

        return !$scope.solver.isFinished() && word.value.toUpperCase() === $scope.choice.value.toUpperCase();
    }

    $scope.isRecommendedChoice = function(word) {
        if (!$scope.solver || !$scope.choice.recommended) {
            return false;
        }

        return !$scope.solver.isFinished() && word.value.toUpperCase() === $scope.choice.recommended.toUpperCase();
    }

    $scope.isAnswer = function(word) {
        if (!$scope.solver || !$scope.choice.recommended) {
            return false;
        }

        return $scope.solver.isFinished() && word.value.toUpperCase() === $scope.choice.recommended.toUpperCase();
    }

    $scope.setChoice = function(word, recommended) {
        var isActive = _.any($scope.words, function(otherWord) {
           return word.toUpperCase() === otherWord.value.toUpperCase() && otherWord.active;
        });

        if (!$scope.isSolveStarted() && !isActive) {
            return;
        }

        console.log("setChoice(" + word + ", " + recommended + ")");

        var recommendedWord = $scope.choice.recommended;
        if (recommended) {
            recommendedWord = word; 
        }

        $scope.choice = {
            value : word,
            correct : "",
            error : "",
            recommended: recommendedWord
        }
    }

    $scope.showEditWords = function() {
        return !$scope.isSolveStarted() && $scope.words.length > 0;
    }

    $scope.showSolveButton = function() {
        return !$scope.isSolveStarted() && this.error === "" && _.every(this.words, function(word) {
            return word.error === "";
        });
    }

    $scope.isSolveStarted = function() {
        return $scope.solver !== null;
    }

    $scope.bulkAddText = "";

    $scope.bulkAdd = function() {
        _.each($scope.bulkAddText.split("\n"), function (word) {
            this.words.push({value: word, active: true, edit: false, error: ""});
            this.wordsLength = word.length;
        }, this);
    }

    $scope.focusAddButton();
});
