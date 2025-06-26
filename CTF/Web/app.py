from flask import Flask, request, jsonify
import jwt
import datetime
app = Flask(__name__)
SECRET_KEY = "123"
USERS = {
    "guest": "guest123",
    "admin": "admin123"
}

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username in USERS and USERS[username] == password:
        is_admin = username == "admin"
        token = jwt.encode({
            "username": username,
            "isAdmin": is_admin,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})

    return jsonify({"error": "Invalid credentials"}), 401
@app.route("/admin", methods=["GET"])
def admin():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"error": "Missing token"}), 401

    token = auth.split(" ")[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if decoded.get("isAdmin"):
            return jsonify({"flag": "CTF{this_is_a_flag}"})
        else:
            return jsonify({"error": "Admins only"}), 403
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == "__main__":
    app.run(debug=True)
