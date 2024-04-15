from flask import Flask, render_template, request, render_template_string, jsonify, redirect, url_for, flash
import time
import sqlite3

app = Flask(__name__)  
app.secret_key = 'test'
DB_NAME = "database.db"

#code to run main game

databaseWord = "testwordc"
guessesLeft = 7
eachGuessedLetter = ""
correctLetters = ""
value = ""
gameOver = 0


for letter in databaseWord:
        correctLetters += "_"
        correctLetters += " "
# main function to run the game
def hangman(guess):
    global guessesLeft
    global eachGuessedLetter
    global correctLetters
    global gameOver
    eachGuessedLetter = eachGuessedLetter + guess
    correctLetters = ""
    if guess in databaseWord:
        print("Correct")
    else:
        guessesLeft -= 1
        print("wrong")
        update_image()
        if guessesLeft == 0:
            print("iwork")
            gameOver = 1
            return gameOver

    #storing guessed letters

    for letter in databaseWord:
        if letter in eachGuessedLetter:
            correctLetters += f"{letter}"
            correctLetters += " "

        else:
            correctLetters += "_"
            correctLetters += " "
    if all(letter in eachGuessedLetter for letter in databaseWord):
        gameOver = 2
        return gameOver
    
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
@app.route('/updateimage', methods=["GET", "POST"])
def update_image():
    global guessesLeft
    imageUpdate = guessesLeft
    return jsonify(imageUpdate)
# used to tell java if the game is running, passed or failed

@app.route('/isGameOver', methods=["GET", "POST"])
def game_over():
    global gameOver
    return jsonify(gameOver)

# used to tell the user they have won
@app.route('/pass')
def passLevel():
    time.sleep(0.1)
    return render_template('pass.html',)

# used to tell the user they have lost
@app.route('/fail')
def failLevel():
    time.sleep(0.1)
    return render_template('fail.html',)

# used to login to the game
@app.route('/login', methods=["GET", "POST"])
def login():
    time.sleep(0.1)
    data = request.form
    print(data)
    return render_template('login.html',)

# used to create a login for the game 
@app.route('/signup', methods=["GET", "POST"])
def signup():
    time.sleep(0.1)
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        query = "SELECT * FROM loginInfo WHERE email = ? "
        conn = sqlite3.connect('loginInfo.db') 
        cursor = conn.cursor() 
        cursor.execute(query, (email,))
        emailCheck = cursor.fetchone()

        if password1 != password2:
            flash('Passwords do not match', category='fail')
        elif len(password1) < 5:
            flash('Password must be longer than 5 characters', category='fail')
        elif emailCheck is not None:
            flash('Email exists in the database', category='fail')
        else:
            flash('Account created!', category='pass')
            cursor.execute("INSERT INTO loginInfo (name, email, password) VALUES (?, ?, ?)", ((name,), (email,), (password1,)))
            conn.commit() 
            conn.close() 
            return render_template('index.html')


    return render_template('signup.html', boolean=True)

if __name__ == "__main__":
    app.run(debug=True)
