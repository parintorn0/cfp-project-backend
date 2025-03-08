from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify

@app.route('/admin/cfp_list', methods=['POST'])
def admin_cfp_list():
    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()

    if 'user_id' in data:
        cursor.execute("SELECT user_type FROM public.\"User\" WHERE user_id = %s", (data['user_id'],))
        if cursor.fetchone()[0]!='A':
            return jsonify({"message": "this is not admin account"}), 401
        result = []
        cursor.execute("SELECT user_id, cfp_id FROM public.\"CFP\"")
        cfps = cursor.fetchall()
        for cfp in cfps:
            cfp_user_id = cfp[0]
            cfp_id = cfp[1]
            cursor.execute("SELECT name, surname, telephone FROM public.\"User\" WHERE user_id = %s", (cfp_user_id,))
            cfp_info = cursor.fetchone()
            cfp_name = f"{cfp_info[0]} {cfp_info[1]}"
            cfp_telephone = cfp_info[2]
            cursor.execute("SELECT COUNT(cfp_id) FROM public.\"Relationship\" WHERE cfp_id = %s", (cfp_id,))
            customer_count = cursor.fetchone()[0]
            result.append({
                'cfp_id': cfp_id,
                'cfp_name': cfp_name,
                'telephone': cfp_telephone,
                'customer_count': customer_count,
            })
        return jsonify(result), 200
    else:
        return jsonify({"message": "Unable to recieve user id"}), 400
