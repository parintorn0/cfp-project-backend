from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify

@app.route('/register', methods=['POST'])
def register():
    data = request.json  # Get the JSON data from the request
    email = data['email']
    password = data['password']
    name = data['name']
    surname = data['surname']
    telephone = data['telephone']
    user_type = "C"

    # Hash the password

    # Database Insert
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if email already exists
    cursor.execute("SELECT * FROM public.\"User\" WHERE email = %s", (email,))
    if cursor.fetchone():
        return jsonify({"message": "Email already exists!"}), 400

    # Insert new user into the database
    cursor.execute(""" 
        INSERT INTO public."User" (email, password, name, surname, telephone, user_type)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING user_id;
    """, (email, password, name, surname, telephone, user_type))
    user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.execute("""
        SELECT customer_id FROM public.\"Customer\" ORDER BY customer_id DESC LIMIT 1
    """)
    customer_id=cursor.fetchone()[0]
    cursor.execute("""
        INSERT INTO public.\"Customer\" (user_id, customer_id)
        VALUES (%s, %s);
    """, (user_id, customer_id+1))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "User registered successfully!", "user_id": user_id}), 201