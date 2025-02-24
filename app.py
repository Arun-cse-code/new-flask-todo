from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import uuid  # Generates unique session IDs

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Arun2004@localhost:3306/todo_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Todo Model with user_session field
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(5000), nullable=False)
    user_session = db.Column(db.String(100), nullable=False)  # Unique session ID for each user

# Home Route - Show Tasks for Only Current User
@app.route('/', methods=["GET", "POST"])
def home():
    # Assign a unique session ID if not already set
    if "user_session" not in session:
        session["user_session"] = str(uuid.uuid4())  # Generate unique session ID

    user_session = session["user_session"]  # Get current user's session ID

    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc, user_session=user_session)  # Save with session ID
        db.session.add(todo)
        db.session.commit()

    # Fetch only the tasks belonging to the current session
    alltodo = Todo.query.filter_by(user_session=user_session).all()
    return render_template("index.html", alltodo=alltodo)

# Delete Task (Only if it belongs to the current user)
@app.route('/delete/<int:sno>')
def delete(sno):
    user_session = session.get("user_session")  # Get current user's session ID
    todo = Todo.query.filter_by(sno=sno, user_session=user_session).first()
    
    if todo:
        db.session.delete(todo)
        db.session.commit()
    
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure database is created
    app.run(debug=True)
