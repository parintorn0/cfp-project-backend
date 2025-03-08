import os
from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify
from PIL import Image
import io
from datetime import date

@app.route('/upload_blog', methods=['POST'])
def upload_blog():
    if 'image' not in request.files or 'pdf' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    title = request.form.get('title')
    user_id = request.form.get('user_id')
    tags = [
        request.form.get('tag1'),
        request.form.get('tag2'),
        request.form.get('tag3'),
        request.form.get('tag4'),
        request.form.get('tag5'),
        ]
    image = request.files['image']
    pdf = request.files['pdf']
    if title == '':
        return jsonify({'message': 'No title'}), 400
    if image.filename == '':
        return jsonify({'message': 'No selected image file'}), 400
    if pdf.filename == '':
        return jsonify({'message': 'No selected pdf file'}), 400
    if not allowed_file(image.filename, ['png', 'jpg']):
        return jsonify({'message': 'image is not correct type'}), 501
    if not allowed_file(pdf.filename, ['pdf']):
        return jsonify({'message': 'image is not correct type'}), 501
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cfp_id FROM public.\"CFP\" WHERE user_id = %s
        """, (user_id,))
    cfp_id = cursor.fetchone()
    if not cfp_id:
        return jsonify({'error': 'user_id is not CFP'}), 501
    cfp_id = cfp_id[0]
    cursor.execute("""
        INSERT INTO public.\"Blog\" (title, date, cfp_id) VALUES (%s, %s, %s) RETURNING blog_id;
        """, (title, date.today(), cfp_id))
    blog_id=cursor.fetchone()[0]
    inserted_tags=[]
    for tag in tags:
        if tag!='':
            if tag not in inserted_tags:
                inserted_tags.append(tag)
                cursor.execute("""
                    INSERT INTO public.\"Tag\" (tagname, blog_id) VALUES (%s, %s) RETURNING blog_id;
                    """, (tag, blog_id))
    conn.commit()
    cursor.close()
    conn.close()
    print(os.path.dirname(os.path.abspath(__file__)))
    with open(f"file-store/blog/images/{blog_id}.{image.filename.rsplit('.', 1)[1].lower()}", "wb") as f:
        f.write(image.read())
    with open(f"file-store/blog/pdfs/{blog_id}.{pdf.filename.rsplit('.', 1)[1].lower()}", "wb") as f:
        f.write(image.read())
    return jsonify({"message": "Uploaded"}), 200

def is_pdf(binary_data):
    return binary_data[:5] == b'%PDF-'

def is_valid_png(binary_data):
    try:
        img = Image.open(io.BytesIO(binary_data))
        return img.format == "PNG"
    except Exception:
        return False
    
def is_valid_jpg(binary_data):
    try:
        img = Image.open(io.BytesIO(binary_data))
        return img.format == "JPG"
    except Exception:
        return False

def allowed_file(filename, extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions