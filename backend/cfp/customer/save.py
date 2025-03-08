from backend import app
from backend.db_connection import get_db_connection
from flask import request, jsonify
from datetime import date

@app.route('/save', methods=['POST'])
def customer_save():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    # get cutomer id version number
    cursor.execute("SELECT customer_id FROM public.\"Version\" WHERE version_id = %s ORDER BY version_id DESC", (data['version_id'],))
    version = cursor.fetchone()
    customer_id = version[0]
    # check all
    version_id = data['version_id']
    if not version_id:
        return jsonify({"message": "Missing version_id"}), 501
    assets = data['assets']
    liabilities = data['liabilities']
    incomes = data['incomes']
    expenses = data['expenses']
    goal = data['goals']['goal']
    retirement = data['goals']['retirement']
    portfolios=[]
    if 'portfolio' in data['goals']:
        portfolios = data['goals']['portfolio']
    # check if input all
    for asset in assets:
        if len(asset['name']) == 0 or len(asset['amount']) == 0 or len(asset['growthrate']) == 0 or len(asset['subtype']) == 0 or len(asset['type']) == 0:
            return jsonify({"message": "Some asset might not be inputed"}), 501
        try:
            float(asset['amount'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Asset's amount is not number"}), 501
        try:
            float(asset['growthrate']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Asset's growth rate is not number"}), 501
    for liability in liabilities:
        if len(liability['name']) == 0 or len(liability['amount']) == 0 or len(liability['start']) == 0 or len(liability['duration']) == 0 or len(liability['rate']) == 0 or len(liability['term']) == 0:
            return jsonify({"message": "Some liability might not be inputed"}), 501
        try:
            int(liability['duration'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Liability's duration is not correct"}), 501
        try:
            float(liability['amount'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Liability's amount is not number"}), 501
        try:
            float(liability['rate']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Liability's rate is not number"}), 501
    for income in incomes:
        if len(income['name']) == 0 or len(income['amount']) == 0 or len(income['growthrate']) == 0 or len(income['type']) == 0:
            return jsonify({"message": "Some income might not be inputed"}), 501
        try:
            float(income['amount'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Income's amount is not number"}), 501
        try:
            float(income['growthrate']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Income's growth rate is not number"}), 501
    for expense in expenses:
        if len(expense['name']) == 0 or len(expense['amount']) == 0 or len(expense['growthrate']) == 0:
            return jsonify({"message": "Some expense might not be inputed"}), 501
        try:
            float(expense['amount'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Expense's amount is not number"}), 501
        try:
            float(expense['growthrate']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Expense's growth rate is not number"}), 501
    if len(goal['name']) == 0 and len(goal['amount']) == 0 and len(goal['year']) == 0 and len(goal['growthrate']) == 0 and len(goal['cashflow']) == 0:
        goal=None
    elif len(goal['name']) == 0 or len(goal['amount']) == 0 or len(goal['year']) == 0 or len(goal['growthrate']) == 0 or len(goal['cashflow']) == 0:
        return jsonify({"message": "Goal is not all be inputed"}), 501
    else:
        try:
            float(goal['amount'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Goal's amount is not number"}), 501
        try:
            int(goal['year']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Goal's year is not correct"}), 501
        try:
            float(goal['growthrate'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Goal's growth rate is not number"}), 501
        try:
            float(goal['cashflow'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Goal's growth rate is not number"}), 501
    if len(retirement['age']) == 0 and len(retirement['deadage']) == 0 and len(retirement['inflation']) == 0 and len(retirement['retirementage']) == 0 and len(retirement['expense']) == 0 and len(retirement['rate']) == 0:
        retirement=None
    elif len(retirement['age']) == 0 or len(retirement['deadage']) == 0 or len(retirement['inflation']) == 0 or len(retirement['retirementage']) == 0 or len(retirement['expense']) == 0 or len(retirement['rate']) == 0:
        return jsonify({"message": "Retirement is not all be inputed"}), 501
    else:
        try:
            int(retirement['age'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Retirement's current age is not number"}), 501
        try:
            int(retirement['deadage']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Retirement's dead age is not number"}), 501
        try:
            int(retirement['retirementage']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Retirement's age is not number"}), 501
        try:
            float(retirement['inflation']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Retirement's inflation is not number"}), 501
        try:
            float(retirement['expense']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Retirement's expense is not number"}), 501
        try:
            float(retirement['rate']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Retirement's rate is not number"}), 501
    for portfolio in portfolios:
        if len(portfolio['amount']) == 0 or len(portfolio['growthrate']) == 0 or len(portfolio['name']) == 0 or len(portfolio['type']) == 0:
            return jsonify({"message": "Portfolio is not all be inputed"}), 501
        else:
            try:
                float(portfolio['amount']),
            except:
                cursor.close()
                conn.close()
                return jsonify({"message": "Portfolio's amount is not number"}), 501
            try:
                float(portfolio['growthrate']),
            except:
                cursor.close()
                conn.close()
                return jsonify({"message": "Portfolio's growthrate is not number"}), 501
    # delete all existed version_id tables
    cursor.execute("""
    DELETE FROM public.\"Asset\" WHERE version_id = %s;
    """, (version_id,))
    cursor.execute("""
    DELETE FROM public.\"Liability\" WHERE version_id = %s;
    """, (version_id,))
    cursor.execute("""
    DELETE FROM public.\"Income\" WHERE version_id = %s;
    """, (version_id,))
    cursor.execute("""
    DELETE FROM public.\"Expense\" WHERE version_id = %s;
    """, (version_id,))
    cursor.execute("""
    DELETE FROM public.\"Goal\" WHERE version_id = %s;
    """, (version_id,))
    cursor.execute("""
    DELETE FROM public.\"Retirement\" WHERE version_id = %s;
    """, (version_id,))
    cursor.execute("""
    DELETE FROM public.\"Portfolio\" WHERE version_id = %s;
    """, (version_id,))
    for asset in assets:
        cursor.execute("""
        INSERT INTO public.\"Asset\" (name, amount, subtype, growthrate, type, version_id) VALUES (%s, %s, %s, %s, %s, %s);
        """, (asset['name'], asset['amount'], asset['subtype'], asset['growthrate'], asset['type'], version_id))
    for liability in liabilities:
        cursor.execute("""
        INSERT INTO public.\"Liability\" (name, amount, rate, start, duration, term, version_id) VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (liability['name'], liability['amount'], liability['rate'], liability['start'], liability['duration'], liability['term'], version_id))
    for income in incomes:
        cursor.execute("""
        INSERT INTO public.\"Income\" (name, amount, growthrate, type, version_id) VALUES (%s, %s, %s, %s, %s);
        """, (income['name'], income['amount'], income['growthrate'], income['type'], version_id))
    for expense in expenses:
        cursor.execute("""
        INSERT INTO public.\"Expense\" (name, amount, growthrate, version_id) VALUES (%s, %s, %s, %s);
        """, (expense['name'], expense['amount'], expense['growthrate'], version_id))
    if not (goal==None):
        cursor.execute("""
        INSERT INTO public.\"Goal\" (name, amount, year, growthrate, cashflow, version_id) VALUES (%s, %s, %s, %s, %s, %s);
        """, (goal['name'], goal['amount'], goal['year'], goal['growthrate'], goal['cashflow'], version_id))
    if not (retirement==None):
        cursor.execute("""
        INSERT INTO public.\"Retirement\" (age, retirementage, deadage, inflation, expense, rate, version_id) VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (retirement['age'], retirement['retirementage'], retirement['deadage'], retirement['inflation'], retirement['expense'], retirement['rate'], version_id))
    for portfolio in portfolios:
        cursor.execute("""
        INSERT INTO public.\"Portfolio\" (name, amount, growthrate, type, version_id) VALUES (%s, %s, %s, %s, %s );
        """, (portfolio['name'], portfolio['amount'], portfolio['growthrate'], portfolio['type'], version_id))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Saved"}), 200

@app.route('/save_as', methods=['POST'])
def customer_save_as():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    # get cutomer id version number
    cursor.execute("SELECT customer_id FROM public.\"Version\" WHERE version_id = %s ORDER BY version_id DESC", (data['version_id'],))
    version = cursor.fetchone()
    customer_id = version[0]
    # check all
    assets = data['assets']
    liabilities = data['liabilities']
    incomes = data['incomes']
    expenses = data['expenses']
    goal = data['goals']['goal']
    retirement = data['goals']['retirement']
    portfolios=[]
    if 'portfolio' in data['goals']:
        portfolios = data['goals']['portfolio']
    # check if input all
    for asset in assets:
        if len(asset['name']) == 0 or len(asset['amount']) == 0 or len(asset['growthrate']) == 0 or len(asset['subtype']) == 0 or len(asset['type']) == 0:
            return jsonify({"message": "Some asset might not be inputed"}), 501
        try:
            float(asset['amount'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Asset's amount is not number"}), 501
        try:
            float(asset['growthrate']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Asset's growth rate is not number"}), 501
    for liability in liabilities:
        if len(liability['name']) == 0 or len(liability['amount']) == 0 or len(liability['start']) == 0 or len(liability['duration']) == 0 or len(liability['rate']) == 0 or len(liability['term']) == 0:
            return jsonify({"message": "Some liability might not be inputed"}), 501
        try:
            int(liability['duration'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Liability's duration is not correct"}), 501
        try:
            float(liability['amount'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Liability's amount is not number"}), 501
        try:
            float(liability['rate']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Liability's rate is not number"}), 501
    for income in incomes:
        if len(income['name']) == 0 or len(income['amount']) == 0 or len(income['growthrate']) == 0 or len(income['type']) == 0:
            return jsonify({"message": "Some income might not be inputed"}), 501
        try:
            float(income['amount'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Income's amount is not number"}), 501
        try:
            float(income['growthrate']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Income's growth rate is not number"}), 501
    for expense in expenses:
        if len(expense['name']) == 0 or len(expense['amount']) == 0 or len(expense['growthrate']) == 0:
            return jsonify({"message": "Some expense might not be inputed"}), 501
        try:
            float(expense['amount'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Expense's amount is not number"}), 501
        try:
            float(expense['growthrate']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Expense's growth rate is not number"}), 501
    
    if len(goal['name']) == 0 and len(goal['amount']) == 0 and len(goal['year']) == 0 and len(goal['growthrate']) == 0 and len(goal['cashflow']) == 0:
        goal=None
    elif len(goal['name']) == 0 or len(goal['amount']) == 0 or len(goal['year']) == 0 or len(goal['growthrate']) == 0 or len(goal['cashflow']) == 0:
        return jsonify({"message": "Goal is not all be inputed"}), 501
    else:
        try:
            float(goal['amount'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Goal's amount is not number"}), 501
        try:
            int(goal['year']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Goal's year is not correct"}), 501
        try:
            float(goal['growthrate'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Goal's growth rate is not number"}), 501
        try:
            float(goal['cashflow'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Goal's growth rate is not number"}), 501
    if len(retirement['age']) == 0 and len(retirement['deadage']) == 0 and len(retirement['inflation']) == 0 and len(retirement['retirementage']) == 0 and len(retirement['expense']) == 0 and len(retirement['rate']) == 0:
        retirement=None
    elif len(retirement['age']) == 0 or len(retirement['deadage']) == 0 or len(retirement['inflation']) == 0 or len(retirement['retirementage']) == 0 or len(retirement['expense']) == 0 or len(retirement['rate']) == 0:
        return jsonify({"message": "Retirement is not all be inputed"}), 501
    else:
        try:
            int(retirement['age'])
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Retirement's current age is not number"}), 501
        try:
            int(retirement['deadage']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Retirement's dead age is not number"}), 501
        try:
            int(retirement['retirementage']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Retirement's age is not number"}), 501
        try:
            float(retirement['inflation']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Retirement's inflation is not number"}), 501
        try:
            float(retirement['expense']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Retirement's expense is not number"}), 501
        try:
            float(retirement['rate']),
        except:
            cursor.close()
            conn.close()
            return jsonify({"message": "Retirement's rate is not number"}), 501
    for portfolio in portfolios:
        if len(portfolio['amount']) == 0 or len(portfolio['growthrate']) == 0 or len(portfolio['name']) == 0 or len(portfolio['type']) == 0:
            return jsonify({"message": "Portfolio is not all be inputed"}), 501
        else:
            try:
                float(portfolio['amount']),
            except:
                cursor.close()
                conn.close()
                return jsonify({"message": "Portfolio's amount is not number"}), 501
            try:
                float(portfolio['growthrate']),
            except:
                cursor.close()
                conn.close()
                return jsonify({"message": "Portfolio's growthrate is not number"}), 501
    # insert to tables
    cursor.execute("""
    SELECT version_number FROM public.\"Version\" WHERE customer_id=%s ORDER BY version_id DESC;
    """, (customer_id,))
    version_number=cursor.fetchone()[0]+1
    cursor.execute("""
    INSERT INTO public.\"Version\" (customer_id, date, version_number) VALUES (%s, %s, %s)
    RETURNING version_id;
    """, (customer_id, date.today(), version_number))
    version_id=cursor.fetchone()[0]
    for asset in assets:
        cursor.execute("""
        INSERT INTO public.\"Asset\" (name, amount, subtype, growthrate, type, version_id) VALUES (%s, %s, %s, %s, %s, %s);
        """, (asset['name'], asset['amount'], asset['subtype'], asset['growthrate'], asset['type'], version_id))
    for liability in liabilities:
        cursor.execute("""
        INSERT INTO public.\"Liability\" (name, amount, rate, start, duration, term, version_id) VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (liability['name'], liability['amount'], liability['rate'], liability['start'], liability['duration'], liability['term'], version_id))
    for income in incomes:
        cursor.execute("""
        INSERT INTO public.\"Income\" (name, amount, growthrate, type, version_id) VALUES (%s, %s, %s, %s, %s);
        """, (income['name'], income['amount'], income['growthrate'], income['type'], version_id))
    for expense in expenses:
        cursor.execute("""
        INSERT INTO public.\"Expense\" (name, amount, growthrate, version_id) VALUES (%s, %s, %s, %s);
        """, (expense['name'], expense['amount'], expense['growthrate'], version_id))
    if not (goal==None):
        cursor.execute("""
        INSERT INTO public.\"Goal\" (name, amount, year, growthrate, cashflow, version_id) VALUES (%s, %s, %s, %s, %s, %s);
        """, (goal['name'], goal['amount'], goal['year'], goal['growthrate'], goal['cashflow'], version_id))
    if not (retirement==None):
        cursor.execute("""
        INSERT INTO public.\"Retirement\" (age, retirementage, deadage, inflation, expense, rate, version_id) VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (retirement['age'], retirement['retirementage'], retirement['deadage'], retirement['inflation'], retirement['expense'], retirement['rate'], version_id))
    for portfolio in portfolios:
        cursor.execute("""
        INSERT INTO public.\"Portfolio\" (name, amount, growthrate, type, version_id) VALUES (%s, %s, %s, %s, %s );
        """, (portfolio['name'], portfolio['amount'], portfolio['growthrate'], portfolio['type'], version_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Saved"}), 200
