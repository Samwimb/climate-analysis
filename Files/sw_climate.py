from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my API!"

@app.route("/about")
def about():
    print("Server received request for 'about' page...")
    return "Sam Wimberly, Arlington"

@app.route("/contact")
def contact():
    print("Server received request for 'contact' page...")
    return "email: samwimb02@gmail.com"

if __name__ == "__main__":
    app.run(debug=True)
