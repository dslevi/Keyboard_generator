from flask import Flask, render_template, redirect, request, g, session, url_for, flash
from model import User, Analytics, Prompts, Keyboard, Key
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
import config
import forms
import model
import random
import genKeyboard


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
        user = User.query.filter_by(id=session['user_id']).first()
    else:
        user = None
    return render_template("index.html", user=user)

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
    strokes = request.form.get("stroke")
    raw = request.form.get("rawtext")
    final = request.form.get("final_text")
    return render_template("keyboard.html", prompt=prompt.text, strokes=strokes, raw=raw, final_text=final)

@app.route("/keyboard")
def show_keyboard():
    prompt = Prompts.query.get(random.randint(1, 227))
    strokes = ""
    raw = ""
    final = ""
    return render_template("keyboard.html", prompt=prompt.text, strokes=strokes, raw=raw, final_text=final)

@app.route("/analytics")
def no_analytics():
    if session.get('text'):
        text = session['text']
        raw_text = session['raw']
        strokes = session['strokes']
        keyboard = session['keyboard']
        key_freq, mistakes, avg_times = genKeyboard.createAnalytics(strokes)
        return render_template("analytics.html", raw_text=raw_text, text=text, strokes=strokes, avg_times=avg_times, keyboard=keyboard,
            key_freq=key_freq, mistakes=mistakes)

    if session.get('user_id'):
        user = User.query.filter_by(id=session['user_id']).first()
        analytics = user.analytics
        if len(analytics) > 0:
            strokes = analytics[-1].strokes
            key_freq, mistakes, avg_times = genKeyboard.createAnalytics(strokes)
            keyboard = genKeyboard.createKeyboard(strokes)
            return render_template("existing_analytics.html", raw_text=analytics[-1].raw_text, text=analytics[-1].text, strokes=analytics[-1].strokes, 
                avg_times=avg_times, keyboard=keyboard, key_freq=key_freq, mistakes=mistakes)
    return render_template("no_analytics.html")

def genName():
    rand_str = "".join(random.choice('ABCDEFGHIJKLMNOP1234567890') for i in range(10))
    return rand_str

@app.route("/analytics", methods=["POST"])
def show_analytics():
    text = request.form.get("final_text")
    raw_text = request.form.get("rawtext")
    strokes = request.form.get("stroke")
    session['text'] = text
    session['raw'] = raw_text
    session['strokes'] = strokes
    key_freq, mistakes, avg_times = genKeyboard.createAnalytics(strokes)
    new_keyboard = genKeyboard.createKeyboard(strokes)
    session['keyboard'] = new_keyboard
    if session.get("user_id"):
        user_id = session['user_id']
        new_a = Analytics(text=text, raw_text=raw_text, strokes=strokes, user_id=user_id)
        model.session.add(new_a)
        new_k = Keyboard(name=genName(), user_id=user_id)
        model.session.add(new_k)
        #creates a new keyboard each time
        for i in range(len(new_keyboard)):
            key = Key(kb_id=new_k.id)
            key.location = new_keyboard[i][0]
            key.div = new_keyboard[i][1]
            qwerty_key = Key.query.filter_by(div=new_keyboard[i][1]).first()
            key.values = qwerty_key.values
            key.codes = qwerty_key.codes
            new_k.keys.append(key)
        model.session.commit()
    else:
        user_id=None
    return render_template("analytics.html", strokes=strokes, text=text, raw_text=raw_text, user_id=user_id, avg_times=avg_times, 
        keyboard=new_keyboard, key_freq=key_freq, mistakes=mistakes)






#testing - remove later
@app.route("/testing")
def testing():
    keyboard=session['keyboard']
    css_keyboard = genKeyboard.CSSkeyboard(keyboard)
    return render_template("test.html", keyboard=css_keyboard)

#still under construction...
@app.route("/allkeyboards")
def all_keyboards():
    keyboards = []
    return render_template("all_keyboards.html", keyboards=keyboards)

@app.route("/pekl/<user_id>")
def view_pekl(user_id):
    keyboard=session['keyboard']
    css_keyboard = genKeyboard.CSSkeyboard(keyboard)
    return render_template("pekl.html", keyboard=css_keyboard)

@app.route("/keyboard/<keyboard_id>")
def display_keyboard(keyboard_id):
    return render_template("display_keyboard.html")

@app.route("/typingtest")
def typing_test():
    return render_template("construction.html")

@app.route("/remap")
def remap_keys():
    return render_template("construction.html")

@app.route("/logging")
def log_keys():
    return render_template("construction.html")

if __name__ == "__main__":
    app.run(debug=True)
