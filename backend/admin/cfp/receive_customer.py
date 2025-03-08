from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify

@app.route('/admin/cfp/receive_customer', methods=['POST'])
def admin_cfp_receive_customers():
    data = request.json

    # Database Query
    conn = get_db_connection()
    cursor = conn.cursor()
    if 'user_id' in data:
        cursor.execute("SELECT user_type FROM public.\"User\" WHERE user_id = %s", (data['user_id'],))
        if cursor.fetchone()[0]!='A':
            return jsonify({"message": "this is not admin account"}), 401
        if 'cfp_id' not in data:
            return jsonify({"message": "cfp id missing"}), 401
        cfp_id = data['cfp_id']
        cursor.execute("SELECT user_id FROM public.\"CFP\" WHERE cfp_id = %s", (cfp_id,))
        cfp_user_id = cursor.fetchone()[0]
        cursor.execute("SELECT name, surname FROM public.\"User\" WHERE user_id = %s", (cfp_user_id,))
        cfp = cursor.fetchone()
        cfp_name = f"{cfp[0]} {cfp[1]}"
        cursor.execute("SELECT customer_id, status FROM public.\"Relationship\" WHERE cfp_id = %s", (cfp_id,))
        relationship = cursor.fetchall()
        result={
            "cfp_name" : cfp_name,
            "customer" :[],
            }
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
            versions_info = []
            for version_num, date, version_id in versions:
                versions_info.append({"version_num": version_num, "date": date.strftime('%Y-%m-%d'), "version_id": version_id})
            result['customer'].append({
                'customer_id': customer_id,
                'customer_name': f"{customer_user[0]} {customer_user[1]}",
                'telephone': str(customer_user[2]),
                'status': str(status),
                'versions_info': versions_info
            })
        cursor.close()
        conn.close()
        return jsonify(result), 200
    else:
        return jsonify({"message": "Unable to recieve user id"}), 400
