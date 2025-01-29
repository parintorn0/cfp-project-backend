import bcrypt
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from datetime import date

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
                    'name': str(customer_user[0] + " " + customer_user[1]),
                    'telephone': str(customer_user[2]),
                    'version_num': str(version[0]),
                    'date': str(version[1].strftime('%Y-%m-%d')),
                    'status': str(status),
                    'version_id': str(version[2])
                })
        cursor.close()
        conn.close()
        return jsonify(result), 200
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
                'name': str(asset[0]),
                'amount': str(asset[1]),
                'subtype': str(asset[2]),
                'growthrate': str(asset[3]),
                'type': str(asset[4]),
                })
        cursor.close()
        conn.close()
        return jsonify(result), 200
    else:
        cursor.close()
        conn.close()
        return jsonify({"message": "Unable to recieve user id"}), 400

@app.route('/customer_liability', methods=['POST'])
def customer_liability():
    data = request.json
    if 'version_id' in data:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, amount, rate, start, end_date FROM public.\"Liability\" WHERE version_id = %s", (data['version_id'],))
        liabilities = cursor.fetchall()
        result=[]
        for liability in liabilities:
            result.append({
                'name': str(liability[0]),
                'amount': str(liability[1]),
                'rate': str(liability[2]),
                'start': str(liability[3]),
                'end': str(liability[4]),
                })
        cursor.close()
        conn.close()
        return jsonify(result), 200
    else:
        cursor.close()
        conn.close()
        return jsonify({"message": "Unable to recieve user id"}), 400

@app.route('/customer_income', methods=['POST'])
def customer_income():
    data = request.json
    if 'version_id' in data:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, amount, growthrate, type FROM public.\"Income\" WHERE version_id = %s", (data['version_id'],))
        incomes = cursor.fetchall()
        result=[]
        for income in incomes:
            result.append({
                'name': str(income[0]),
                'amount': str(income[1]),
                'growthrate': str(income[2]),
                'type': str(income[3]),
                })
        cursor.close()
        conn.close()
        return jsonify(result), 200
    else:
        cursor.close()
        conn.close()
        return jsonify({"message": "Unable to recieve user id"}), 400

@app.route('/customer_expense', methods=['POST'])
def customer_expense():
    data = request.json
    if 'version_id' in data:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, amount, growthrate FROM public.\"Expense\" WHERE version_id = %s", (data['version_id'],))
        expenses = cursor.fetchall()
        result=[]
        for expense in expenses:
            result.append({
                'name': str(expense[0]),
                'amount': str(expense[1]),
                'growthrate': str(expense[2]),
                })
        cursor.close()
        conn.close()
        return jsonify(result), 200
    else:
        cursor.close()
        conn.close()
        return jsonify({"message": "Unable to recieve user id"}), 400


@app.route('/customer_goal', methods=['POST'])
def customer_goal():
    data = request.json
    if 'version_id' in data:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, amount, year, priority FROM public.\"Goal\" WHERE version_id = %s", (data['version_id'],))
        goals = cursor.fetchall()
        cursor.execute("SELECT age, retirementage, deadage, inflation FROM public.\"Retirement\" WHERE version_id = %s", (data['version_id'],))
        retirement = cursor.fetchone()
        result=[]
        for goal in goals:
            result.append({
                'name': str(goal[0]),
                'amount': str(goal[1]),
                'year': str(goal[2]),
                'priority': str(goal[3])
                })
        if retirement:
            cursor.close()
            conn.close()
            return jsonify({
            "retirement": {
                'age': str(retirement[0]),
                'retirementage': str(retirement[1]),
                'deadage': str(retirement[2]),
                'inflation': str(retirement[3]),
                },
            "goal": result
            }), 200
        else:
            cursor.close()
            conn.close()
            return jsonify({
                "retirement": None,
                "goal": result
                }), 200
    else:
        cursor.close()
        conn.close()
        return jsonify({"message": "Unable to recieve user id"}), 400

@app.route('/save', methods=['POST'])
def save():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    # get cutomer id version number
    cursor.execute("SELECT customer_id FROM public.\"Version\" WHERE version_id = %s ORDER BY version_id DESC", (data['version_id'],))
    version = cursor.fetchone()
    customer_id = version[0]
    # check all
    assets = data['assets']
    liabilities = data['liabilities']
    incomes = data['incomes']
    expenses = data['expenses']
    goals = data['goals']['goal']
    retirement = data['goals']['retirement']
    # check if input all
    for asset in assets:
        if len(asset['name']) == 0 or len(asset['amount']) == 0 or len(asset['growthrate']) == 0 or len(asset['subtype']) == 0 or len(asset['type']) == 0:
            return jsonify({"message": "Some asset might not be inputed"}), 501
        try:
            float(asset['amount'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Asset's amount is not number"}), 501
        try:
            float(asset['growthrate']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Asset's growth rate is not number"}), 501
    for liability in liabilities:
        if len(liability['name']) == 0 or len(liability['amount']) == 0 or len(liability['start']) == 0 or len(liability['end']) == 0 or len(liability['rate']) == 0:
            return jsonify({"message": "Some liability might not be inputed"}), 501
        try:
            float(liability['amount'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Liability's amount is not number"}), 501
        try:
            float(liability['rate']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Liability's rate is not number"}), 501
    for income in incomes:
        if len(income['name']) == 0 or len(income['amount']) == 0 or len(income['growthrate']) == 0 or len(income['type']) == 0:
            return jsonify({"message": "Some income might not be inputed"}), 501
        try:
            float(income['amount'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Income's amount is not number"}), 501
        try:
            float(income['growthrate']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Income's growth rate is not number"}), 501
    for expense in expenses:
        if len(expense['name']) == 0 or len(expense['amount']) == 0 or len(expense['growthrate']) == 0:
            return jsonify({"message": "Some expense might not be inputed"}), 501
        try:
            float(expense['amount'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Expense's amount is not number"}), 501
        try:
            float(expense['growthrate']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Expense's growth rate is not number"}), 501
    for goal in goals:
        if len(goal['name']) == 0 or len(goal['amount']) == 0 or len(goal['year']) == 0 or len(goal['priority']) == 0:
            return jsonify({"message": "Some goal might not be inputed"}), 501
        try:
            float(goal['amount'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Goal's amount is not number"}), 501
        try:
            float(goal['year']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Goal's year is not number"}), 501
    if len(retirement['age']) == 0 or len(retirement['deadage']) == 0 or len(retirement['inflation']) == 0 or len(retirement['retirementage']) == 0:
        return jsonify({"message": data['goals']}), 501
    try:
        int(retirement['age'])
    except:
        cursor.close()
        conn.close()
        return jsonify({"message": "Retirement's current age is not number"}), 501
    try:
        int(retirement['deadage']),
    except:
        cursor.close()
        conn.close()
        return jsonify({"message": "Retirement's dead age is not number"}), 501
    try:
        int(retirement['retirementage']),
    except:
        cursor.close()
        conn.close()
        return jsonify({"message": "Retirement's age is not number"}), 501
    
    # insert to tables
    cursor.execute("""
    SELECT version_number FROM public.\"Version\" WHERE customer_id=%s ORDER BY version_id DESC;
    """, str(customer_id))
    version_number=cursor.fetchone()[0]+1
    cursor.execute("""
    INSERT INTO public.\"Version\" (customer_id, date, version_number) VALUES (%s, %s, %s)
    RETURNING version_id;
    """, (customer_id, date.today(), version_number))
    version_id=cursor.fetchone()[0]
    for asset in assets:
        cursor.execute("""
        INSERT INTO public.\"Asset\" (name, amount, subtype, growthrate, type, version_id) VALUES (%s, %s, %s, %s, %s, %s);
        """, (asset['name'], asset['amount'], asset['subtype'], asset['growthrate'], asset['type'], version_id))
    for liability in liabilities:
        cursor.execute("""
        INSERT INTO public.\"Liability\" (name, amount, rate, start, end_date, version_id) VALUES (%s, %s, %s, %s, %s, %s);
        """, (liability['name'], liability['amount'], liability['rate'], liability['start'], liability['end'], version_id))
    for income in incomes:
        cursor.execute("""
        INSERT INTO public.\"Income\" (name, amount, growthrate, type, version_id) VALUES (%s, %s, %s, %s, %s);
        """, (income['name'], income['amount'], income['growthrate'], income['type'], version_id))
    for expense in expenses:
        cursor.execute("""
        INSERT INTO public.\"Expense\" (name, amount, growthrate, version_id) VALUES (%s, %s, %s, %s);
        """, (expense['name'], expense['amount'], expense['growthrate'], version_id))
    for goal in goals:
        cursor.execute("""
        INSERT INTO public.\"Goal\" (name, amount, year, priority, version_id) VALUES (%s, %s, %s, %s, %s);
        """, (goal['name'], goal['amount'], goal['year'], goal['priority'], version_id))
    cursor.execute("""
    INSERT INTO public.\"Retirement\" (age, retirementage, deadage, inflation, version_id) VALUES (%s, %s, %s, %s, %s);
    """, (retirement['age'], retirement['retirementage'], retirement['deadage'], retirement['inflation'], version_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Saved"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
