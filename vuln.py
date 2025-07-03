import os
import sqlite3
import pickle
from flask import Flask, request, send_file

app = Flask(__name__)

# Hardcoded credentials (bad practice)
USERNAME = "admin"
PASSWORD = "1234"

# Database connection
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
conn.commit()

@app.route("/login", methods=["POST"])
def login():
    user = request.form["username"]
    pwd = request.form["password"]

    if user == USERNAME and pwd == PASSWORD:
        return "Logged in"
    else:
        return "Unauthorized", 401

@app.route("/run", methods=["GET"])
def run_command():
    cmd = request.args.get("cmd")
    os.system(cmd)  # 🛑 Command injection
    return f"Executed: {cmd}"

@app.route("/query", methods=["GET"])
def query():
    name = request.args.get("name")
    query = f"SELECT * FROM users WHERE name = '{name}'"  # 🛑 SQL injection
    result = cursor.execute(query).fetchall()
    return str(result)

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    filepath = os.path.join("uploads", f.filename)  # 🛑 Path traversal risk
    f.save(filepath)
    return "File saved."

@app.route("/deserialize", methods=["POST"])
def deserialize():
    data = request.data
    obj = pickle.loads(data)  # 🛑 Insecure deserialization
    return f"Deserialized object: {obj}"

@app.route("/eval", methods=["GET"])
def evaluate():
    expr = request.args.get("expr")
    result = eval(expr)  # 🛑 Arbitrary code execution
    return str(result)

if __name__ == "__main__":
    app.run(debug=True)
