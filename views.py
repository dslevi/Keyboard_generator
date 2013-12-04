from flask import Flask, render_template, redirect, request, g, session, url_for, flash, jsonify
from model import User, Analytics, Prompts, Keyboard, Key, Text, TestAnalytic
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
import config
import forms
import model
import random
import genData, genetic2
import time
import json

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
    prompt = Prompts.query.get(random.randint(1, 172))
    input1 = request.form.get("input1")
    return render_template("keyboard.html", prompt=prompt.text, input1=input1)

@app.route("/keyboard")
def show_keyboard():
    prompt = Prompts.query.get(random.randint(1, 172))
    input1 = ""
    return render_template("keyboard.html", prompt=prompt.text, input1=input1)

@app.route("/input2", methods=["POST"])
def get_input2():
    text = Text.query.get(random.randint(1, 11))
    input1 = request.form.get("input1")
    return render_template("input2.html", text=text, input1=input1)

def genName():
    rand_str = "".join(random.choice('ABCDEFGHIJKLMNOP1234567890') for i in range(10))
    return rand_str

@app.route("/analytics", methods=["POST"])
def show_analytics():
    input1 = request.form.get("input1")
    input2 = request.form.get("input2")
    m = request.form.get("mistakes")

    keystrokes = genData.parseKeystrokes(input1)
    freq = genData.keyFreq(keystrokes)
    keys = genData.makeKeys(keystrokes)
    keytimes = genData.findKeytimes(keystrokes)
    hands, fingers = genData.handFingerFreq(keytimes)
    distance = genData.distance(keytimes)

    dwelltimes = genData.dwellTime(keytimes)
    fastdwell = genData.definingTimes(3, dwelltimes, True)
    slowdwell = genData.definingTimes(3, dwelltimes, False)

    bigrams = genData.findngrams(2, keytimes)
    bigramtimes = genData.ngramTimes(bigrams)
    fastbigrams = genData.definingTimes(4, bigramtimes, True)
    slowbigrams = genData.definingTimes(4, bigramtimes, False)
    biAtt = genData.biAttributes(bigrams)
    fast = genData.fastestTimes(len(bigramtimes)/2, bigramtimes)
    att = genData.definingAtt(biAtt[3])

    flighttimes = genData.flightTime(bigrams)
    fastflights = genData.definingTimes(3, flighttimes, True)
    slowflights = genData.definingTimes(3, flighttimes, False)

    mistakes = genData.keyMistakes(m)
    mostmistakes = genData.definingTimes(3, mistakes, True)
    accuracy, wpm = genData.keyAccuracy(request.form.get("mistakes"), request.form.get("text"), request.form.get("time"))

    if session.get("user_id"):
        user_id = session['user_id']
        new_a = Analytics(input1=input1, input2=input2, user_id=user_id, mistakes=m, accuracy=accuracy, wpm=wpm)
        model.session.add(new_a)
        model.session.commit()

    return render_template("test.html", fastflights=fastflights, fastdwell=fastdwell, slowdwell=slowdwell, slowflights=slowflights, 
        freq=freq, fastbigrams=fastbigrams, slowbigrams=slowbigrams, mostmistakes=mostmistakes, biAtt=biAtt, att=att, keys=keys, 
        fast=fast, accuracy=accuracy, wpm=wpm, hands=hands, fingers=fingers, distance=distance, input1=input1)

@app.route("/genetic/")
def genetic():
    f = request.args.get('f')
    a = request.args.get('a')
    k = request.args.get('k')

    fast = json.loads(f)
    keys = json.loads(k)
    att = json.loads(a)

    layout  = genetic2.main(fast, att, keys)

    print layout

    l = layout[0][0]

    if session.get("user_id"):
        new_k = Keyboard(name=genName(), user_id=session['user_id'])
        model.session.add(new_k)
        model.session.commit()
        for i in range(len(l)):
            key = Key(kb_id=new_k.id)
            key.location = l[i][0]
            key.values = l[i][1][0] + " " + l[i][1][1]
            qwerty_key = Key.query.get(i + 1)
            key.code = qwerty_key.code
            model.session.add(key)
            new_k.keys.append(key)
        user = User.query.get(session['user_id'])
        a = user.analytics[-1]
        a.kd_id = new_k.id
        print new_k.id
        model.session.commit()

    return jsonify(result=l)

@app.route("/pekl", methods=['POST'])
def view_pekl():
    f = request.form.get('fast')
    a = request.form.get('att')
    k = request.form.get('keys')
    return render_template("pekl.html", f=f, a=a, k=k)

@app.route("/search")
def search():
    keyboards = Keyboard.query.all()
    users = User.query.all()
    return render_template("search.html", keyboards=keyboards, users=users)

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

def sortKeys(k):
    sorted_k = []
    h = []
    for j in k:
        h.append(j.location)
    h = sorted(h)
    for i in range(len(h)):
        for j in range(len(k)):
            if k[j].location == h[i]:
                sorted_k.append(k[j])
    return sorted_k

@app.route("/keyboard/<keyboard_id>")
def display_keyboard(keyboard_id):
    keyboard = Keyboard.query.get(keyboard_id)
    date = time.strftime('%b %d, %Y %I:%M%p', keyboard.created_at.timetuple())
    k = keyboard.keys
    keys = sortKeys(k)
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
    jsonKeyboard = json_keyboard(keys)
    text = Text.query.get(random.randint(1, 11))
    return render_template("display_keyboard.html", keyboard=keyboard, values=values, session_id=session_id, date=date, jsonKeyboard = jsonKeyboard, 
        text=text)

@app.route("/keyboard/<keyboard_id>", methods=["POST"])
def rename_keyboard(keyboard_id):
    keyboard = Keyboard.query.get(keyboard_id)
    user = User.query.get(session['user_id'])
    new_k = Keyboard(name=keyboard.name, user_id=user.id)
    model.session.add(new_k)
    for key in keyboard.keys:
        new_key = Key(kb_id=new_k.id, location=key.location, values=key.values, code=key.code)
        new_k.keys.append(new_key)
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
def save_name(board_id):
    keyboard = Keyboard.query.get(board_id)
    keyboard.name = request.form.get('new_name')
    model.session.commit()
    return jsonify(result="name")

@app.route("/savelayout/<board_id>", methods=['POST'])
def save_edits(board_id):
    new = json.loads(request.form['new_layout'])
    t = {}
    for key in new:
        k = Key.query.get(int(key))
        prev = k.location
            
        if prev != new[key][1:]:
            k.location = new[key][1:]
        t[k.id] = [k.location, k.values]
        model.session.add(k)
    model.session.commit()
    return redirect(url_for("edit_board", board_id=board_id))

def json_keyboard2(keys):
    l = []
    for key in keys:
        l.append({
            'id': key.id,
            'location': key.location,
            'val1': key.values.split()[1],
            'val2': key.values.split()[0]
        })
    return l

@app.route("/edit/<board_id>")
def edit_board(board_id):
    keyboard = Keyboard.query.get(board_id)
    jsonKeyboard = json_keyboard2(keyboard.keys)
    return render_template("edit_board2.html", keyboard=keyboard, jsonkeyboard=jsonKeyboard)

@app.route("/delete/<board_id>")
def delete_board(board_id):
    keyboard = Keyboard.query.get(board_id)
    for key in keyboard.keys:
        model.session.delete(key)
    model.session.delete(keyboard)
    model.session.commit()
    return redirect(url_for("display_user", user_id=session['user_id']))

@app.route("/testanalytics/<keyboard_id>", methods=['POST'])
def test_analytics(keyboard_id):
    keyboard = Keyboard.query.get(keyboard_id)

    if request.form.get('time'):
        
        t = request.form.get('time')
        text = request.form.get('text')
        mistakes = request.form.get('mistakes')
        acc, w = genData.keyAccuracy(mistakes, text, t)

        if (len(keyboard.tests) == 0) or (acc!= keyboard.tests[-1].accuracy and w != keyboard.tests[-1].wpm):
            a = TestAnalytic(accuracy=acc, wpm=w, keyboard_id=keyboard_id)
            model.session.add(a)
            model.session.commit()

    tests = keyboard.tests
    t = []

    if (len(tests) > 0):
        for test in tests:
            t.append([test.accuracy, test.wpm, time.strftime('%m/%d/%y %I:%M%p', test.created_at.timetuple())])
        tests = t

    if (len(keyboard.analytics) > 0):
        analytics = Analytics.query.filter_by(kd_id=keyboard_id).one()
        input1 = analytics.input1
        input2 = analytics.input2
        m = analytics.mistakes
        accuracy = analytics.accuracy
        wpm = analytics.wpm

        keystrokes = genData.parseKeystrokes(input1)
        freq = genData.keyFreq(keystrokes)
        keys = genData.makeKeys(keystrokes)
        keytimes = genData.findKeytimes(keystrokes)
        hands, fingers = genData.handFingerFreq(keytimes)
        distance = genData.distance(keytimes)

        dwelltimes = genData.dwellTime(keytimes)
        fastdwell = genData.definingTimes(3, dwelltimes, True)
        slowdwell = genData.definingTimes(3, dwelltimes, False)

        bigrams = genData.findngrams(2, keytimes)
        bigramtimes = genData.ngramTimes(bigrams)
        fastbigrams = genData.definingTimes(4, bigramtimes, True)
        slowbigrams = genData.definingTimes(4, bigramtimes, False)
        biAtt = genData.biAttributes(bigrams)
        fast = genData.fastestTimes(len(bigramtimes)/2, bigramtimes)
        att = genData.definingAtt(biAtt[3])

        flighttimes = genData.flightTime(bigrams)
        fastflights = genData.definingTimes(3, flighttimes, True)
        slowflights = genData.definingTimes(3, flighttimes, False)

        mistakes = genData.keyMistakes(m)
        mostmistakes = genData.definingTimes(3, mistakes, True)
    else:
        analytics = None
        fastflights = None
        slowflights = None
        fastdwell = None
        slowdwell = None
        freq = None
        fastbigrams = None
        slowbigrams = None
        mostmistakes = None
        biAtt = None
        att = None
        keys = None
        fast = None
        accuracy = None
        wpm = None
        hands = None
        fingers = None
        distance = None
        mult = None

    return render_template("testanalytics.html", an=analytics, keyboard=keyboard, fastflights=fastflights, fastdwell=fastdwell, slowdwell=slowdwell, slowflights=slowflights, 
        freq=freq, fastbigrams=fastbigrams, slowbigrams=slowbigrams, mostmistakes=mostmistakes, biAtt=biAtt, att=att, keys=keys, tests=tests,
        fast=fast, accuracy=accuracy, wpm=wpm, hands=hands, fingers=fingers, distance=distance)

    
    

if __name__ == "__main__":
    app.run(debug=True)
