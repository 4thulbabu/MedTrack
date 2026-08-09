from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'med_app_secret_key_123')
app.config['TEMPLATES_AUTO_RELOAD'] = True

DATABASE = 'pharmacy.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        conn.execute('''
                     CREATE TABLE IF NOT EXISTS shops
                     (
                         shop_id
                         TEXT
                         PRIMARY
                         KEY,
                         name
                         TEXT,
                         location
                         TEXT,
                         password
                         TEXT,
                         contact
                         TEXT,
                         email
                         TEXT,
                         map_url
                         TEXT
                     )
                     ''')
        conn.execute('''
                     CREATE TABLE IF NOT EXISTS inventory
                     (
                         id
                         INTEGER
                         PRIMARY
                         KEY
                         AUTOINCREMENT,
                         shop_id
                         TEXT,
                         med_name
                         TEXT,
                         stock_count
                         INTEGER
                         DEFAULT
                         0,
                         price
                         REAL
                         DEFAULT
                         0.0,
                         FOREIGN
                         KEY
                     (
                         shop_id
                     ) REFERENCES shops
                     (
                         shop_id
                     )
                         )
                     ''')
        conn.execute('''
                     CREATE TABLE IF NOT EXISTS sales
                     (
                         id
                         INTEGER
                         PRIMARY
                         KEY
                         AUTOINCREMENT,
                         shop_id
                         TEXT,
                         med_name
                         TEXT,
                         quantity
                         INTEGER,
                         price_per_unit
                         REAL,
                         total_amount
                         REAL,
                         sale_date
                         TIMESTAMP
                         DEFAULT
                         CURRENT_TIMESTAMP,
                         FOREIGN
                         KEY
                     (
                         shop_id
                     ) REFERENCES shops
                     (
                         shop_id
                     ) ON DELETE CASCADE
                         )
                     ''')
        conn.commit()


init_db()


def get_all_medicine_names():
    try:
        with get_db_connection() as conn:
            meds = conn.execute("SELECT DISTINCT med_name FROM inventory").fetchall()
            return [m['med_name'] for m in meds]
    except sqlite3.Error:
        return []


# ---------- PUBLIC ROUTES ----------

@app.route('/')
def index():
    query = request.args.get('search', '').lower().strip()
    location_query = request.args.get('location', '').lower().strip()
    results = []
    all_meds = get_all_medicine_names()
    if query:
        with get_db_connection() as conn:
            sql = '''
                  SELECT s.name, \
                         s.location, \
                         s.contact, \
                         s.email, \
                         s.map_url,
                         i.med_name, \
                         i.stock_count, \
                         i.price
                  FROM inventory i
                           JOIN shops s ON i.shop_id = s.shop_id
                  WHERE LOWER(i.med_name) LIKE ?
                    AND LOWER(s.location) LIKE ?
                    AND i.stock_count > 0 \
                  '''
            results = conn.execute(sql, (f'%{query}%', f'%{location_query}%')).fetchall()
    return render_template('index.html', results=results, all_meds=all_meds)


# ---------- AUTHENTICATION ----------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        sid = request.form.get('shop_id', '').strip()
        pwd = request.form.get('password', '').strip()
        with get_db_connection() as conn:
            user = conn.execute("SELECT * FROM shops WHERE shop_id=?", (sid,)).fetchone()
        if user and user['password'] == pwd:
            session['shop_id'] = sid
            session['shop_name'] = user['name']
            return redirect(url_for('dashboard'))
        flash("Invalid Shop ID or Password.", "danger")
    return render_template('login.html')


from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'med_app_secret_key_123')
app.config['TEMPLATES_AUTO_RELOAD'] = True

DATABASE = 'pharmacy.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        conn.execute('''
                     CREATE TABLE IF NOT EXISTS shops
                     (
                         shop_id
                         TEXT
                         PRIMARY
                         KEY,
                         name
                         TEXT,
                         location
                         TEXT,
                         password
                         TEXT,
                         contact
                         TEXT,
                         email
                         TEXT,
                         map_url
                         TEXT
                     )
                     ''')
        conn.execute('''
                     CREATE TABLE IF NOT EXISTS inventory
                     (
                         id
                         INTEGER
                         PRIMARY
                         KEY
                         AUTOINCREMENT,
                         shop_id
                         TEXT,
                         med_name
                         TEXT,
                         stock_count
                         INTEGER
                         DEFAULT
                         0,
                         price
                         REAL
                         DEFAULT
                         0.0,
                         FOREIGN
                         KEY
                     (
                         shop_id
                     ) REFERENCES shops
                     (
                         shop_id
                     )
                         )
                     ''')
        conn.execute('''
                     CREATE TABLE IF NOT EXISTS sales
                     (
                         id
                         INTEGER
                         PRIMARY
                         KEY
                         AUTOINCREMENT,
                         shop_id
                         TEXT,
                         med_name
                         TEXT,
                         quantity
                         INTEGER,
                         price_per_unit
                         REAL,
                         total_amount
                         REAL,
                         sale_date
                         TIMESTAMP
                         DEFAULT
                         CURRENT_TIMESTAMP,
                         FOREIGN
                         KEY
                     (
                         shop_id
                     ) REFERENCES shops
                     (
                         shop_id
                     ) ON DELETE CASCADE
                         )
                     ''')
        conn.commit()


init_db()


def get_all_medicine_names():
    try:
        with get_db_connection() as conn:
            meds = conn.execute("SELECT DISTINCT med_name FROM inventory").fetchall()
            return [m['med_name'] for m in meds]
    except sqlite3.Error:
        return []


# ---------- PUBLIC ROUTES ----------

@app.route('/')
def index():
    query = request.args.get('search', '').lower().strip()
    location_query = request.args.get('location', '').lower().strip()
    results = []
    all_meds = get_all_medicine_names()
    if query:
        with get_db_connection() as conn:
            sql = '''
                  SELECT s.name, \
                         s.location, \
                         s.contact, \
                         s.email, \
                         s.map_url,
                         i.med_name, \
                         i.stock_count, \
                         i.price
                  FROM inventory i
                           JOIN shops s ON i.shop_id = s.shop_id
                  WHERE LOWER(i.med_name) LIKE ?
                    AND LOWER(s.location) LIKE ?
                    AND i.stock_count > 0 \
                  '''
            results = conn.execute(sql, (f'%{query}%', f'%{location_query}%')).fetchall()
    return render_template('index.html', results=results, all_meds=all_meds)


# ---------- AUTHENTICATION ----------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        sid = request.form.get('shop_id', '').strip()
        pwd = request.form.get('password', '').strip()
        with get_db_connection() as conn:
            user = conn.execute("SELECT * FROM shops WHERE shop_id=?", (sid,)).fetchone()
        if user and user['password'] == pwd:
            session['shop_id'] = sid
            session['shop_name'] = user['name']
            return redirect(url_for('dashboard'))
        flash("Invalid Shop ID or Password.", "danger")
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        sid = request.form.get('shop_id', '').strip()
        name = request.form.get('name', '').strip()
        loc = request.form.get('location', '').strip()
        pwd = request.form.get('password', '').strip()
        if not all([sid, pwd, name, loc]):
            flash("All required fields must be filled.", "warning")
            return redirect(url_for('register'))
        try:
            with get_db_connection() as conn:
                conn.execute(
                    "INSERT INTO shops (shop_id, name, location, password, contact, email, map_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (sid, name, loc, pwd, request.form.get('contact'), request.form.get('email'),
                     request.form.get('map_url'))
                )
                conn.commit()
            flash("Registration successful!", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Shop ID already exists.", "danger")
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------- DASHBOARD & INVENTORY ----------

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'shop_id' not in session:
        return redirect(url_for('login'))
    sid = session['shop_id']
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        try:
            with get_db_connection() as conn:
                if form_type == 'edit_shop':
                    conn.execute("UPDATE shops SET name=?, location=?, contact=?, email=?, map_url=? WHERE shop_id=?",
                                 (request.form.get('name'), request.form.get('location'), request.form.get('contact'),
                                  request.form.get('email'), request.form.get('map_url'), sid))
                elif form_type == 'add':
                    med = request.form.get('med_name', '').lower().strip()
                    conn.execute(
                        "INSERT OR REPLACE INTO inventory (shop_id, med_name, stock_count, price) VALUES (?, ?, ?, ?)",
                        (sid, med, int(request.form.get('stock', 0)), float(request.form.get('price', 0.0))))
                elif form_type == 'update_stock':
                    conn.execute("UPDATE inventory SET stock_count=? WHERE shop_id=? AND med_name=?",
                                 (int(request.form.get('stock', 0)), sid, request.form.get('med_name')))
                elif form_type == 'update_price':
                    conn.execute("UPDATE inventory SET price=? WHERE shop_id=? AND med_name=?",
                                 (float(request.form.get('price', 0.0)), sid, request.form.get('med_name')))
                conn.commit()
            flash("Updates saved!", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

    with get_db_connection() as conn:
        shop = conn.execute("SELECT * FROM shops WHERE shop_id=?", (sid,)).fetchone()
        stocks = conn.execute(
            "SELECT med_name, stock_count, price FROM inventory WHERE shop_id=? ORDER BY med_name ASC",
            (sid,)).fetchall()
        rev_row = conn.execute(
            "SELECT SUM(total_amount) as daily_total FROM sales WHERE shop_id=? AND DATE(sale_date) = DATE('now')",
            (sid,)).fetchone()
        today_revenue = rev_row['daily_total'] if rev_row['daily_total'] else 0
    return render_template('dashboard.html', shop=shop, stocks=stocks, today_revenue=today_revenue)


@app.route('/inventory')
def inventory_list():
    if 'shop_id' not in session: return redirect(url_for('login'))
    sid = session['shop_id']
    with get_db_connection() as conn:
        shop = conn.execute("SELECT * FROM shops WHERE shop_id=?", (sid,)).fetchone()
        stocks = conn.execute("SELECT * FROM inventory WHERE shop_id=? ORDER BY med_name ASC", (sid,)).fetchall()
    return render_template('inventory_list.html', shop=shop, stocks=stocks)


# ---------- BILLING & SALES REPORTS ----------

@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if 'shop_id' not in session: return redirect(url_for('login'))
    sid = session['shop_id']
    if request.method == 'POST':
        names = request.form.getlist('med_name[]')
        qtys = request.form.getlist('quantity[]')
        with get_db_connection() as conn:
            for n, q in zip(names, qtys):
                clean_name = n.lower().strip()
                if clean_name and q:
                    item = conn.execute("SELECT price FROM inventory WHERE shop_id=? AND med_name=?",
                                        (sid, clean_name)).fetchone()
                    if item:
                        qty = int(q)
                        conn.execute(
                            "INSERT INTO sales (shop_id, med_name, quantity, price_per_unit, total_amount) VALUES (?, ?, ?, ?, ?)",
                            (sid, clean_name, qty, item['price'], item['price'] * qty))
                        conn.execute(
                            "UPDATE inventory SET stock_count = MAX(0, stock_count - ?) WHERE shop_id=? AND med_name=?",
                            (qty, sid, clean_name))
            conn.commit()
        flash("Billing complete!", "success")
        return redirect(url_for('dashboard'))
    with get_db_connection() as conn:
        items = conn.execute("SELECT * FROM inventory WHERE shop_id=? AND stock_count > 0", (sid,)).fetchall()
    return render_template('billing.html', available_items=items, shop_name=session.get('shop_name'))


@app.route('/sales_report')
def sales_report():
    if 'shop_id' not in session: return redirect(url_for('login'))
    sid = session['shop_id']
    with get_db_connection() as conn:
        history = conn.execute(
            "SELECT sale_date as date, med_name, quantity, total_amount as total_price FROM sales WHERE shop_id=? ORDER BY sale_date DESC",
            (sid,)).fetchall()
        stats = conn.execute(
            "SELECT SUM(total_amount) as total_revenue, COUNT(*) as transaction_count FROM sales WHERE shop_id=? AND DATE(sale_date) = DATE('now')",
            (sid,)).fetchone()
        today_details = {
            'total_revenue': stats['total_revenue'] if stats['total_revenue'] else 0.0,
            'transaction_count': stats['transaction_count'] if stats['transaction_count'] else 0
        }
    return render_template('sales_report.html', history=history, details=today_details)


# ---------- QUICK ACTIONS (AJAX COMPATIBLE) ----------

@app.route('/increase_stock_one/<med>')
def increase_stock_one(med):
    if 'shop_id' in session:
        with get_db_connection() as conn:
            conn.execute("UPDATE inventory SET stock_count = stock_count + 1 WHERE shop_id=? AND med_name=?",
                         (session['shop_id'], med.lower()))
            conn.commit()
        return jsonify(status="success"), 200
    return jsonify(status="unauthorized"), 401


@app.route('/decrease_stock_one/<med>')
def decrease_stock_one(med):
    if 'shop_id' in session:
        with get_db_connection() as conn:
            conn.execute("UPDATE inventory SET stock_count = MAX(0, stock_count - 1) WHERE shop_id=? AND med_name=?",
                         (session['shop_id'], med.lower()))
            conn.commit()
        return jsonify(status="success"), 200
    return jsonify(status="unauthorized"), 401


@app.route('/delete_medicine/<med>')
def delete_medicine(med):
    if 'shop_id' in session:
        with get_db_connection() as conn:
            conn.execute("DELETE FROM inventory WHERE shop_id=? AND med_name=?", (session['shop_id'], med.lower()))
            conn.commit()
    return redirect(url_for('dashboard'))


@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    # Fixes the 404 error when clicking 'Delete Account'
    if 'shop_id' not in session: return redirect(url_for('login'))
    sid = session['shop_id']
    with get_db_connection() as conn:
        conn.execute("DELETE FROM shops WHERE shop_id=?", (sid,))
        conn.execute("DELETE FROM inventory WHERE shop_id=?", (sid,))
        conn.execute("DELETE FROM sales WHERE shop_id=?", (sid,))
        conn.commit()
    session.clear()
    flash("Account deleted successfully.", "success")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)