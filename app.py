from flask import Flask, render_template, request,  request, render_template_string
import time

app = Flask(__name__)


#code to run main game

databaseWord = "testwordc"
guessesLeft = 7
eachGuessedLetter = ""
correctLetters = ""
value = ""

for letter in databaseWord:
        correctLetters += "_"
        correctLetters += " "
def hanmgan(guess):
    global guessesLeft
    global eachGuessedLetter
    global correctLetters
    eachGuessedLetter = eachGuessedLetter + guess
    correctLetters = ""
    if guess in databaseWord:
        print("Correct")
    else:
        guessesLeft -= 1
        print("wrong")
        if guessesLeft == 0:
            print("you lose")

    #storing guessed letters

    for letter in databaseWord:
        if letter in eachGuessedLetter:
            correctLetters += f"{letter}"
            correctLetters += " "

        else:
            correctLetters += "_"
            correctLetters += " "
    print(guessesLeft)
    print(eachGuessedLetter)



@app.route('/')
def index():
    return render_template('/index.html')


@app.route('/button', methods=["GET", "POST"])
def buttonpress():
    data = request.json
    value = data['value']
    hanmgan(value)
    # Call your Python function here with the value
    print(f'Button clicked with value: {value}')
    return {'status': 'success', 'value_received': value}

@app.route('/gameboard')
def gameboard():
    time.sleep(0.1)
    return render_template('/gameboard.html', displayedLetters = correctLetters)

if __name__ == "__main__":
    app.run(debug=True)
