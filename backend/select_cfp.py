import os
from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify, send_file
from datetime import date

@app.route('/select_cfp', methods=['POST'])
def select_cfp():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    if 'user_id' in data:
        user_id = data['user_id']
        if 'cfp_id' not in data:
            return jsonify({'message': "cfp_id missing"}), 501
        cfp_id = data['cfp_id']
        cursor.execute("""
            SELECT customer_id FROM public.\"Customer\" WHERE user_id = %s
        """, (user_id,))
        customer=cursor.fetchone()
        if customer:
            customer_id = customer[0]
            cursor.execute("""
                SELECT customer_id FROM public.\"Relationship\" WHERE customer_id = %s
            """, (customer_id,))
            relationship = cursor.fetchone()
            if relationship:
                return jsonify({"message": "คุณมีนักวางแผนอยู่แล้ว"}), 200
            
            cursor.execute("""
                INSERT INTO public.\"Relationship\" (cfp_id, customer_id, status) VALUES (%s, %s, %s)
            """, (cfp_id, customer_id, "รอการติดต่อ",))
            cursor.execute("""
                INSERT INTO public.\"Version\" (date, customer_id, version_number) VALUES (%s, %s, %s)
            """, (date.today(), customer_id, 1,))
            conn.commit()
            return jsonify({
                "message": "เลือกสำเร็จ",
            }), 200
        else:
            return jsonify({'message': "not found customer_id"}), 501
    else:
        return jsonify({'message': "user_id missing"}), 501