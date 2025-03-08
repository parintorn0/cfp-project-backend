from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify

@app.route('/login', methods=['POST'])
def login():
    data = request.json  # Get the JSON data from the request
    email = data['email']
    password = data['password']

    # Database Query
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get user data
    cursor.execute("SELECT user_id, user_type FROM public.\"User\" WHERE email = %s AND password = %s", (email, password,))
    user = cursor.fetchone()
    if user:
        cursor.close()
        conn.close()
        return jsonify({
            "message": "Login successful!",
            "user_id": user[0],
            "user_type": user[1],
        }), 200
    else:
        cursor.close()
        conn.close()
        return jsonify({"message": "Unsuccessful"}), 400
