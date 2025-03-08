import os
from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify, send_file
import datetime as date

@app.route('/getall_blog', methods=['GET'])
def getall_blog():
    # Database Query
    conn = get_db_connection()
    cursor = conn.cursor()
    result = []
    cursor.execute("""
        SELECT blog_id, title, date, cfp_id, approval FROM public.\"Blog\" ORDER BY date DESC
    """)
    blogs=cursor.fetchall()
    for blog in blogs:
        blog_id = blog[0]
        title = blog[1]
        date = blog[2]
        cfp_id = blog[3]
        approval = blog[4]
        if(not approval):
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
            SELECT COUNT(blog_id) FROM public.\"Like\" WHERE blog_id = %s
        """, (blog_id,))
        like_count = cursor.fetchone()[0]
        cursor.execute("""
            SELECT tagname FROM public.\"Tag\" WHERE blog_id = %s
        """, (blog_id,))
        tags=[]
        for tag in cursor.fetchall():
            tags.append(tag[0])
        result.append({
            "blog_id": blog_id,
            "tags": tags,
            "like_count": like_count,
            "cfp_name": cfp_name,
            "title": title,
            "date": date.strftime('%d/%m/%Y'),
        })
    return jsonify(result), 200

@app.route('/get_blog', methods=['POST'])
def get_blog():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    if 'blog_id' in data:
        if 'user_id' not in data:
            return jsonify({"message": "user_id missing"}), 501
        user_id = data['user_id']
        blog_id = data['blog_id']
        cursor.execute("""
            SELECT title, date, cfp_id, approval FROM public.\"Blog\" WHERE blog_id = %s
        """, (blog_id,))
        blog=cursor.fetchone()
        title = blog[0]
        date = blog[1]
        cfp_id = blog[2]
        approval = blog[3]
        cursor.execute("""
            SELECT user_type FROM public.\"User\" WHERE user_id = %s
        """, (user_id,))
        user_type = cursor.fetchone()
        if user_type:
            if user_type[0]!='A' and not approval:
                return jsonify({'message': "Not Existed"}), 501
        cursor.execute("""
            SELECT user_id FROM public.\"CFP\" WHERE cfp_id = %s
        """, (cfp_id,))
        cfp_user_id = cursor.fetchone()[0]
        cursor.execute("""
            SELECT name, surname FROM public.\"User\" WHERE user_id = %s
        """, (cfp_user_id,))
        cfp = cursor.fetchone()
        cfp_name = f"{cfp[0]} {cfp[1]}"
        cursor.execute("""
            SELECT COUNT(blog_id) FROM public.\"Like\" WHERE blog_id = %s
        """, (blog_id,))
        like_count = cursor.fetchone()[0]
        cursor.execute("""
            SELECT tagname FROM public.\"Tag\" WHERE blog_id = %s
        """, (blog_id,))
        tags=[]
        for tag in cursor.fetchall():
            tags.append(tag[0])
        cursor.execute("""
            SELECT customer_id FROM public.\"Customer\" WHERE user_id = %s
        """, (user_id,))
        customer_id=cursor.fetchone()[0]
        cursor.execute("""
            SELECT COUNT(customer_id) FROM public.\"Like\" WHERE customer_id = %s AND blog_id = %s
        """, (customer_id, blog_id,))
        is_liked = cursor.fetchone()[0]
        if is_liked!=0:
            is_liked = True
        else:
            is_liked = False
        return jsonify({
            "cfp_id": cfp_id,
            "tags": tags,
            "like_count": like_count,
            "cfp_name": cfp_name,
            "title": title,
            "date": date.strftime('%d/%m/%Y'),
            "is_liked": is_liked,
        })
    else:
        return jsonify({'message': "blog_id not found"}), 200

@app.route('/get_blog_image', methods=['POST'])
def get_blog_image():
    data = request.json
    if 'blog_id' in data:
        blog_id = data['blog_id']
        try:
            return send_file(f"../file-store/blog/images/{blog_id}.png", as_attachment=True)
        except:
            try:
                return send_file(f"../file-store/blog/images/{blog_id}.jpg", as_attachment=True)
            except:
                return jsonify({"message": "Unable to get file"}), 501
    else:
        return jsonify({'message': "blog_id not found"}), 200

@app.route('/get_blog_pdf', methods=['POST'])
def get_blog_pdf():
    data = request.json
    if 'blog_id' in data:
        blog_id = data['blog_id']
        pdf_path = f"file-store/blog/pdfs/{blog_id}.pdf"
        if os.path.exists(pdf_path):
            print(f"File exists. Size: {os.path.getsize(pdf_path)} bytes")
        else:
            print("File not found.")
        try:
            return send_file(f"../file-store/blog/pdfs/{blog_id}.pdf", as_attachment=True)
        except:
            return jsonify({"message": "Unable to get file"}), 501
    else:
        return jsonify({'message': "blog_id not found"}), 200

@app.route('/like_blog', methods=['POST'])
def like_blog():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    if 'blog_id' in data:
        if 'user_id' not in data:
            return jsonify({"message": "user_id missing"}), 501
        user_id = data['user_id']
        blog_id = data['blog_id']
        cursor.execute("""
            SELECT customer_id FROM public.\"Customer\" WHERE user_id = %s
        """, (user_id,))
        customer_id=cursor.fetchone()[0]
        cursor.execute("""
            SELECT COUNT(customer_id) FROM public.\"Like\" WHERE customer_id = %s AND blog_id = %s
        """, (customer_id, blog_id,))
        if cursor.fetchone()[0]==1:
            cursor.execute("""
                DELETE FROM public.\"Like\" WHERE customer_id = %s AND blog_id = %s;
            """, (customer_id, blog_id,))
            conn.commit()
            return jsonify({'message': "Unliked"}), 200
        else:
            cursor.execute("""
                INSERT INTO public.\"Like\" (customer_id, blog_id) VALUES (%s, %s);
            """, (customer_id, blog_id,))
            conn.commit()
            return jsonify({'message': "Liked"}), 200
    else:
        return jsonify({'message': "blog_id not found"}), 504
