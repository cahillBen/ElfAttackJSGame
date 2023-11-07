from flask import Flask, render_template, request, jsonify, g, session, redirect, url_for
from database import close_db, get_db
from flask_session import Session
from form import UsernameForm
from functools import wraps

app = Flask(__name__)

app.config["SECRET_KEY"] = "MY_SECRET_KEY"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.teardown_appcontext
def close_db_at_end_of_request(e=None):
    close_db(e)

@app.before_request
def load_logged_in_user():
    g.user = session.get("username",None)
    g.continueKey = session.get("continueKey","c")
    g.shootKey = session.get("shootKey","f")
    g.hitKey = session.get("hitKey","h")
    g.invincibleKey = session.get("invincibleKey","i")
    g.skipKey = session.get("skipKey","s")

@app.route("/",methods=["GET","POST"])
def index():
    if g.user == None:
        return redirect(url_for("username"))
    return render_template("home.html")

@app.route("/home",methods=["GET","POST"])
def home():
    if g.user == None:
        return redirect(url_for("username"))
    return render_template("home.html")

@app.route("/username",methods=["GET","POST"])
def username():
    form = UsernameForm()
    if form.validate_on_submit():
        username = form.username.data
        session.clear()
        session["username"] = username
        print(username)
        return redirect(url_for("home"))
    return render_template("username.html",form=form)

@app.route("/rules")
def rules():
    return render_template("rules.html",hit=g.hitKey,shoot=g.shootKey,continueKey=g.continueKey,invincibleKey=g.invincibleKey,skipKey=g.skipKey)

@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")

@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/settings", methods=["GET","POST"])
def settings():
    g.continueKey = session.get("continueKey",None)
    g.shootKey = session.get("shootKey",None)
    g.hitKey = session.get("hitKey",None)
    g.invincibleKey = session.get("invincibleKey",None)
    g.skipKey = session.get("skipKey",None)
    return render_template("settings.html",continueKey=g.continueKey,shootKey=g.shootKey,hitKey=g.hitKey,skipKey=g.skipKey,invincibleKey=g.invincibleKey)

@app.route("/store_keys",methods=["POST","GET"])
def store_keys():
    continueKey = (request.form["continueKey"])
    shootKey = (request.form["shootKey"])
    hitKey = (request.form["hitKey"])
    skipKey = (request.form["skipKey"])
    invincibleKey = (request.form["invincibleKey"])
    if invincibleKey != "" and invincibleKey != " ":
        session["invincibleKey"] = invincibleKey[0].lower()
    if skipKey != "" and skipKey != " ":
        session["skipKey"] = skipKey[0].lower()
    if continueKey != "" and continueKey != " ":
        session["continueKey"] = continueKey[0].lower()
    if shootKey != "" and shootKey != " ":
        session["shootKey"] = shootKey[0].lower()
    if hitKey != "" and hitKey != " ":
        session["hitKey"] = hitKey[0].lower()
    return render_template('home.html')

@app.route("/scores")
def scores():
    db = get_db()
    scores = db.execute("""  SELECT * FROM scores ORDER BY score DESC""").fetchall()
    return render_template("scores.html",scores=scores)

@app.route("/store_score",methods=["POST"])
def store_score():
    score = int(request.form["score"])
    db = get_db()
    db.execute("""INSERT INTO scores(username,score) VALUES (?,?)""",(g.user,score))
    db.commit()
    return "success"

@app.route("/return_keys",methods=["GET","POST"])
def return_keys():
    return jsonify({"continueKey":g.continueKey,"shootKey":g.shootKey,"hitKey":g.hitKey,"skipKey":g.skipKey,"invincibleKey":g.invincibleKey})

    