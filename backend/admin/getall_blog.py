import os
from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify, send_file
import datetime as date

@app.route('/admin/getall_blog', methods=['POST'])
def admin_getall_blog():
    data = request.json
    if 'user_id' in data:
        # Database Query
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_type FROM public.\"User\" WHERE user_id = %s", (data['user_id'],))
        user_type = cursor.fetchone()
        if user_type==None or user_type[0]!='A':
            return jsonify({"message": "this is not admin account"}), 401
        result = []
        cursor.execute("""
            SELECT blog_id, title, date, cfp_id, approval FROM public.\"Blog\" ORDER BY date DESC;
        """)
        blogs=cursor.fetchall()
        for blog in blogs:
            blog_id = blog[0]
            title = blog[1]
            date = blog[2]
            cfp_id = blog[3]
            approval = blog[4]
            if(approval):
                continue
            cursor.execute("""
                SELECT user_id FROM public.\"CFP\" WHERE cfp_id = %s
            """, (cfp_id, ))
            cfp_user_id=cursor.fetchone()[0]
            cursor.execute("""
                SELECT name, surname FROM public.\"User\" WHERE user_id = %s
            """, (cfp_user_id, ))
            cfp=cursor.fetchone()
            cfp_name = f"{cfp[0]} {cfp[1]}"
            cursor.execute("""
                SELECT tagname FROM public.\"Tag\" WHERE blog_id = %s
            """, (blog_id,))
            tags=[]
            for tag in cursor.fetchall():
                tags.append(tag[0])
            result.append({
                "blog_id": blog_id,
                "tags": tags,
                "cfp_name": cfp_name,
                "title": title,
                "date": date.strftime('%d/%m/%Y'),
            })
        return jsonify(result), 200
    else:
        return jsonify({"message": "user_id missing"}), 501