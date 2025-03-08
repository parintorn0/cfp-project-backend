from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify

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