from flask import (
    Flask, render_template, request, jsonify, 
    redirect, url_for, flash, session)
import time
import os
import pymongo
import random
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__) 

app.config['PREFERRED_URL_SCHEME'] = 'https'
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "loginInfo"
COLLECTION = "Users"
LIBRARY = "lib"
WORDS = "words"
#code to run main game

def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("mongo is connected")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("error") %e


conn = mongo_connect(MONGO_URI)

# two data base connections, coll is the main login sys, and lib is for all the libraries 
coll = conn[DATABASE][COLLECTION]
lib = conn[LIBRARY][WORDS]


def start_new_game(session):
    session['guesses_left'] = 7
    session['guessed_letters'] = ""
    session['correct_letters'] = ""
    session['game_over'] = 0
    session['database_word'] = ""


def hangman(guess, session):
    guesses_left = session['guesses_left']
    guessed_letters = session['guessed_letters']
    correct_letters = session['correct_letters']
    game_over = session['game_over']
    database_word = session['database_word']

    guessed_letters = guessed_letters + guess
    correct_letters = ""
    if guess not in database_word:
        guesses_left -= 1
        session['guesses_left'] = guesses_left
        if guesses_left == 0:
            session['game_over'] = 1
            return game_over

    for letter in database_word:
        if letter in guessed_letters:
            correct_letters += f"{letter} "
        else:
            correct_letters += "_ "

    session['correct_letters'] = correct_letters
    session['guessed_letters'] = guessed_letters
    print("cookie", session['correct_letters'])
    if all(letter in guessed_letters for letter in database_word):
        session['game_over'] = 2

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/updateButtons')
def updateButtons():
    guessed_letters = session.get('guessed_letters')
    return jsonify(guessed_letters)


@app.route('/button', methods=["POST"])
def buttonpress():
    data = request.json
    value = data['value']
    hangman(value, session)
    session.modified = True
    
    return jsonify({
    'status': 'success',
    'value_received': value,
})

@app.route('/gameboard')
def gameboard():
    time.sleep(0.1)
    correct_letters = session.get('correct_letters')
    print("gameboard", correct_letters)
    return render_template('gameboard.html', displayedLetters=correct_letters)


@app.route('/viewlib', methods=['GET', 'POST'])
def viewlib():
    titles = set()
    for item in lib.find({}):
        title = item.get("title")
        if title:
            titles.add(title)
    return render_template("viewlib.html", titles=titles)


@app.route('/start', methods=["POST"])
def start():
    start_new_game(session)
    title = request.form.get('title')
    wordSet = set()

    for item in lib.find({"title": title}):
        word = item.get("word")
        if word:
            wordSet.add(word)

    wordList = list(wordSet)
    if len(wordList) > 0:
        database_word = random.choice(wordList)
        session['database_word'] = database_word
        session['correct_letters'] = "_ " * len(database_word)
        return redirect(url_for("gameboard"))
    else:
        flash('No words exist in database', category="fail")
        return redirect(url_for("viewlib"))


@app.route('/updateimage', methods=["POST" , "GET"])
def update_image():
    guesses_left = session.get('guesses_left')
    return jsonify(guesses_left)


@app.route('/isGameOver', methods=["POST" , "GET"])
def game_over():
    game_over = session.get('game_over', False)
    return jsonify(game_over)


@app.route('/pass')
def passLevel():
    time.sleep(0.1)
    database_word = session.get('database_word', "")
    return render_template('pass.html', databaseWord=database_word)


@app.route('/fail')
def failLevel():
    time.sleep(0.1)
    database_word = session.get('database_word', "")
    return render_template('fail.html', databaseWord=database_word)




# used to login to the game
@app.route('/login', methods=["GET", "POST"])
def login():
    time.sleep(0.1)
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        usernameCheck = coll.find_one({"username": username,})
        if usernameCheck:
            if check_password_hash(usernameCheck["password"], password1):
                session["user"] = request.form.get("username")
                flash("Welcome Back! {}".format(request.form.get("username")), category='pass')
                return redirect(url_for("profile", username=session["user"]))
            else:
                flash("username and/or password is incorrect", category="fail")
        else:
            flash("account does not exist", category="fail")

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
        usernameCheck = coll.find_one({"username": username,})
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
            session["user"] = request.form.get("username")
            return redirect(url_for("profile", username=session["user"]))


    return render_template('signup.html', boolean=True)

# used to logout the game
@app.route("/logout")
def logout():
    flash("you have been logged out", category="pass")
    session.pop("user")
    return redirect(url_for("login"))

# Route for user profile
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
    word = request.form.get('word').lower()
    title = request.form.get('title')
    wordCheck = lib.find_one({'word': word, 'title': title,})
    newword = {
        "username": username,
        "word": word,
        "title": title, 
    }
    if wordCheck:
        flash('word is already in your library', category="fail")
    else:
        lib.insert_one(newword)
        print(newword)
    return redirect(url_for("userlibrary", username=session['user']))

# route to delete word in database
@app.route('/delword/', methods=['POST'])
def delword():
    word = request.form.get('word').lower()
    title = request.form.get('title')
    lib.delete_one({'word': word, 'title': title,})
    return redirect(url_for("userlibrary", username=session['user']))

#route to edit words in database
@app.route('/editword', methods=['POST'])
def editword():
    word = request.form.get('word').lower()
    word2 = request.form.get('word2').lower()
    title = request.form.get('title')
    wordCheck = lib.find_one({'word': word2, 'title': title,})
    if wordCheck:
        flash('word is already in your library', category="fail")
    else:
        lib.update_one({'word': word, 'title': title,}, {'$set': {'word': word2}})
        flash("word updated sucessfully", category="pass")
    return redirect(url_for("userlibrary", username=session['user']))

# route to add a new library to the database
@app.route('/addtitle', methods=["POST"])
def addtitle():
    username = session['user']
    word = request.form.get('word')
    title = request.form.get('title')
    wordCheck = lib.find_one({"title":title,})
    newword = {
        "username": username,
        "word": word,
        "title": title, 
    }
    if wordCheck:
        flash("title already exists please use another", category="fail")
    else:
        lib.insert_one(newword)
        flash("new Library created sucessfully", category="pass")
    return redirect(url_for("userlibrary", username=session['user']))








if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)