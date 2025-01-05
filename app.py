from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Configure the app with a secret key and database URI
app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

# Define the Form model for the database
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))

# Define the route for the home page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve form data from the request
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")  # Convert date string to a date object
        occupation = request.form["occupation"]

        # Create a new Form object and add it to the database
        form = Form(first_name=first_name, last_name=last_name,
                    email=email, date=date_obj, occupation=occupation)
        db.session.add(form)
        db.session.commit()

        # Display a success message to the user
        flash(f"Hi {first_name}, your form was submitted successfully!", "success")

    # Render the index.html template
    return render_template('index.html')

# Run the Flask app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables
        app.run(debug=True, port=5001)  # Start the app in debug mode on port 5001
