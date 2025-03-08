from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify

@app.route('/admin/receive_customer', methods=['POST'])
def admin_receive_customers():
    data = request.json

    # Database Query
    conn = get_db_connection()
    cursor = conn.cursor()
    if 'user_id' in data:
        cursor.execute("SELECT user_type FROM public.\"User\" WHERE user_id = %s", (data['user_id'],))
        if cursor.fetchone()[0]!='A':
            return jsonify({"message": "this is not admin account"}), 401
        cursor.execute("SELECT cfp_id, customer_id FROM public.\"Relationship\"")
        relationship = cursor.fetchall()
        result = []
        for relation in relationship:
            cfp_id = relation[0]
            customer_id = relation[1]
            cursor.execute("SELECT date FROM public.\"Version\" WHERE customer_id = %s AND version_number = 1", (customer_id,))
            date = cursor.fetchone()[0]
            cursor.execute("SELECT user_id FROM public.\"Customer\" WHERE customer_id = %s", (customer_id,))
            customer_user_id = cursor.fetchone()[0]
            cursor.execute("SELECT user_id FROM public.\"CFP\" WHERE cfp_id = %s", (cfp_id,))
            cfp_user_id = cursor.fetchone()[0]
            cursor.execute("SELECT name, surname, telephone FROM public.\"User\" WHERE user_id = %s", (customer_user_id,))
            customer=cursor.fetchone()
            customer_name = f"{customer[0]} {customer[1]}"
            customer_telephone = customer[2]
            cursor.execute("SELECT name, surname FROM public.\"User\" WHERE user_id = %s", (cfp_user_id,))
            cfp=cursor.fetchone()
            cfp_name = f"{cfp[0]} {cfp[1]}"
            result.append({
                'customer_name': customer_name,
                'telephone': customer_telephone,
                'date': date.strftime('%Y-%m-%d'),
                'cfp_name': cfp_name
            })
        cursor.close()
        conn.close()
        return jsonify(result), 200
    else:
        return jsonify({"message": "Unable to recieve user id"}), 400
