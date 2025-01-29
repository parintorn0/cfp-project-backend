import bcrypt
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app, origins="*")

def get_db_connection():
    conn = psycopg2.connect(
        dbname="CFP project",
        user="postgres",
        password="DekDe579",
        host="localhost",
        port="5432"
    )
    return conn

@app.route('/ping', methods=['GET'])
def pong():
    return("pongyyy") ,200

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Get the JSON data from the request
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    surname = data.get('surname')
    telephone = data.get('telephone')
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
    cursor.execute("""
        INSERT INTO public."Customer" ()
        VALUES (%s) RETURNING user_id;
    """, (user_id))
    user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "User registered successfully!", "user_id": user_id}), 201



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Get the JSON data from the request
    email = data.get('email')
    password = data.get('password')

    # Database Query
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get user data
    cursor.execute("SELECT * FROM public.\"User\" WHERE email = %s", (email,))  # Fix tuple formatting
    user = cursor.fetchone()

    if user:
        # Assuming user[2] is the stored hashed password and user[3] is user_type
        user_id = user[0]
        stored_password = user[2]
        user_type = user[3]

        # Compare the password (hashed comparison recommended)
        if password == stored_password:  # Replace with hashed comparison in production
            cursor.close()
            conn.close()
            return jsonify({
                "message": "Login successful!",
                "user_type": user_type,
                "user_id": user_id
            }), 200
        else:
            cursor.close()
            conn.close()
            return jsonify({"message": "Invalid password!"}), 400
    else:
        cursor.close()
        conn.close()
        return jsonify({"message": "User not found!"}), 400


@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    return jsonify(data)

@app.route('/receive_customer', methods=['POST'])
def receive_customer():
    data = request.json

    # Database Query
    conn = get_db_connection()
    cursor = conn.cursor()
    if 'user_id' in data:
        cursor.execute("SELECT * FROM public.\"CFP\" WHERE user_id = %s", (data['user_id'],))
        cfp = cursor.fetchone()
        cfp_id = cfp[1]
        cursor.execute("SELECT customer_id, status FROM public.\"Relationship\" WHERE cfp_id = %s", (cfp_id,))
        relationship = cursor.fetchall()
        result=[]
        for relation in relationship:
            customer_id=relation[0]
            status=relation[1]
            cursor.execute("SELECT user_id FROM public.\"Customer\" WHERE customer_id = %s", (customer_id,))
            customer = cursor.fetchone()
            customer_user_id = customer[0]
            cursor.execute("SELECT name, surname, telephone FROM public.\"User\" WHERE user_id = %s", (customer_user_id,))
            customer_user = cursor.fetchone()
            cursor.execute("SELECT version_number, date, version_id FROM public.\"Version\" WHERE customer_id = %s", (customer_id,))
            versions = cursor.fetchall()
            for version in versions:
                result.append({
                    'name': customer_user[0] + " " + customer_user[1],
                    'telephone': customer_user[2],
                    'version_num': version[0],
                    'date': version[1].strftime('%d/%m/%Y'),
                    'status': status,
                    'version_id': version[2]
                })
        cursor.close()
        conn.close()
        return jsonify(result)
    else:
        return jsonify({"message": "Unable to recieve user id"}), 400

@app.route('/customer_asset', methods=['POST'])
def customer_asset():
    data = request.json

    if 'version_id' in data:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, amount, subtype, growthrate, type FROM public.\"Asset\" WHERE version_id = %s", (data['version_id'],))
        assets = cursor.fetchall()
        result=[]
        for asset in assets:
            result.append({
                'name': asset[0],
                'amount': asset[1],
                'subtype': asset[2],
                'growthrate': asset[3],
                'type': asset[4],
                })
        return jsonify(result), 400
    else:
        return jsonify({"message": "Unable to recieve user id"}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
