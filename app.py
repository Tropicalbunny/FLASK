from flask import (
    Flask, render_template, request, jsonify, 
    redirect, url_for, flash, session)
import time
import os
import pymongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__) 

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "loginInfo"
COLLECTION = "Users"
LIBRARY = "lib"
WORDS = "words"
#code to run main game

databaseWord = "testwordc"
guessesLeft = 7
eachGuessedLetter = ""
correctLetters = ""
value = ""
gameOver = 0
def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("mongo is connected")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("error") %e


conn = mongo_connect(MONGO_URI)


coll = conn[DATABASE][COLLECTION]
lib = conn[LIBRARY][WORDS]

documents = coll.find()

for doc in documents:
    print(doc)


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
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        usernameCheck = coll.find_one({"username": username.lower(),})
        if usernameCheck:
            if check_password_hash(usernameCheck["password"], password1):
                session["user"] = request.form.get("username").lower()
                flash("Welcome Back! {}".format(request.form.get("username")), category='pass')
                return redirect(url_for("profile", username=session["user"]))
            else:
                flash("username and/or password is incorrect", category="fail")


    return render_template('login.html',)


# used to create a login for the game 
@app.route('/signup', methods=["GET", "POST"])
def signup():
    time.sleep(0.1)
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        usernameCheck = coll.find_one({"username": username.lower(),})
        if password1 != password2:
            flash('Passwords do not match', category='fail')
        elif len(password1) < 5:
            flash('Password must be longer than 5 characters', category='fail')
        elif usernameCheck:
            flash('username exists in the database', category='fail') 
        else:
            flash('Account created!', category='pass')
            password = generate_password_hash(password1)
            newInfo = {
                    "name": name,
                    "username": username,
                    "password": password 
            }
            coll.insert_one(newInfo)
            session["user"] = request.form.get("username").lower()
            return redirect(url_for("profile", username=session["user"]))


    return render_template('signup.html', boolean=True)

# used to logout the game
@app.route("/logout")
def logout():
    flash("you have been logged out", category="pass")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/profile/<username>", methods=["GET","POST"])
def profile(username): 
    username = coll.find_one({"username": session["user"]})["username"]
    if session["user"]:
        return render_template("profile.html", username=session["user"])
    return redirect(url_for("login"))

#finds all the user assosiated libraries.
@app.route("/userlibrary/<username>", methods=["GET", "POST"])
def userlibrary(username):
    username = coll.find_one({"username": session["user"]})["username"]
    words = {}
    for item in lib.find({"username": session["user"]}):
        title = item["title"]
        word = item["word"]
        if title not in words:
            words[title] = []
        words[title].append(word)
    return render_template("userlibrary.html", username=session['user'], words=words )

#adding words to a library
@app.route('/addword', methods=["POST"])
def addword():
    username = session['user']
    word = request.form.get('word')
    title = request.form.get('title')
    newword = {
        "username": username,
        "word": word,
        "title": title, 
    }
    lib.insert_one(newword)
    print(newword)
    return redirect(url_for("userlibrary", username=session['user']))

@app.route('/delword/', methods=['POST'])
def delword():
    word = request.form.get('word')
    title = request.form.get('title')
    lib.delete_one({'word': word, 'title': title,})
    return redirect(url_for("userlibrary", username=session['user']))








if __name__ == "__main__":
    app.run(debug=True)
