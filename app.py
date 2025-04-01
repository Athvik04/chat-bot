from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

USER_DB = "users.json"

# Function to load users
def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as file:
            return json.load(file)
    return {}

# Function to save users
def save_users(users):
    with open(USER_DB, "w") as file:
        json.dump(users, file, indent=4)

# Chatbot responses
def chatbot_response(user_input):
    responses = {
        "hello": ["Hi there! How can I help you?", "Hello! What's on your mind?"],
        "how are you": ["I'm just a bot, but I'm doing great!", "I'm always operational! How about you?"],
        "bye": ["Goodbye! Have a great day!", "See you next time!"],
        "help": ["You can ask me about greetings, how I'm doing, or say 'bye' to exit."],
        
        # College-related queries
        "admission process": [
            "The admission process varies by college. Generally, you need to apply online, submit required documents, and appear for an entrance exam if necessary.",
            "You can check the official website for details on admissions, eligibility, and deadlines."
        ],
        "courses offered": [
            "Our college offers courses in Engineering, Business, Science, Arts, and more.",
            "We have undergraduate and postgraduate programs in various disciplines."
        ],
        "fees structure": [
            "The fee structure depends on the course. You can check the college website for the latest fee details.",
            "Scholarships and financial aid options are also available."
        ],
        "scholarship options": [
            "Yes, we offer merit-based and need-based scholarships. You can apply through the financial aid office.",
            "There are various government and private scholarships available for eligible students."
        ],
        "hostel facilities": [
            "Yes, we provide hostel facilities for students, with separate accommodations for boys and girls.",
            "Hostel facilities include Wi-Fi, study rooms, and a cafeteria."
        ],
        "placement opportunities": [
            "Our college has a strong placement cell that connects students with top companies.",
            "We have partnerships with leading companies that offer internships and job placements."
        ],
        "library facilities": [
            "Our library has a vast collection of books, digital resources, and research materials.",
            "Students can access e-books, journals, and study materials anytime."
        ],
        "entrance exam": [
            "Admissions may require an entrance exam. Check the official website for eligibility and exam details.",
            "Some courses require specific entrance exams like JEE, CAT, or NEET."
        ],
        "faculty details": [
            "Our faculty members are highly qualified and experienced in their respective fields.",
            "We have a dedicated team of professors and guest lecturers from reputed universities."
        ]
    }
    return responses.get(user_input.lower(), ["I'm not sure how to respond to that.", "Can you rephrase that?"])[0]

@app.route("/")
def home():
    if "username" in session:
        return render_template("index.html", username=session["username"])
    return redirect(url_for("login"))

@app.route("/chat", methods=["POST"])
def chat():
    if "username" not in session:
        return jsonify({"response": "Please log in first."})
    data = request.json
    user_message = data.get("message", "")
    response = chatbot_response(user_message)
    return jsonify({"response": response})

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    data = request.json
    username = data.get("username")
    password = data.get("password")

    users = load_users()

    if username in users and users[username] == password:
        session["username"] = username
        return jsonify({"success": True, "message": "Login successful!", "redirect": "/"})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"})

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    data = request.json
    username = data.get("username")
    password = data.get("password")

    users = load_users()

    if username in users:
        return jsonify({"success": False, "message": "User already exists!"})

    users[username] = password
    save_users(users)

    return jsonify({"success": True, "message": "Signup successful! Please login.", "redirect": "/login"})

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
