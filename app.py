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



@app.route('/')
def index():
    return render_template('/index.html')

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

@app.route('/gameboard')
def gameboard():
    time.sleep(0.1)
    return render_template('/gameboard.html', displayedLetters = correctLetters,)


# updates the image bases on how many guesses are left
@app.route('/update-image', methods=["GET", "POST"])
def update_image():
    global guessesLeft
    imageUpdate = guessesLeft
    if guessesLeft == 7:
        new_image_src = "/static/images/hang1.png" 
    elif guessesLeft == 6:
        new_image_src = "/static/images/hang2.png"
    elif guessesLeft == 5:
        new_image_src = "/static/images/hang3.png"
    elif guessesLeft == 4:
        new_image_src = "/static/images/hang4.png"
    elif guessesLeft == 3:
        new_image_src = "/static/images/hang5.png"
    elif guessesLeft == 2:
        new_image_src = "/static/images/hang6.png"
    elif guessesLeft == 1:
        new_image_src = "/static/images/hang7.png"
    else:
        new_image_src = "/static/images/hang8.png"
    
    return jsonify(imageUpdate)


if __name__ == "__main__":
    app.run(debug=True)
