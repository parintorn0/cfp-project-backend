from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify

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