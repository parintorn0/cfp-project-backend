from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify

@app.route('/customer_goal', methods=['POST'])
def customer_goal():
    data = request.json
    if 'version_id' in data:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, amount, year, cashflow, growthrate FROM public.\"Goal\" WHERE version_id = %s", (data['version_id'],))
        goal = cursor.fetchone()
        cursor.execute("SELECT age, retirementage, deadage, inflation, expense, rate FROM public.\"Retirement\" WHERE version_id = %s", (data['version_id'],))
        retirement = cursor.fetchone()
        cursor.execute("SELECT name, amount, growthrate, type FROM public.\"Portfolio\" WHERE version_id = %s", (data['version_id'],))
        portfolios = cursor.fetchall()
        result={
            "retirement": None,
            "goal": None,
            "portfolio": [],
            }
        if goal:
            result['goal']={
                'name': str(goal[0]),
                'amount': str(goal[1]),
                'year': str(goal[2]),
                'cashflow': str(goal[3]),
                'growthrate': str(goal[4]),
                }
        if retirement:
            result['retirement']={
                'age': str(retirement[0]),
                'retirementage': str(retirement[1]),
                'deadage': str(retirement[2]),
                'inflation': str(retirement[3]),
                'expense': str(retirement[4]),
                'rate': str(retirement[5]),
                }
        for portfolio in portfolios:
            result['portfolio'].append({
                'name': str(portfolio[0]),
                'amount': str(portfolio[1]),
                'growthrate': str(portfolio[2]),
                'type': str(portfolio[3]),
                })
        return jsonify(result), 200
        
        cursor.close()
        conn.close()
    else:
        cursor.close()
        conn.close()
        return jsonify({"message": "Unable to recieve user id"}), 400