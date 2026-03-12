from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Import FarmMind brain
from brain import FarmMind
from knowledge_base import agriculture_knowledge


# -----------------------------
# Flask Setup
# -----------------------------
app = Flask(__name__)
app.secret_key = "supersecretkey123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmmind.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------------
# Load AI Brain
# -----------------------------
brain = FarmMind(agriculture_knowledge)


def farmmind_respond(message):
    try:
        return brain.answer(message)
    except Exception:
        return "⚠️ FarmMind had trouble answering. Please try again."


# -----------------------------
# Database Models
# -----------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_message = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)


# -----------------------------
# Login
# -----------------------------
@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username'].strip()
        password = request.form['password'].strip()

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            session['user_id'] = user.id
            session['username'] = user.username

            return redirect(url_for('dashboard'))

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


# -----------------------------
# Register
# -----------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if User.query.filter_by(username=username).first():
            return render_template("register.html", error="Username already exists")

        hashed_pw = generate_password_hash(password)

        new_user = User(username=username, password=hashed_pw)

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        session['username'] = new_user.username

        return redirect(url_for('dashboard'))

    return render_template("register.html")


# -----------------------------
# Logout
# -----------------------------
@app.route('/logout')
def logout():

    session.clear()
    return redirect(url_for('login'))


# -----------------------------
# Dashboard + Chat
# -----------------------------
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    # User sends a message
    if request.method == 'POST':

        data = request.get_json()

        user_message = data.get("message", "")

        ai_reply = farmmind_respond(user_message)

        chat_entry = Chat(
            user_id=session['user_id'],
            user_message=user_message,
            ai_response=ai_reply
        )

        db.session.add(chat_entry)
        db.session.commit()

        return jsonify({"reply": ai_reply})

    # Load previous chats
    chats = Chat.query.filter_by(user_id=session['user_id']).all()

    return render_template(
        "dashboard.html",
        chats=chats,
        username=session['username']
    )


# -----------------------------
# Initialize Database
# -----------------------------
with app.app_context():
    db.create_all()


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    print("starting farm mind server.....")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


