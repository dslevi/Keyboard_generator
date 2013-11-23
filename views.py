from flask import Flask, render_template, redirect, request, g, session, url_for, flash, jsonify
from model import User, Analytics, Prompts, Keyboard, Key, Text
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
import config
import forms
import model
import random
import genData
import time


app = Flask(__name__)
app.config.from_object(config)

# Stuff to make login easier
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# End login stuff

# Adding markdown capability to the app
Markdown(app)

@app.route("/")
def index():
    if session.get('user_id'):
        return redirect(url_for("display_user", user_id=session['user_id']))
    else:
        return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_newuser():
    email = request.form.get("email")
    user = User.query.filter_by(email=email).first()
    if user == None:
        name = request.form.get("name")
        age = request.form.get("age")
        occupation = request.form.get("occupation")
        password = request.form.get("password")
        v_password = request.form.get("verify_password")
        right_hand = (request.form.get("right_hand") == 'true')
        if password == v_password:
            flash("New user created")
            new_user = User(email=email, right_hand=right_hand, occupation=occupation, age=age, name=name)
            new_user.set_password(password)
            model.session.add(new_user)
            model.session.commit()
            return redirect(url_for("login"))
        else:
            flash("Passwords do not match")
            return redirect(url_for("register"))
    flash("User email already exists.")
    return redirect(url_for("register"))

@app.route("/login")
def login():
    session.clear()
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def authenticate():
    session.clear()
    form = forms.LoginForm(request.form)
    if not form.validate():
        flash("Incorrect username or password") 
        return render_template("login.html")

    email = form.email.data
    password = form.password.data

    user = User.query.filter_by(email=email).first()
    if not user or not user.authenticate(password):
        flash("Incorrect username or password") 
        return render_template("login.html")

    login_user(user)
    session['user_id'] = user.id
    return redirect(request.args.get("next", url_for("index")))

@app.route("/signout")
def signout():
    session.clear()
    flash("User signed out.")
    return redirect(url_for("login"))

#can condense?
@app.route("/keyboard", methods=["POST"])
def continue_keyboard():
    prompt = Prompts.query.get(random.randint(1, 227))
    input1 = request.form.get("input1")
    return render_template("keyboard.html", prompt=prompt.text, input1=input1)

@app.route("/keyboard")
def show_keyboard():
    prompt = Prompts.query.get(random.randint(1, 227))
    input1 = ""
    return render_template("keyboard.html", prompt=prompt.text, input1=input1)

@app.route("/input2", methods=["POST"])
def get_input2():
    text = Text.query.get(random.randint(1, 11))
    input1 = request.form.get("input1")
    return render_template("input2.html", text=text, input1=input1)

@app.route("/input3", methods=["POST"])
def get_input3():
    pattern = genData.makePattern()
    input1 = request.form.get("input1")
    input2 = request.form.get("input2")
    return render_template("input3.html", pattern=pattern, input1=input1, input2=input2)

@app.route("/analytics")
def no_analytics():
    if session.get('input1'):
        strokes = session['input1']
        input2 = session['input2']
        input3 = session['input3']
        keyboard = session['keyboard']
        keystrokes = genData.parseKeystrokes(strokes)
        freq = genData.keyFreq(keystrokes)
        mistakes = genData.keyMistakes(keystrokes)
        keytimes = genData.findKeytimes(keystrokes)
        bigrams = genData.findngrams(2, keytimes)
        trigrams = genData.findngrams(3, keytimes)
        dwelltimes = genData.dwellTime(keytimes)
        flighttimes = genData.flightTime(bigrams)
        fastflights = genData.definingTimes(3, flighttimes, True)
        fastdwell = genData.definingTimes(3, dwelltimes, True)
        slowflights = genData.definingTimes(3, flighttimes, False)
        slowdwell = genData.definingTimes(3, dwelltimes, False)
        return render_template("test.html", trigrams=trigrams, dwelltimes=dwelltimes, flighttimes=flighttimes, fastflights=fastflights, fastdwell=fastdwell,
        slowdwell=slowdwell, slowflights=slowflights, keyboard=keyboard, bigrams=bigrams, keytimes=keytimes, keystrokes=keystrokes, 
        freq=freq, mistakes=mistakes, input2=input2, input3=input3)

    if session.get('user_id'):
        user = User.query.filter_by(id=session['user_id']).first()
        analytics = user.analytics
        if len(analytics) > 0:
            strokes = analytics[-1].input1
            input2 = analytics[-1].input2
            input3 = analytics[-1].input3
            keystrokes = genData.parseKeystrokes(strokes)
            freq = genData.keyFreq(keystrokes)
            mistakes = genData.keyMistakes(keystrokes)
            keytimes = genData.findKeytimes(keystrokes)
            bigrams = genData.findngrams(2, keytimes)
            trigrams = genData.findngrams(3, keytimes)
            dwelltimes = genData.dwellTime(keytimes)
            flighttimes = genData.flightTime(bigrams)
            fastflights = genData.definingTimes(3, flighttimes, True)
            fastdwell = genData.definingTimes(3, dwelltimes, True)
            slowflights = genData.definingTimes(3, flighttimes, False)
            slowdwell = genData.definingTimes(3, dwelltimes, False)
            return render_template("test.html", trigrams=trigrams, dwelltimes=dwelltimes, flighttimes=flighttimes, fastflights=fastflights, fastdwell=fastdwell,
            slowdwell=slowdwell, slowflights=slowflights, keyboard=keyboard, bigrams=bigrams, keytimes=keytimes, keystrokes=keystrokes, 
            freq=freq, mistakes=mistakes)   
    return render_template("no_analytics.html")

def genName():
    rand_str = "".join(random.choice('ABCDEFGHIJKLMNOP1234567890') for i in range(10))
    return rand_str

@app.route("/analytics", methods=["POST"])
def show_analytics():
    strokes = request.form.get("input1")
    session['strokes'] = strokes
    input2 = request.form.get("input2")
    session['input2'] = input2
    input3 = request.form.get("input3")
    session['input3'] = input3
    keystrokes = genData.parseKeystrokes(strokes)
    freq = genData.keyFreq(keystrokes)
    mistakes = genData.keyMistakes(keystrokes)
    keytimes = genData.findKeytimes(keystrokes)
    bigrams = genData.findngrams(2, keytimes)
    trigrams = genData.findngrams(3, keytimes)
    dwelltimes = genData.dwellTime(keytimes)
    flighttimes = genData.flightTime(bigrams)
    fastflights = genData.definingTimes(3, flighttimes, True)
    fastdwell = genData.definingTimes(3, dwelltimes, True)
    slowflights = genData.definingTimes(3, flighttimes, False)
    slowdwell = genData.definingTimes(3, dwelltimes, False)
    visualKeyboard, keyboard = genData.createKeyboard(keystrokes)
    bigramtimes = genData.ngramTimes(bigrams)
    trigramtimes = genData.ngramTimes(trigrams)
    fastbigrams = genData.definingTimes(4, bigramtimes, True)
    slowbigrams = genData.definingTimes(4, bigramtimes, False)
    fasttrigrams = genData.definingTimes(4, trigramtimes, True)
    slowtrigrams = genData.definingTimes(4, trigramtimes, False)
    session['keyboard'] = keyboard
    session['visualKeyboard'] = visualKeyboard
    if session.get("user_id"):
        user_id = session['user_id']
        new_a = Analytics(input1=strokes, input2=input2, input3=input3, user_id=user_id)
        model.session.add(new_a)
        new_k = Keyboard(name=genName(), user_id=user_id)
        model.session.add(new_k)
        for i in range(len(keyboard)):
            key = Key(kb_id=new_k.id)
            key.location = keyboard[i][0]
            key.values = keyboard[i][1][0] + " " + keyboard[i][1][1]
            qwerty_key = Key.query.get(i + 1)
            key.code = qwerty_key.code
            new_k.keys.append(key)
        model.session.commit()
    else:
        user_id=None
    
    return render_template("test.html", trigrams=trigrams, dwelltimes=dwelltimes, flighttimes=flighttimes, fastflights=fastflights, fastdwell=fastdwell,
        slowdwell=slowdwell, slowflights=slowflights, keyboard=keyboard, bigrams=bigrams, keytimes=keytimes, keystrokes=keystrokes, 
        freq=freq, mistakes=mistakes, bigramtimes=bigramtimes, trigramtimes=trigramtimes, fastbigrams=fastbigrams, slowbigrams=slowbigrams,
        fasttrigrams=fasttrigrams, slowtrigrams=slowtrigrams)

@app.route("/pekl/<user_id>")
def view_pekl(user_id):
    if session.get('keyboard'):
        keyboard=session['keyboard']
        visualKeyboard = session['visualKeyboard']
        return render_template("pekl.html", keyboard=keyboard, visualKeyboard=visualKeyboard)
    return render_template("no_keyboard.html")

@app.route("/allusers")
def all_users():
    users = User.query.all()
    return render_template("all_users.html", users=users)

@app.route("/allkeyboards")
def all_keyboards():
    keyboards = Keyboard.query.all()
    return render_template("all_keyboards.html", keyboards=keyboards)

def json_keyboard(keys):
    l = []
    for key in keys:
        values = key.values.split()
        sublist = []
        sublist.append(key.location.encode('ascii', 'ignore'))
        if len(values) > 1:
            sublist.append([values[1].encode('ascii', 'ignore'), values[0].encode('ascii', 'ignore')])
        else:
            sublist.append(values)
        l.append(sublist)
    return l

@app.route("/keyboard/<keyboard_id>")
def display_keyboard(keyboard_id):
    keyboard = Keyboard.query.get(keyboard_id)
    date = time.strftime('%b %d, %Y %I:%M%p', keyboard.created_at.timetuple())
    keys = keyboard.keys
    values = []
    word_list = ["DELETE","TAB","SPACE","ENTER", "A", "B", "C", "O", "D", "E", 'F', 'G', 'H', 'J', 'I', 'L', 'K', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    if session.get('user_id'):
        session_id = session['user_id']
    else:
        session_id = None
    for key in keys:
        key_values = key.values
        tokens = key_values.split()
        if tokens[1] not in word_list: 
            values.append([tokens[1],tokens[0]])
        else:
            values.append([tokens[1]])
    jsonKeyboard = json_keyboard(keyboard.keys)
    text = Text.query.get(random.randint(1, 11))
    return render_template("display_keyboard.html", keyboard=keyboard, values=values, session_id=session_id, date=date, jsonKeyboard = jsonKeyboard, text=text)

@app.route("/keyboard/<keyboard_id>", methods=["POST"])
def rename_keyboard(keyboard_id):
    id = request.form.get('board_id')
    keyboard = Keyboard.query.get(id)
    if request.form.get('new_name'):
        keyboard.name = request.form.get('new_name')
        model.session.commit()
        return jsonify(result="name")
    user = User.query.get(session['user_id'])
    user.keyboard.append(keyboard)
    model.session.commit()
    return jsonify(result="add")

@app.route("/user/<user_id>")
def display_user(user_id):
    user = User.query.get(user_id)
    if session.get('user_id'):
        user_id = session['user_id']
    else:
        user_id = None
    return render_template("display_user.html", user=user, user_id=user_id)

@app.route("/edit/<board_id>", methods=['POST'])
def save_edits(board_id):
    keyboard = Keyboard.query.get(board_id)
    new = request.form.get('new_layout')
    if new == "":
        return jsonify(result="fail")
    d = {}
    tokens = new.encode('ascii', 'ignore').split()
    for token in tokens:
        k = token.split(":")
        d[k[0][1:]] = k[1][1:]
    for key in keyboard.keys:
        print "1 ", key.location, key.values
        prev = key.location
        key.location = d[prev]
        print "2 ", key.location, key.values
    model.session.commit()
    keyboard = Keyboard.query.get(board_id)
    for key in keyboard.keys:
        print "3 ", key.location, key.values
    return jsonify(result="edited")

@app.route("/edit/<board_id>")
def edit_board(board_id):
    keyboard = Keyboard.query.get(board_id)
    jsonKeyboard = json_keyboard(keyboard.keys)
    return render_template("edit_board2.html", keyboard=keyboard, jsonkeyboard=jsonKeyboard)



#still under construction...

@app.route("/remap")
def remap_keys():
    return render_template("construction.html")

@app.route("/logging")
def log_keys():
    return render_template("construction.html")

if __name__ == "__main__":
    app.run(debug=True)
