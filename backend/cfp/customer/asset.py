from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify

@app.route('/customer_asset', methods=['POST'])
def customer_asset():
    data = request.json
    if 'version_id' in data:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, amount, subtype, growthrate, type FROM public.\"Asset\" WHERE version_id = %s", (data['version_id'],))
        assets = cursor.fetchall()
        result=[]
        for asset in assets:
            result.append({
                'name': str(asset[0]),
                'amount': str(asset[1]),
                'subtype': str(asset[2]),
                'growthrate': str(asset[3]),
                'type': str(asset[4]),
                })
        cursor.close()
        conn.close()
        return jsonify(result), 200
    else:
        cursor.close()
        conn.close()
        return jsonify({"message": "Unable to recieve user id"}), 400