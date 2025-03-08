import os
from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify, send_file
import datetime as date

@app.route('/getall_cfp', methods=['GET'])
def getall_cfp():
    # Database Query
    conn = get_db_connection()
    cursor = conn.cursor()
    result = []
    cursor.execute("""
        SELECT user_id, cfp_id FROM public.\"CFP\"
    """)
    cfps=cursor.fetchall()
    for cfp in cfps:
        cfp_user_id = cfp[0]
        cfp_id = cfp[1]
        cursor.execute("""
            SELECT name, surname FROM public.\"User\" WHERE user_id = %s
        """, (cfp_user_id, ))
        cfp_info=cursor.fetchone()
        cfp_name = f"{cfp_info[0]} {cfp_info[1]}"
        cursor.execute("""
            SELECT COUNT(blog_id) FROM public.\"Blog\" WHERE cfp_id = %s
        """, (cfp_id,))
        blog_count = cursor.fetchone()[0]
        result.append({
            "cfp_id": cfp_id,
            "blog_count": blog_count,
            "cfp_name": cfp_name,
        })
    return jsonify(result), 200

@app.route('/get_cfp', methods=['POST'])
def get_cfp():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    if 'cfp_id' in data:
        cfp_id = data['cfp_id']
        cursor.execute("""
            SELECT user_id FROM public.\"CFP\" WHERE cfp_id = %s
        """, (cfp_id,))
        cfp=cursor.fetchone()
        if cfp:
            cfp_user_id = cfp[0]
            cursor.execute("""
                SELECT name, surname, telephone, email FROM public.\"User\" WHERE user_id = %s
            """, (cfp_user_id,))
            cfp_info = cursor.fetchone()
            cfp_name = f"{cfp_info[0]} {cfp_info[1]}"
            cfp_telephone = cfp_info[2]
            cfp_email = cfp_info[3]

            cursor.execute("""
                SELECT certificate FROM public.\"Certificate\" WHERE cfp_id = %s
            """, (cfp_id,))
            certificates = cursor.fetchall()
            cfp_certificates = []
            for certificate in certificates:
                cfp_certificates.append(certificate[0])
            cursor.execute("""
                SELECT education FROM public.\"Education\" WHERE cfp_id = %s
            """, (cfp_id,))
            educations = cursor.fetchall()
            cfp_educations = []
            for education in educations:
                cfp_educations.append(education[0])
            cursor.execute("""
                SELECT training FROM public.\"Training\" WHERE cfp_id = %s
            """, (cfp_id,))
            trainings = cursor.fetchall()
            cfp_trainings = []
            for training in trainings:
                cfp_trainings.append(training[0])
            cursor.execute("""
                SELECT experience FROM public.\"Experience\" WHERE cfp_id = %s
            """, (cfp_id,))
            experiences = cursor.fetchall()
            cfp_experiences = []
            for experience in experiences:
                cfp_experiences.append(experience[0])
            cursor.execute("""
                SELECT expert FROM public.\"Expert\" WHERE cfp_id = %s
            """, (cfp_id,))
            experts = cursor.fetchall()
            cfp_experts = []
            for expert in experts:
                cfp_experts.append(expert[0])
            cursor.execute("""
                SELECT fee FROM public.\"Fee\" WHERE cfp_id = %s
            """, (cfp_id,))
            fees = cursor.fetchall()
            cfp_fees = []
            for fee in fees:
                cfp_fees.append(fee[0])
            cursor.execute("""
                SELECT reason FROM public.\"Reason\" WHERE cfp_id = %s
            """, (cfp_id,))
            cfp_reason = cursor.fetchone()
            if cfp_reason:
                cfp_reason=cfp_reason[0]
            else:
                cfp_reason=""
            return jsonify({
                "cfp_name": cfp_name,
                "cfp_telephone": cfp_telephone,
                "cfp_email": cfp_email,
                "cfp_certificates": cfp_certificates,
                "cfp_educations": cfp_educations,
                "cfp_trainings": cfp_trainings,
                "cfp_experiences": cfp_experiences,
                "cfp_experts": cfp_experts,
                "cfp_fees": cfp_fees,
                "cfp_reason": cfp_reason,
            }), 200
        else:
            return jsonify({'message': "cfp_id not existed"}), 501
    else:
        return jsonify({'message': "blog_id not found"}), 200

@app.route('/get_cfp_image', methods=['POST'])
def get_cfp_image():
    data = request.json
    if 'cfp_id' in data:
        cfp_id = data['cfp_id']
        try:
            return send_file(f"../file-store/cfp/images/{cfp_id}.png", as_attachment=True)
        except:
            try:
                return send_file(f"../file-store/cfp/images/{cfp_id}.jpg", as_attachment=True)
            except:
                return jsonify({"message": "Unable to get file"}), 501
    else:
        return jsonify({'message': "cfp_id not found"}), 200