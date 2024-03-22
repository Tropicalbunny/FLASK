from flask import Flask, render_template

app = Flask(__name__)


#code to run main game

databaseWord = "testword"
guessesLeft = 7
eachGuessedLetter = ""
correctLetters = ""

while guessesLeft != 0:
    guess = "hi"

    if guess in databaseWord:
        print("Correct")
    else:
        guessesLeft -= 1
        print("wrong")

    #storing guessed letters
    eachGuessedLetter = eachGuessedLetter + guess
    correctLetters = ""
    for letter in databaseWord:
        if letter in eachGuessedLetter:
            correctLetters += f"{letter}"
            correctLetters += " "
        else:
             correctLetters += "_"
             correctLetters += " "




@app.route('/')
def index():
    return render_template('/index.html')
@app.route('/gameboard')
def gameboard():
    return render_template('/gameboard.html', displayedLetters = correctLetters)

if __name__ == "__main__":
    app.run(debug=True)
