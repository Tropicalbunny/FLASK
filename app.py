from flask import Flask, render_template, request,  request, render_template_string

app = Flask(__name__)


#code to run main game

databaseWord = "testwordc"
guessesLeft = 7
eachGuessedLetter = ""
correctLetters = ""
value = ""


def hanmgan(guess):
    global guessesLeft
    global eachGuessedLetter
    if guess in databaseWord:
        print("Correct")
    else:
        guessesLeft -= 1
        print("wrong")
        if guessesLeft == 0:
            print("you lose")

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
    print(guessesLeft)



@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/gameboard')
def gameboard():
    return render_template('/gameboard.html', displayedLetters = correctLetters)

@app.route('/button', methods=["GET", "POST"])
def buttonpress():
    data = request.json
    value = data['value']
    hanmgan(value)
    # Call your Python function here with the value
    print(f'Button clicked with value: {value}')
    return {'status': 'success', 'value_received': value}

if __name__ == "__main__":
    app.run(debug=True)
