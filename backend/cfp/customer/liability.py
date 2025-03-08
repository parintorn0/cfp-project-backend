from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify

@app.route('/customer_liability', methods=['POST'])
def customer_liability():
    data = request.json
    if 'version_id' in data:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, amount, rate, start, term, duration FROM public.\"Liability\" WHERE version_id = %s", (data['version_id'],))
        liabilities = cursor.fetchall()
        result=[]
        for liability in liabilities:
            result.append({
                'name': str(liability[0]),
                'amount': str(liability[1]),
                'rate': str(liability[2]),
                'start': str(liability[3]),
                'term': str(liability[4]),
                'duration': str(liability[5]),
                })
        cursor.close()
        conn.close()
        return jsonify(result), 200
    else:
        cursor.close()
        conn.close()
        return jsonify({"message": "Unable to recieve user id"}), 400