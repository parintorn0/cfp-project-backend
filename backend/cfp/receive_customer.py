from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify

@app.route('/receive_customer', methods=['POST'])
def receive_customers():
    data = request.json
    # Database Query
    conn = get_db_connection()
    cursor = conn.cursor()
    if 'user_id' in data:
        cursor.execute("SELECT user_type FROM public.\"User\" WHERE user_type = 'A' OR user_type ='F' AND user_id = %s", (data['user_id'],))
        userType = cursor.fetchone()
        if userType:
            userType=userType[0]
        if userType!='F' and userType!='A':
            return jsonify({"message": "No permission"}), 501
        cfp_id=None
        if userType=='A' and 'cfp_id' in data:
            cfp_id = data['cfp_id']
        else:
            cursor.execute("SELECT cfp_id FROM public.\"CFP\" WHERE user_id = %s", (data['user_id'],))
            cfp_id = cursor.fetchone()
            if cfp_id:
                cfp_id = cfp_id[0]
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
            versions_info = []
            for version_num, date, version_id in versions:
                versions_info.append({"version_num": version_num, "date": date.strftime('%Y-%m-%d'), "version_id": version_id})
            result.append({
                'customer_id': str(customer_id),
                'name': str(customer_user[0] + " " + customer_user[1]),
                'telephone': str(customer_user[2]),
                'status': str(status),
                'versions_info': versions_info
            })
        cursor.close()
        conn.close()
        return jsonify(result), 200
    else:
        return jsonify({"message": "Unable to recieve user id"}), 400
