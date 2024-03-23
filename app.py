from flask import Flask, render_template, request,  request, render_template_string, jsonify
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
# main function to run the game
def hangman(guess):
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
        update_image()
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


# used to create the connection for the home screen
@app.route('/')
def index():
    return render_template('index.html')

# updates the buttons to be removed when clicked
@app.route('/updateButtons')
def updateButtons():
    global eachGuessedLetter
    buttonsToUpdate = eachGuessedLetter
    return jsonify(buttonsToUpdate)


# used to grab a value from a button press to be used within the game
@app.route('/button', methods=["GET", "POST"])
def buttonpress():
    data = request.json
    value = data['value']
    hangman(value)
    return {'status': 'success', 'value_received': value}

# used to create the connection for the gameboard html
@app.route('/gameboard')
def gameboard():
    time.sleep(0.1)
    return render_template('gameboard.html', displayedLetters = correctLetters,)


# updates the image bases on how many guesses are left, sends the data to js for processing
@app.route('/update-image', methods=["GET", "POST"])
def update_image():
    global guessesLeft
    imageUpdate = guessesLeft
    return jsonify(imageUpdate)


if __name__ == "__main__":
    app.run(debug=True)
