import os
from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify, send_file
import datetime as date

@app.route('/admin/approve_blog', methods=['POST'])
def admin_approve_blog():
    data = request.json
    if 'user_id' in data:
        if 'blog_id' in data:
            # Database Query
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT user_type FROM public.\"User\" WHERE user_id = %s", (data['user_id'],))
            user_type = cursor.fetchone()
            if user_type==None or user_type[0]!='A':
                return jsonify({"message": "this is not admin account"}), 401
            blog_id = data['blog_id']
            cursor.execute("""
                UPDATE public.\"Blog\" SET approval = true WHERE blog_id = %s
            """, (blog_id,))
            conn.commit()
            return jsonify({"message": "Approved"}), 200
        else:
            return jsonify({"message": "blog_id missing"}), 501
    else:
        return jsonify({"message": "user_id missing"}), 501
    
@app.route('/admin/decline_blog', methods=['POST'])
def admin_decline_blog():
    data = request.json
    if 'user_id' in data:
        if 'blog_id' in data:
            # Database Query
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT user_type FROM public.\"User\" WHERE user_id = %s", (data['user_id'],))
            user_type = cursor.fetchone()
            if user_type==None or user_type[0]!='A':
                return jsonify({"message": "this is not admin account"}), 401
            blog_id = data['blog_id']
            cursor.execute("""
                DELETE FROM public.\"Blog\" WHERE blog_id = %s;
            """, (blog_id,))
            if os.path.exists(f"file-store/blog/images/{blog_id}.jpg"):
                os.remove(f"file-store/blog/images/{blog_id}.jpg")
            else:
                os.remove(f"file-store/blog/images/{blog_id}.png")
            os.remove(f"file-store/blog/pdfs/{blog_id}.pdf")
            conn.commit()
            return jsonify({"message": "Declined"}), 200
        else:
            return jsonify({"message": "blog_id missing"}), 501
    else:
        return jsonify({"message": "user_id missing"}), 501