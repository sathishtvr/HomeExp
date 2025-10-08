#!/usr/bin/env python3
"""
Simple working backend for Personal Finance Tracker
This is a minimal version that should work without issues
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime, timedelta
import json

# Create Flask app
app = Flask(__name__)
CORS(app)

# Database setup
DB_PATH = 'finance_simple.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            month TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create assets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT NOT NULL,
            name TEXT NOT NULL,
            value REAL NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS liabilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL
        )
    ''')
    
    # Create income table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            is_recurring INTEGER DEFAULT 0
        )
    ''')
    
    # Create expense templates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expense_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            subcategory TEXT,
            default_amount REAL DEFAULT 0,
            description TEXT,
            is_recurring INTEGER DEFAULT 0
        )
    ''')
    
    # Create income templates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS income_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            subcategory TEXT,
            default_amount REAL DEFAULT 0,
            description TEXT,
            is_recurring INTEGER DEFAULT 1
        )
    ''')
    
    # Create asset templates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS asset_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            subcategory TEXT,
            default_amount REAL DEFAULT 0,
            description TEXT
        )
    ''')
    
    # Create liability templates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS liability_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            subcategory TEXT,
            default_amount REAL DEFAULT 0,
            description TEXT
        )
    ''')
    
    # Create RD table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recurring_deposits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bank_name TEXT NOT NULL,
            account_number TEXT,
            monthly_amount REAL NOT NULL,
            interest_rate REAL NOT NULL,
            tenure INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            maturity_date TEXT,
            maturity_amount REAL,
            status TEXT DEFAULT 'Active'
        )
    ''')
    
    # Create RD payments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rd_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rd_id INTEGER NOT NULL,
            payment_date TEXT NOT NULL,
            amount REAL NOT NULL,
            month_number INTEGER NOT NULL,
            FOREIGN KEY (rd_id) REFERENCES recurring_deposits (id)
        )
    ''')
    
    # Create Chit Fund table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chit_funds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chit_name TEXT NOT NULL,
            total_value REAL NOT NULL,
            monthly_amount REAL NOT NULL,
            total_months INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            organizer TEXT,
            status TEXT DEFAULT 'Active'
        )
    ''')
    
    # Create Chit payments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chit_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chit_id INTEGER NOT NULL,
            payment_date TEXT NOT NULL,
            amount REAL NOT NULL,
            month_number INTEGER NOT NULL,
            FOREIGN KEY (chit_id) REFERENCES chit_funds (id)
        )
    ''')
    
    # Create Gold Chit table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gold_chits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chit_name TEXT NOT NULL,
            gold_weight REAL NOT NULL,
            monthly_amount REAL NOT NULL,
            total_months INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            jeweller TEXT,
            status TEXT DEFAULT 'Active'
        )
    ''')
    
    # Create Gold Chit payments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gold_chit_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gold_chit_id INTEGER NOT NULL,
            payment_date TEXT NOT NULL,
            amount REAL NOT NULL,
            month_number INTEGER NOT NULL,
            FOREIGN KEY (gold_chit_id) REFERENCES gold_chits (id)
        )
    ''')
    
    # Check if templates exist, if not add defaults
    expense_count = conn.execute('SELECT COUNT(*) as count FROM expense_templates').fetchone()
    if expense_count['count'] == 0:
        # Add default expense templates
        default_expenses = [
            ('Housing', 'Rent', 15000, 'Monthly rent payment', 1),
            ('Housing', 'Home Loan EMI', 25000, 'Home loan monthly installment', 1),
            ('Housing', 'Maintenance', 2000, 'Society maintenance charges', 1),
            ('Utilities', 'Electricity', 2000, 'Monthly electricity bill', 1),
            ('Utilities', 'Water', 500, 'Monthly water bill', 1),
            ('Utilities', 'Internet', 1000, 'Broadband/WiFi', 1),
            ('Utilities', 'Mobile', 500, 'Mobile recharge', 1),
            ('Food', 'Groceries', 8000, 'Monthly grocery shopping', 1),
            ('Food', 'Dining Out', 3000, 'Restaurants and cafes', 0),
            ('Transportation', 'Fuel', 4000, 'Petrol/Diesel', 1),
            ('Transportation', 'Car EMI', 15000, 'Car loan installment', 1),
            ('Healthcare', 'Health Insurance', 5000, 'Monthly premium', 1),
            ('Healthcare', 'Medicines', 1000, 'Regular medicines', 1),
            ('Education', 'School Fees', 10000, 'Monthly school fees', 1),
            ('Education', 'Tuition', 5000, 'Private tuition', 1),
            ('Entertainment', 'OTT Subscriptions', 1000, 'Netflix, Prime, etc.', 1),
            ('Shopping', 'Clothing', 3000, 'Clothes and footwear', 0),
            ('Shopping', 'Personal Care', 1500, 'Grooming products', 1),
            ('Loans & EMI', 'Personal Loan EMI', 10000, 'Personal loan installment', 1),
            ('Loans & EMI', 'Credit Card Bill', 15000, 'Monthly credit card payment', 1),
            ('Insurance', 'Life Insurance', 3000, 'Monthly premium', 1),
            ('Savings & Investment', 'Mutual Funds SIP', 10000, 'Monthly SIP', 1),
            ('Others', 'Miscellaneous', 2000, 'Other expenses', 0)
        ]
        
        cursor.executemany(
            'INSERT INTO expense_templates (category, subcategory, default_amount, description, is_recurring) VALUES (?, ?, ?, ?, ?)',
            default_expenses
        )
    
    income_count = conn.execute('SELECT COUNT(*) as count FROM income_templates').fetchone()
    if income_count['count'] == 0:
        # Add default income templates
        default_income = [
            ('Salary', 'Basic Salary', 50000, 'Monthly basic salary', 1),
            ('Salary', 'HRA', 15000, 'House Rent Allowance', 1),
            ('Salary', 'Bonus', 50000, 'Annual bonus', 0),
            ('Business', 'Business Income', 100000, 'Monthly business revenue', 1),
            ('Freelance', 'Freelance Projects', 30000, 'Project payments', 0),
            ('Investment', 'Dividend Income', 5000, 'Stock dividends', 0),
            ('Investment', 'Interest Income', 3000, 'FD/Savings interest', 1),
            ('Investment', 'Rental Income', 15000, 'Property rent', 1),
            ('Side Income', 'Part-time Job', 10000, 'Additional work', 1),
            ('Others', 'Miscellaneous', 5000, 'Other income', 0)
        ]
        
        cursor.executemany(
            'INSERT INTO income_templates (category, subcategory, default_amount, description, is_recurring) VALUES (?, ?, ?, ?, ?)',
            default_income
        )
    
    # Check if asset templates exist, if not add defaults
    asset_count = conn.execute('SELECT COUNT(*) as count FROM asset_templates').fetchone()
    if asset_count['count'] == 0:
        default_assets = [
            ('Savings Account', 'Primary Savings', 50000, 'Main savings account'),
            ('Savings Account', 'Emergency Fund', 100000, 'Emergency savings'),
            ('Fixed Deposit', 'Bank FD', 200000, 'Fixed deposit investment'),
            ('Fixed Deposit', 'Corporate FD', 150000, 'Corporate fixed deposit'),
            ('Mutual Funds', 'Equity Funds', 300000, 'Equity mutual funds'),
            ('Mutual Funds', 'Debt Funds', 150000, 'Debt mutual funds'),
            ('Mutual Funds', 'ELSS', 150000, 'Tax saving mutual funds'),
            ('Stocks', 'Blue Chip Stocks', 200000, 'Large cap stocks'),
            ('Stocks', 'Mid Cap Stocks', 100000, 'Mid cap stocks'),
            ('Property', 'Residential Property', 5000000, 'Home/apartment value'),
            ('Property', 'Commercial Property', 3000000, 'Commercial property'),
            ('Property', 'Land', 1000000, 'Land investment'),
            ('Gold', 'Physical Gold', 200000, 'Gold jewelry/coins'),
            ('Gold', 'Gold ETF', 100000, 'Gold exchange traded funds'),
            ('Gold', 'Sovereign Gold Bonds', 150000, 'Government gold bonds'),
            ('PPF', 'Public Provident Fund', 150000, 'PPF account balance'),
            ('NPS', 'National Pension System', 200000, 'NPS investment'),
            ('Insurance', 'Life Insurance', 500000, 'Life insurance cash value'),
            ('Insurance', 'ULIP', 300000, 'Unit linked insurance'),
            ('Provident Fund', 'EPF', 500000, 'Employee provident fund'),
            ('Provident Fund', 'VPF', 200000, 'Voluntary provident fund'),
            ('Others', 'Cryptocurrency', 50000, 'Digital currency'),
            ('Others', 'Bonds', 100000, 'Government/corporate bonds')
        ]
        
        cursor.executemany(
            'INSERT INTO asset_templates (category, subcategory, default_amount, description) VALUES (?, ?, ?, ?)',
            default_assets
        )
    
    # Check if liability templates exist, if not add defaults
    liability_count = conn.execute('SELECT COUNT(*) as count FROM liability_templates').fetchone()
    if liability_count['count'] == 0:
        default_liabilities = [
            ('Home Loan', 'Primary Home Loan', 2500000, 'Main home loan EMI'),
            ('Home Loan', 'Plot Loan', 1000000, 'Land purchase loan'),
            ('Car Loan', 'Car Loan', 800000, 'Vehicle loan'),
            ('Car Loan', 'Two Wheeler Loan', 150000, 'Bike/scooter loan'),
            ('Personal Loan', 'Personal Loan', 500000, 'Personal loan'),
            ('Personal Loan', 'Consumer Loan', 200000, 'Consumer durable loan'),
            ('Education Loan', 'Education Loan', 1000000, 'Student loan'),
            ('Education Loan', 'Professional Course', 500000, 'Professional education'),
            ('Credit Card', 'Credit Card Outstanding', 50000, 'Credit card debt'),
            ('Credit Card', 'Credit Card EMI', 25000, 'Credit card installments'),
            ('Business Loan', 'Business Loan', 1500000, 'Business loan'),
            ('Business Loan', 'Working Capital', 500000, 'Working capital loan'),
            ('Gold Loan', 'Gold Loan', 300000, 'Loan against gold'),
            ('Gold Loan', 'Jewelry Loan', 150000, 'Jewelry loan'),
            ('Others', 'Loan from Friends', 100000, 'Personal borrowing'),
            ('Others', 'Advance Salary', 50000, 'Salary advance')
        ]
        
        cursor.executemany(
            'INSERT INTO liability_templates (category, subcategory, default_amount, description) VALUES (?, ?, ?, ?)',
            default_liabilities
        )
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Routes
@app.route('/')
def home():
    return jsonify({
        'message': 'Personal Finance Tracker API',
        'status': 'running',
        'endpoints': [
            '/api/auth/register',
            '/api/auth/login',
            '/api/expenses',
            '/api/assets',
            '/api/liabilities'
        ]
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    
    # Check if user exists
    existing = conn.execute(
        'SELECT id FROM users WHERE username = ? OR email = ?',
        (data['username'], data['email'])
    ).fetchone()
    
    if existing:
        conn.close()
        return jsonify({'error': 'User already exists'}), 400
    
    # Create user
    cursor = conn.execute(
        'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
        (data['username'], data['email'], data['password'])  # In real app, hash the password
    )
    user_id = cursor.lastrowid
    
    user = conn.execute(
        'SELECT id, username, email, created_at FROM users WHERE id = ?',
        (user_id,)
    ).fetchone()
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'access_token': f'simple_token_{user_id}',  # Simple token for demo
        'user': dict(user)
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not all(k in data for k in ['username', 'password']):
        return jsonify({'error': 'Missing username or password'}), 400
    
    conn = get_db_connection()
    user = conn.execute(
        'SELECT id, username, email, created_at FROM users WHERE username = ? AND password = ?',
        (data['username'], data['password'])
    ).fetchone()
    conn.close()
    
    if user:
        return jsonify({
            'access_token': f'simple_token_{user["id"]}',
            'user': dict(user)
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/expenses', methods=['GET', 'POST'])
def expenses():
    if request.method == 'POST':
        data = request.get_json()
        
        if not data or not all(k in data for k in ['category', 'description', 'amount', 'date']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Extract month from date
        month = data['date'][:7]  # YYYY-MM format
        
        conn = get_db_connection()
        cursor = conn.execute(
            'INSERT INTO expenses (user_id, category, description, amount, date, month) VALUES (?, ?, ?, ?, ?, ?)',
            (1, data['category'], data['description'], data['amount'], data['date'], month)  # Using user_id = 1 for demo
        )
        expense_id = cursor.lastrowid
        
        expense = conn.execute(
            'SELECT * FROM expenses WHERE id = ?',
            (expense_id,)
        ).fetchone()
        
        conn.commit()
        conn.close()
        
        return jsonify(dict(expense)), 201
    
    else:  # GET
        conn = get_db_connection()
        expenses = conn.execute(
            'SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC',
            (1,)  # Using user_id = 1 for demo
        ).fetchall()
        conn.close()
        
        return jsonify([dict(expense) for expense in expenses])

@app.route('/api/expenses/month/<string:month>')
def expenses_by_month(month):
    conn = get_db_connection()
    expenses = conn.execute(
        'SELECT * FROM expenses WHERE user_id = ? AND month = ? ORDER BY date DESC',
        (1, month)
    ).fetchall()
    conn.close()
    
    return jsonify([dict(expense) for expense in expenses])

@app.route('/api/expenses/total/<string:month>')
def total_expenses_by_month(month):
    conn = get_db_connection()
    result = conn.execute(
        'SELECT SUM(amount) as total FROM expenses WHERE user_id = ? AND month = ?',
        (1, month)
    ).fetchone()
    conn.close()
    
    total = result['total'] if result['total'] else 0
    return jsonify({'total': total})

@app.route('/api/assets', methods=['GET', 'POST'])
def assets():
    if request.method == 'POST':
        data = request.get_json()
        
        if not data or not all(k in data for k in ['name', 'category', 'value', 'month']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        conn = get_db_connection()
        cursor = conn.execute(
            'INSERT INTO assets (user_id, name, category, value, month) VALUES (?, ?, ?, ?, ?)',
            (1, data['name'], data['category'], data['value'], data['month'])
        )
        asset_id = cursor.lastrowid
        
        asset = conn.execute(
            'SELECT * FROM assets WHERE id = ?',
            (asset_id,)
        ).fetchone()
        
        conn.commit()
        conn.close()
        
        return jsonify(dict(asset)), 201
    
    else:  # GET
        conn = get_db_connection()
        assets = conn.execute(
            'SELECT * FROM assets WHERE user_id = ? ORDER BY created_at DESC',
            (1,)
        ).fetchall()
        conn.close()
        
        return jsonify([dict(asset) for asset in assets])

@app.route('/api/liabilities', methods=['GET', 'POST'])
def liabilities():
    if request.method == 'POST':
        data = request.get_json()
        
        if not data or not all(k in data for k in ['name', 'category', 'amount', 'month']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        conn = get_db_connection()
        cursor = conn.execute(
            'INSERT INTO liabilities (user_id, name, category, amount, month) VALUES (?, ?, ?, ?, ?)',
            (1, data['name'], data['category'], data['amount'], data['month'])
        )
        liability_id = cursor.lastrowid
        
        liability = conn.execute(
            'SELECT * FROM liabilities WHERE id = ?',
            (liability_id,)
        ).fetchone()
        
        conn.commit()
        conn.close()
        
        return jsonify(dict(liability)), 201
    
    else:  # GET
        conn = get_db_connection()
        liabilities = conn.execute(
            'SELECT * FROM liabilities WHERE user_id = ? ORDER BY created_at DESC',
            (1,)
        ).fetchall()
        conn.close()
        
        return jsonify([dict(liability) for liability in liabilities])

@app.route('/api/networth/<string:month>')
def networth(month):
    conn = get_db_connection()
    
    # Get total assets
    assets_result = conn.execute(
        'SELECT SUM(value) as total FROM assets WHERE user_id = ? AND month = ?',
        (1, month)
    ).fetchone()
    total_assets = assets_result['total'] if assets_result['total'] else 0
    
    # Get total liabilities
    liabilities_result = conn.execute(
        'SELECT SUM(amount) as total FROM liabilities WHERE user_id = ? AND month = ?',
        (1, month)
    ).fetchone()
    total_liabilities = liabilities_result['total'] if liabilities_result['total'] else 0
    
    conn.close()
    
    net_worth = total_assets - total_liabilities
    
    return jsonify({
        'month': month,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'net_worth': net_worth
    })

# Admin Routes
@app.route('/api/admin/users')
def admin_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

@app.route('/api/admin/reports')
def admin_reports():
    conn = get_db_connection()
    
    # Get summary statistics
    total_users = conn.execute('SELECT COUNT(*) as count FROM users').fetchone()['count']
    total_expenses = conn.execute('SELECT COUNT(*) as count FROM expenses').fetchone()['count']
    total_assets = conn.execute('SELECT COUNT(*) as count FROM assets').fetchone()['count']
    total_liabilities = conn.execute('SELECT COUNT(*) as count FROM liabilities').fetchone()['count']
    
    # Get monthly data
    monthly_data = conn.execute('''
        SELECT 
            month,
            SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expenses,
            SUM(CASE WHEN type = 'asset' THEN amount ELSE 0 END) as assets,
            SUM(CASE WHEN type = 'liability' THEN amount ELSE 0 END) as liabilities
        FROM (
            SELECT month, amount, 'expense' as type FROM expenses
            UNION ALL
            SELECT month, value as amount, 'asset' as type FROM assets
            UNION ALL
            SELECT month, amount, 'liability' as type FROM liabilities
        ) 
        GROUP BY month ORDER BY month DESC
    ''').fetchall()
    
    conn.close()
    
    return jsonify({
        'summary': {
            'total_users': total_users,
            'total_expenses': total_expenses,
            'total_assets': total_assets,
            'total_liabilities': total_liabilities
        },
        'monthly_data': [dict(row) for row in monthly_data]
    })

@app.route('/api/admin/delete/<string:table>/<int:item_id>', methods=['DELETE'])
def admin_delete(table, item_id):
    if table not in ['expenses', 'assets', 'liabilities', 'users']:
        return jsonify({'error': 'Invalid table'}), 400
    
    conn = get_db_connection()
    conn.execute(f'DELETE FROM {table} WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': f'{table[:-1]} deleted successfully'})

# Admin Edit Routes
@app.route('/api/admin/edit/expense/<int:expense_id>', methods=['PUT'])
def admin_edit_expense(expense_id):
    data = request.get_json()
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE expenses 
        SET category = ?, description = ?, amount = ?, date = ?, month = ?
        WHERE id = ?
    ''', (data['category'], data['description'], data['amount'], 
          data['date'], data['date'][:7], expense_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Expense updated successfully'})

@app.route('/api/admin/edit/asset/<int:asset_id>', methods=['PUT'])
def admin_edit_asset(asset_id):
    data = request.get_json()
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE assets 
        SET name = ?, category = ?, value = ?, month = ?
        WHERE id = ?
    ''', (data['name'], data['category'], data['value'], data['month'], asset_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Asset updated successfully'})

@app.route('/api/admin/edit/liability/<int:liability_id>', methods=['PUT'])
def admin_edit_liability(liability_id):
    data = request.get_json()
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE liabilities 
        SET name = ?, category = ?, amount = ?, month = ?
        WHERE id = ?
    ''', (data['name'], data['category'], data['amount'], data['month'], liability_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Liability updated successfully'})

# Admin Login
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    
    # Simple admin credentials (in production, use proper authentication)
    if data.get('username') == 'admin' and data.get('password') == 'admin123':
        return jsonify({
            'success': True,
            'token': 'admin_token_123',
            'message': 'Admin login successful'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid admin credentials'
        }), 401

# Loan Calculator and Tips
@app.route('/api/loan/calculate', methods=['POST'])
def calculate_loan():
    data = request.get_json()
    
    principal = float(data.get('principal', 0))
    rate = float(data.get('rate', 0)) / 100 / 12  # Monthly rate
    months = int(data.get('months', 0))
    
    if rate == 0:
        monthly_payment = principal / months
        total_payment = principal
        total_interest = 0
    else:
        monthly_payment = principal * (rate * (1 + rate)**months) / ((1 + rate)**months - 1)
        total_payment = monthly_payment * months
        total_interest = total_payment - principal
    
    # Calculate closure tips
    tips = generate_loan_tips(principal, monthly_payment, total_interest, months)
    
    return jsonify({
        'monthly_payment': round(monthly_payment, 2),
        'total_payment': round(total_payment, 2),
        'total_interest': round(total_interest, 2),
        'tips': tips
    })

def generate_loan_tips(principal, monthly_payment, total_interest, months):
    tips = []
    
    # Tip 1: Extra payment impact
    extra_payment = monthly_payment * 0.1  # 10% extra
    if extra_payment > 0:
        tips.append({
            'type': 'extra_payment',
            'title': '💡 Pay 10% Extra Monthly',
            'description': f'Adding ${extra_payment:.2f} extra per month could save you thousands in interest',
            'savings': round(total_interest * 0.15, 2)
        })
    
    # Tip 2: Bi-weekly payments
    biweekly_payment = monthly_payment / 2
    tips.append({
        'type': 'biweekly',
        'title': '📅 Switch to Bi-Weekly Payments',
        'description': f'Pay ${biweekly_payment:.2f} every 2 weeks instead of monthly',
        'savings': round(total_interest * 0.25, 2)
    })
    
    # Tip 3: Refinancing suggestion
    if total_interest > principal * 0.2:
        tips.append({
            'type': 'refinance',
            'title': '🏦 Consider Refinancing',
            'description': 'Your interest is high. Shop for better rates to reduce total cost',
            'potential_savings': round(total_interest * 0.3, 2)
        })
    
    # Tip 4: Lump sum payment
    lump_sum = monthly_payment * 3
    tips.append({
        'type': 'lump_sum',
        'title': '💰 Annual Lump Sum Payment',
        'description': f'Make a ${lump_sum:.2f} payment once a year to reduce principal faster',
        'impact': 'Could reduce loan term by 2-3 years'
    })
    
    return tips

# AI Investment Suggestions
@app.route('/api/ai/investment-suggestions', methods=['GET'])
def ai_investment_suggestions():
    conn = get_db_connection()
    
    # Get current month data
    current_month = datetime.now().strftime('%Y-%m')
    
    # Calculate financial metrics
    assets = conn.execute('SELECT SUM(value) as total FROM assets WHERE month = ?', (current_month,)).fetchone()
    liabilities = conn.execute('SELECT SUM(amount) as total FROM liabilities WHERE month = ?', (current_month,)).fetchone()
    expenses = conn.execute('SELECT SUM(amount) as total FROM expenses WHERE month = ?', (current_month,)).fetchone()
    
    total_assets = assets['total'] if assets['total'] else 0
    total_liabilities = liabilities['total'] if liabilities['total'] else 0
    total_expenses = expenses['total'] if expenses['total'] else 0
    
    net_worth = total_assets - total_liabilities
    monthly_income = total_assets * 0.05  # Estimate 5% monthly income
    
    suggestions = []
    
    # Emergency Fund Suggestion
    emergency_fund_needed = total_expenses * 6
    if total_assets < emergency_fund_needed:
        suggestions.append({
            'type': 'emergency_fund',
            'priority': 'high',
            'title': '🚨 Build Emergency Fund',
            'description': f'You need ₹{emergency_fund_needed:,.2f} for 6 months expenses. Current: ₹{total_assets:,.2f}',
            'action': 'Save in liquid funds or savings account',
            'allocation': min(50, (emergency_fund_needed - total_assets) / monthly_income * 100) if monthly_income > 0 else 50
        })
    
    # Debt Reduction
    if total_liabilities > total_assets * 0.3:
        suggestions.append({
            'type': 'debt_reduction',
            'priority': 'high',
            'title': '💳 Reduce Debt Burden',
            'description': f'Your debt is {(total_liabilities/total_assets*100):.1f}% of assets. Recommended: <30%',
            'action': 'Focus on high-interest debt first',
            'allocation': 30
        })
    
    # Equity Investment (Stocks/Mutual Funds)
    age = 30  # Default age, can be from user profile
    equity_allocation = 100 - age
    if net_worth > emergency_fund_needed:
        suggestions.append({
            'type': 'equity',
            'priority': 'medium',
            'title': '📈 Equity Investment',
            'description': f'Invest {equity_allocation}% in equity for long-term growth',
            'action': 'Index funds, Large-cap mutual funds, Blue-chip stocks',
            'allocation': equity_allocation,
            'recommendations': [
                {'name': 'Nifty 50 Index Fund', 'allocation': 40, 'risk': 'Medium'},
                {'name': 'Large Cap Mutual Funds', 'allocation': 30, 'risk': 'Medium'},
                {'name': 'Mid Cap Funds', 'allocation': 20, 'risk': 'High'},
                {'name': 'Small Cap Funds', 'allocation': 10, 'risk': 'Very High'}
            ]
        })
    
    # Fixed Income (Debt Funds)
    debt_allocation = age
    suggestions.append({
        'type': 'debt',
        'priority': 'low',
        'title': '🏦 Fixed Income Investment',
        'description': f'Invest {debt_allocation}% in debt for stability',
        'action': 'PPF, EPF, Debt Mutual Funds, Fixed Deposits',
        'allocation': debt_allocation,
        'recommendations': [
            {'name': 'PPF (Public Provident Fund)', 'allocation': 40, 'risk': 'Low', 'returns': '7-8%'},
            {'name': 'Debt Mutual Funds', 'allocation': 30, 'risk': 'Low', 'returns': '6-7%'},
            {'name': 'Fixed Deposits', 'allocation': 20, 'risk': 'Very Low', 'returns': '5-6%'},
            {'name': 'Corporate Bonds', 'allocation': 10, 'risk': 'Medium', 'returns': '8-9%'}
        ]
    })
    
    # Gold Investment
    if net_worth > 100000:
        suggestions.append({
            'type': 'gold',
            'priority': 'low',
            'title': '🪙 Gold Investment',
            'description': 'Allocate 5-10% in gold for portfolio diversification',
            'action': 'Gold ETFs, Sovereign Gold Bonds',
            'allocation': 5,
            'recommendations': [
                {'name': 'Sovereign Gold Bonds', 'allocation': 60, 'risk': 'Low'},
                {'name': 'Gold ETFs', 'allocation': 40, 'risk': 'Low'}
            ]
        })
    
    # Tax Saving
    suggestions.append({
        'type': 'tax_saving',
        'priority': 'medium',
        'title': '💰 Tax Saving Investments',
        'description': 'Save up to ₹1.5 lakh under Section 80C',
        'action': 'ELSS, PPF, NPS, Life Insurance',
        'allocation': 10,
        'recommendations': [
            {'name': 'ELSS Mutual Funds', 'allocation': 50, 'risk': 'High', 'returns': '12-15%'},
            {'name': 'NPS (National Pension System)', 'allocation': 30, 'risk': 'Medium', 'returns': '10-12%'},
            {'name': 'PPF', 'allocation': 20, 'risk': 'Low', 'returns': '7-8%'}
        ]
    })
    
    conn.close()
    
    return jsonify({
        'suggestions': suggestions,
        'total_investable': net_worth - emergency_fund_needed if net_worth > emergency_fund_needed else 0,
        'risk_profile': 'Moderate' if equity_allocation > 50 else 'Conservative'
    })

# Monthly Report with Predictions
@app.route('/api/ai/monthly-report', methods=['GET'])
def ai_monthly_report():
    conn = get_db_connection()
    
    # Get last 6 months data
    reports = []
    predictions = []
    
    for i in range(6, -1, -1):
        date = datetime.now() - timedelta(days=30*i)
        month = date.strftime('%Y-%m')
        
        expenses = conn.execute('SELECT SUM(amount) as total FROM expenses WHERE month = ?', (month,)).fetchone()
        assets = conn.execute('SELECT SUM(value) as total FROM assets WHERE month = ?', (month,)).fetchone()
        liabilities = conn.execute('SELECT SUM(amount) as total FROM liabilities WHERE month = ?', (month,)).fetchone()
        
        total_expenses = expenses['total'] if expenses['total'] else 0
        total_assets = assets['total'] if assets['total'] else 0
        total_liabilities = liabilities['total'] if liabilities['total'] else 0
        
        reports.append({
            'month': month,
            'expenses': total_expenses,
            'assets': total_assets,
            'liabilities': total_liabilities,
            'net_worth': total_assets - total_liabilities,
            'savings_rate': ((total_assets - total_expenses) / total_assets * 100) if total_assets > 0 else 0
        })
    
    # AI Predictions for next 3 months
    if len(reports) >= 3:
        # Simple linear regression for prediction
        avg_expense_growth = sum([(reports[i]['expenses'] - reports[i-1]['expenses']) for i in range(1, len(reports))]) / (len(reports) - 1)
        avg_asset_growth = sum([(reports[i]['assets'] - reports[i-1]['assets']) for i in range(1, len(reports))]) / (len(reports) - 1)
        
        last_report = reports[-1]
        
        for i in range(1, 4):
            future_date = datetime.now() + timedelta(days=30*i)
            future_month = future_date.strftime('%Y-%m')
            
            predicted_expenses = last_report['expenses'] + (avg_expense_growth * i)
            predicted_assets = last_report['assets'] + (avg_asset_growth * i)
            predicted_liabilities = last_report['liabilities']  # Assume constant
            
            predictions.append({
                'month': future_month,
                'predicted_expenses': max(0, predicted_expenses),
                'predicted_assets': max(0, predicted_assets),
                'predicted_liabilities': predicted_liabilities,
                'predicted_net_worth': max(0, predicted_assets) - predicted_liabilities,
                'confidence': 85 - (i * 10)  # Confidence decreases with time
            })
    
    # Generate insights
    insights = []
    
    if len(reports) >= 2:
        expense_trend = reports[-1]['expenses'] - reports[-2]['expenses']
        if expense_trend > 0:
            insights.append({
                'type': 'warning',
                'message': f'📊 Expenses increased by ₹{expense_trend:,.2f} this month'
            })
        else:
            insights.append({
                'type': 'success',
                'message': f'✅ Expenses decreased by ₹{abs(expense_trend):,.2f} this month'
            })
        
        net_worth_trend = reports[-1]['net_worth'] - reports[-2]['net_worth']
        if net_worth_trend > 0:
            insights.append({
                'type': 'success',
                'message': f'💰 Net worth increased by ₹{net_worth_trend:,.2f}'
            })
    
    conn.close()
    
    return jsonify({
        'historical': reports,
        'predictions': predictions,
        'insights': insights,
        'summary': {
            'avg_monthly_expenses': sum([r['expenses'] for r in reports]) / len(reports) if reports else 0,
            'avg_savings_rate': sum([r['savings_rate'] for r in reports]) / len(reports) if reports else 0,
            'total_growth': reports[-1]['net_worth'] - reports[0]['net_worth'] if len(reports) >= 2 else 0
        }
    })

# Seasonal Stock Suggestions
@app.route('/api/ai/seasonal-stocks', methods=['GET'])
def seasonal_stocks():
    current_month = datetime.now().month
    
    # Indian seasonal stock recommendations
    seasonal_recommendations = {
        1: {  # January
            'season': 'New Year & Winter',
            'sectors': ['Textile', 'Retail', 'FMCG'],
            'stocks': [
                {'name': 'Raymond Ltd', 'sector': 'Textile', 'reason': 'Winter clothing demand', 'risk': 'Medium'},
                {'name': 'Titan Company', 'sector': 'Retail', 'reason': 'New Year gifting season', 'risk': 'Low'},
                {'name': 'ITC Ltd', 'sector': 'FMCG', 'reason': 'Stable consumer demand', 'risk': 'Low'}
            ]
        },
        2: {  # February
            'season': 'Pre-Budget & Valentine',
            'sectors': ['Banking', 'Infrastructure', 'Retail'],
            'stocks': [
                {'name': 'HDFC Bank', 'sector': 'Banking', 'reason': 'Budget expectations', 'risk': 'Low'},
                {'name': 'L&T', 'sector': 'Infrastructure', 'reason': 'Budget infrastructure push', 'risk': 'Medium'},
                {'name': 'Jubilant Foodworks', 'sector': 'Retail', 'reason': 'Valentine celebrations', 'risk': 'Medium'}
            ]
        },
        3: {  # March
            'season': 'Year-End & Holi',
            'sectors': ['Auto', 'FMCG', 'Pharma'],
            'stocks': [
                {'name': 'Maruti Suzuki', 'sector': 'Auto', 'reason': 'Year-end discounts', 'risk': 'Medium'},
                {'name': 'Asian Paints', 'sector': 'FMCG', 'reason': 'Holi painting demand', 'risk': 'Low'},
                {'name': 'Sun Pharma', 'sector': 'Pharma', 'reason': 'Seasonal health needs', 'risk': 'Low'}
            ]
        },
        4: {  # April
            'season': 'New Financial Year',
            'sectors': ['IT', 'Banking', 'Mutual Funds'],
            'stocks': [
                {'name': 'TCS', 'sector': 'IT', 'reason': 'New contracts & projects', 'risk': 'Low'},
                {'name': 'ICICI Bank', 'sector': 'Banking', 'reason': 'New FY lending', 'risk': 'Low'},
                {'name': 'HDFC AMC', 'sector': 'Mutual Funds', 'reason': 'Investment season', 'risk': 'Medium'}
            ]
        },
        5: {  # May
            'season': 'Summer & AC Demand',
            'sectors': ['Power', 'Consumer Durables', 'Beverages'],
            'stocks': [
                {'name': 'Voltas', 'sector': 'Consumer Durables', 'reason': 'AC & cooler demand', 'risk': 'Medium'},
                {'name': 'NTPC', 'sector': 'Power', 'reason': 'High electricity demand', 'risk': 'Low'},
                {'name': 'Coca-Cola India', 'sector': 'Beverages', 'reason': 'Summer beverage sales', 'risk': 'Low'}
            ]
        },
        6: {  # June
            'season': 'Monsoon Preparation',
            'sectors': ['Agro', 'Cement', 'Pharma'],
            'stocks': [
                {'name': 'UPL Ltd', 'sector': 'Agro', 'reason': 'Monsoon crop season', 'risk': 'High'},
                {'name': 'UltraTech Cement', 'sector': 'Cement', 'reason': 'Construction activity', 'risk': 'Medium'},
                {'name': 'Dr Reddy\'s', 'sector': 'Pharma', 'reason': 'Monsoon health issues', 'risk': 'Low'}
            ]
        },
        7: {  # July
            'season': 'Monsoon & Budget',
            'sectors': ['Agro', 'FMCG', 'Infrastructure'],
            'stocks': [
                {'name': 'Tata Consumer', 'sector': 'FMCG', 'reason': 'Stable demand', 'risk': 'Low'},
                {'name': 'Jain Irrigation', 'sector': 'Agro', 'reason': 'Irrigation demand', 'risk': 'High'},
                {'name': 'Adani Ports', 'sector': 'Infrastructure', 'reason': 'Trade growth', 'risk': 'Medium'}
            ]
        },
        8: {  # August
            'season': 'Independence Day & Festive Prep',
            'sectors': ['Retail', 'E-commerce', 'FMCG'],
            'stocks': [
                {'name': 'Reliance Retail', 'sector': 'Retail', 'reason': 'Festive shopping begins', 'risk': 'Low'},
                {'name': 'Nykaa', 'sector': 'E-commerce', 'reason': 'Online shopping surge', 'risk': 'High'},
                {'name': 'Britannia', 'sector': 'FMCG', 'reason': 'Festive food demand', 'risk': 'Low'}
            ]
        },
        9: {  # September
            'season': 'Festive Season Start',
            'sectors': ['Auto', 'Retail', 'Gold'],
            'stocks': [
                {'name': 'Hero MotoCorp', 'sector': 'Auto', 'reason': 'Festive vehicle sales', 'risk': 'Medium'},
                {'name': 'Shoppers Stop', 'sector': 'Retail', 'reason': 'Festive shopping', 'risk': 'Medium'},
                {'name': 'Titan Gold', 'sector': 'Gold', 'reason': 'Dhanteras preparation', 'risk': 'Low'}
            ]
        },
        10: {  # October
            'season': 'Diwali & Peak Festive',
            'sectors': ['Auto', 'Retail', 'Electronics'],
            'stocks': [
                {'name': 'Bajaj Auto', 'sector': 'Auto', 'reason': 'Peak vehicle buying', 'risk': 'Medium'},
                {'name': 'DMart', 'sector': 'Retail', 'reason': 'Diwali shopping', 'risk': 'Low'},
                {'name': 'Dixon Technologies', 'sector': 'Electronics', 'reason': 'Electronics demand', 'risk': 'High'}
            ]
        },
        11: {  # November
            'season': 'Post-Diwali & Wedding Season',
            'sectors': ['Jewelry', 'Hospitality', 'Real Estate'],
            'stocks': [
                {'name': 'Kalyan Jewellers', 'sector': 'Jewelry', 'reason': 'Wedding season', 'risk': 'Medium'},
                {'name': 'Indian Hotels', 'sector': 'Hospitality', 'reason': 'Wedding & travel', 'risk': 'Medium'},
                {'name': 'DLF Ltd', 'sector': 'Real Estate', 'reason': 'Property buying season', 'risk': 'High'}
            ]
        },
        12: {  # December
            'season': 'Year-End & Christmas',
            'sectors': ['Tourism', 'Retail', 'Banking'],
            'stocks': [
                {'name': 'Thomas Cook', 'sector': 'Tourism', 'reason': 'Holiday travel', 'risk': 'Medium'},
                {'name': 'Avenue Supermarts', 'sector': 'Retail', 'reason': 'Year-end shopping', 'risk': 'Low'},
                {'name': 'Kotak Mahindra', 'sector': 'Banking', 'reason': 'Year-end investments', 'risk': 'Low'}
            ]
        }
    }
    
    current_recommendations = seasonal_recommendations.get(current_month, seasonal_recommendations[1])
    
    return jsonify({
        'current_month': datetime.now().strftime('%B'),
        'season': current_recommendations['season'],
        'recommended_sectors': current_recommendations['sectors'],
        'stocks': current_recommendations['stocks'],
        'general_advice': [
            'Diversify across sectors',
            'Invest for long-term (3-5 years)',
            'Review portfolio quarterly',
            'Keep 20% in liquid funds',
            'Avoid timing the market'
        ]
    })

# Quick Loan Closure Strategies
@app.route('/api/ai/quick-loan-closure', methods=['POST'])
def quick_loan_closure():
    data = request.get_json()
    
    loan_amount = float(data.get('loan_amount', 0))
    interest_rate = float(data.get('interest_rate', 0))
    remaining_months = int(data.get('remaining_months', 0))
    monthly_income = float(data.get('monthly_income', 0))
    
    # Calculate current EMI
    rate = interest_rate / 100 / 12
    if rate > 0:
        current_emi = loan_amount * (rate * (1 + rate)**remaining_months) / ((1 + rate)**remaining_months - 1)
    else:
        current_emi = loan_amount / remaining_months
    
    strategies = []
    
    # Strategy 1: Increase EMI by 20%
    increased_emi = current_emi * 1.2
    if increased_emi < monthly_income * 0.4:  # Affordable
        new_months = loan_amount / increased_emi if rate == 0 else int((loan_amount * rate) / (increased_emi - loan_amount * rate))
        time_saved = remaining_months - new_months
        interest_saved = (current_emi * remaining_months - loan_amount) - (increased_emi * new_months - loan_amount)
        
        strategies.append({
            'strategy': '💪 Increase EMI by 20%',
            'new_emi': round(increased_emi, 2),
            'new_tenure': max(1, new_months),
            'time_saved_months': max(0, time_saved),
            'interest_saved': max(0, round(interest_saved, 2)),
            'feasibility': 'High' if increased_emi < monthly_income * 0.3 else 'Medium',
            'priority': 1
        })
    
    # Strategy 2: Make lump sum payment
    lump_sum = monthly_income * 2  # 2 months salary
    remaining_after_lumpsum = loan_amount - lump_sum
    if remaining_after_lumpsum > 0:
        new_months_lumpsum = int(remaining_after_lumpsum / current_emi)
        time_saved_lumpsum = remaining_months - new_months_lumpsum
        interest_saved_lumpsum = (current_emi * remaining_months - loan_amount) - (current_emi * new_months_lumpsum - remaining_after_lumpsum)
        
        strategies.append({
            'strategy': '💰 Make Lump Sum Payment',
            'lump_sum_amount': round(lump_sum, 2),
            'new_tenure': max(1, new_months_lumpsum),
            'time_saved_months': max(0, time_saved_lumpsum),
            'interest_saved': max(0, round(interest_saved_lumpsum, 2)),
            'feasibility': 'Medium',
            'priority': 2
        })
    
    # Strategy 3: Balance Transfer
    new_rate = interest_rate * 0.8  # 20% lower rate
    new_rate_monthly = new_rate / 100 / 12
    if new_rate_monthly > 0:
        new_emi = loan_amount * (new_rate_monthly * (1 + new_rate_monthly)**remaining_months) / ((1 + new_rate_monthly)**remaining_months - 1)
    else:
        new_emi = loan_amount / remaining_months
    
    interest_saved_transfer = (current_emi * remaining_months) - (new_emi * remaining_months)
    
    strategies.append({
        'strategy': '🏦 Balance Transfer to Lower Rate',
        'new_rate': round(new_rate, 2),
        'new_emi': round(new_emi, 2),
        'same_tenure': remaining_months,
        'interest_saved': round(interest_saved_transfer, 2),
        'feasibility': 'High',
        'priority': 3
    })
    
    # Strategy 4: Bi-weekly payments
    biweekly_payment = current_emi / 2
    annual_extra_payment = biweekly_payment * 2  # 2 extra payments per year
    new_months_biweekly = remaining_months - 6  # Approximate 6 months saved
    interest_saved_biweekly = current_emi * 6
    
    strategies.append({
        'strategy': '📅 Switch to Bi-Weekly Payments',
        'biweekly_amount': round(biweekly_payment, 2),
        'extra_annual_payment': round(annual_extra_payment, 2),
        'time_saved_months': 6,
        'interest_saved': round(interest_saved_biweekly, 2),
        'feasibility': 'High',
        'priority': 4
    })
    
    # Strategy 5: Use bonus/windfall
    strategies.append({
        'strategy': '🎁 Use Annual Bonus/Windfall',
        'recommendation': 'Use 50% of bonus towards loan',
        'suggested_amount': round(monthly_income * 2, 2),
        'impact': 'Can reduce tenure by 3-6 months',
        'feasibility': 'Medium',
        'priority': 5
    })
    
    # Best strategy recommendation
    best_strategy = min(strategies[:3], key=lambda x: x.get('new_tenure', remaining_months) if 'new_tenure' in x else remaining_months)
    
    return jsonify({
        'current_situation': {
            'loan_amount': loan_amount,
            'current_emi': round(current_emi, 2),
            'remaining_months': remaining_months,
            'total_interest': round(current_emi * remaining_months - loan_amount, 2)
        },
        'strategies': strategies,
        'best_strategy': best_strategy,
        'quick_tips': [
            'Pay more than minimum EMI whenever possible',
            'Use tax refunds for loan prepayment',
            'Avoid taking new loans until current is cleared',
            'Set up auto-debit to avoid late fees',
            'Review loan annually for better rates'
        ]
    })

# Financial Reports API
@app.route('/api/reports/yearly', methods=['GET'])
def yearly_report():
    conn = get_db_connection()
    year = request.args.get('year', datetime.now().year)
    
    # Get all months in the year
    monthly_data = []
    for month in range(1, 13):
        month_str = f"{year}-{str(month).zfill(2)}"
        
        expenses = conn.execute('SELECT SUM(amount) as total FROM expenses WHERE month = ?', (month_str,)).fetchone()
        assets = conn.execute('SELECT SUM(value) as total FROM assets WHERE month = ?', (month_str,)).fetchone()
        liabilities = conn.execute('SELECT SUM(amount) as total FROM liabilities WHERE month = ?', (month_str,)).fetchone()
        
        monthly_data.append({
            'month': month_str,
            'month_name': datetime(int(year), month, 1).strftime('%B'),
            'expenses': expenses['total'] if expenses['total'] else 0,
            'assets': assets['total'] if assets['total'] else 0,
            'liabilities': liabilities['total'] if liabilities['total'] else 0,
            'net_worth': (assets['total'] if assets['total'] else 0) - (liabilities['total'] if liabilities['total'] else 0)
        })
    
    total_expenses = sum([m['expenses'] for m in monthly_data])
    total_assets = monthly_data[-1]['assets'] if monthly_data else 0
    total_liabilities = monthly_data[-1]['liabilities'] if monthly_data else 0
    
    conn.close()
    
    return jsonify({
        'year': year,
        'monthly_data': monthly_data,
        'summary': {
            'total_expenses': total_expenses,
            'final_assets': total_assets,
            'final_liabilities': total_liabilities,
            'final_net_worth': total_assets - total_liabilities,
            'avg_monthly_expenses': total_expenses / 12
        }
    })

@app.route('/api/reports/monthly', methods=['GET'])
def monthly_report():
    conn = get_db_connection()
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    
    # Get expenses by category
    expenses_by_category = conn.execute(
        'SELECT category, SUM(amount) as total FROM expenses WHERE month = ? GROUP BY category',
        (month,)
    ).fetchall()
    
    # Get all expenses
    all_expenses = conn.execute(
        'SELECT * FROM expenses WHERE month = ? ORDER BY date DESC',
        (month,)
    ).fetchall()
    
    # Get assets
    assets = conn.execute('SELECT * FROM assets WHERE month = ?', (month,)).fetchall()
    
    # Get liabilities
    liabilities = conn.execute('SELECT * FROM liabilities WHERE month = ?', (month,)).fetchall()
    
    total_expenses = sum([e['total'] for e in expenses_by_category])
    total_assets = sum([a['value'] for a in assets])
    total_liabilities = sum([l['amount'] for l in liabilities])
    
    conn.close()
    
    return jsonify({
        'month': month,
        'expenses_by_category': [dict(e) for e in expenses_by_category],
        'all_expenses': [dict(e) for e in all_expenses],
        'assets': [dict(a) for a in assets],
        'liabilities': [dict(l) for l in liabilities],
        'summary': {
            'total_expenses': total_expenses,
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'net_worth': total_assets - total_liabilities,
            'expense_count': len(all_expenses),
            'asset_count': len(assets),
            'liability_count': len(liabilities)
        }
    })

@app.route('/api/reports/weekly', methods=['GET'])
def weekly_report():
    conn = get_db_connection()
    
    # Get date parameter or use current week
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    target_date = datetime.strptime(date_str, '%Y-%m-%d')
    
    # Calculate week start (Monday) and end (Sunday)
    week_start = target_date - timedelta(days=target_date.weekday())
    week_end = week_start + timedelta(days=6)
    
    # Get expenses for the week
    expenses = conn.execute(
        'SELECT * FROM expenses WHERE date >= ? AND date <= ? ORDER BY date',
        (week_start.strftime('%Y-%m-%d'), week_end.strftime('%Y-%m-%d'))
    ).fetchall()
    
    # Group by day
    daily_data = {}
    for i in range(7):
        day = week_start + timedelta(days=i)
        day_str = day.strftime('%Y-%m-%d')
        daily_data[day_str] = {
            'date': day_str,
            'day_name': day.strftime('%A'),
            'expenses': [],
            'total': 0
        }
    
    for expense in expenses:
        if expense['date'] in daily_data:
            daily_data[expense['date']]['expenses'].append(dict(expense))
            daily_data[expense['date']]['total'] += expense['amount']
    
    daily_list = list(daily_data.values())
    total_week_expenses = sum([d['total'] for d in daily_list])
    
    conn.close()
    
    return jsonify({
        'week_start': week_start.strftime('%Y-%m-%d'),
        'week_end': week_end.strftime('%Y-%m-%d'),
        'daily_data': daily_list,
        'summary': {
            'total_expenses': total_week_expenses,
            'avg_daily_expenses': total_week_expenses / 7,
            'expense_count': len(expenses),
            'highest_day': max(daily_list, key=lambda x: x['total'])['day_name'] if daily_list else 'N/A',
            'highest_amount': max([d['total'] for d in daily_list]) if daily_list else 0
        }
    })

# AI Stock Analysis with P/E Ratio
@app.route('/api/ai/stock-analysis', methods=['GET'])
def stock_analysis():
    # Top 20 Indian stocks under ₹1000 with comprehensive analysis (Updated prices as of Oct 2025)
    stocks = [
        {
            'name': 'Tata Motors',
            'symbol': 'TATAMOTORS',
            'current_price': 920,
            'pe_ratio': 10.2,
            'market_cap': 338000,
            'sector': 'Automobile',
            'dividend_yield': 0.5,
            'debt_to_equity': 0.38,
            'roe': 22.5,
            'revenue_growth': 18.2,
            'profit_margin': 7.8,
            'recommendation': 'Buy',
            'target_price': 1100,
            'risk': 'Medium',
            'reasons': ['Strong EV portfolio', 'JLR profitability improved', 'Growing domestic demand', 'Debt reduction'],
            'concerns': ['Commodity price volatility', 'Global slowdown risk', 'Competition in EV space']
        },
        {
            'name': 'State Bank of India',
            'symbol': 'SBIN',
            'current_price': 785,
            'pe_ratio': 9.5,
            'market_cap': 700000,
            'sector': 'Banking',
            'dividend_yield': 1.8,
            'debt_to_equity': 0.0,
            'roe': 18.5,
            'revenue_growth': 15.5,
            'profit_margin': 24.3,
            'recommendation': 'Strong Buy',
            'target_price': 950,
            'risk': 'Low',
            'reasons': ['Largest PSU bank', 'Improving asset quality', 'Strong deposit growth', 'Digital transformation'],
            'concerns': ['Government ownership', 'NPA concerns']
        },
        {
            'name': 'Tata Steel',
            'symbol': 'TATASTEEL',
            'current_price': 148,
            'pe_ratio': 38.5,
            'market_cap': 185000,
            'sector': 'Steel',
            'dividend_yield': 2.8,
            'debt_to_equity': 0.48,
            'roe': 9.5,
            'revenue_growth': 6.5,
            'profit_margin': 5.2,
            'recommendation': 'Hold',
            'target_price': 165,
            'risk': 'High',
            'reasons': ['Integrated steel player', 'Global presence', 'Infrastructure demand', 'Debt reduction progress'],
            'concerns': ['High P/E ratio', 'Commodity cycle risk', 'China slowdown', 'Steel price volatility']
        },
        {
            'name': 'Power Grid Corporation',
            'symbol': 'POWERGRID',
            'current_price': 315,
            'pe_ratio': 13.8,
            'market_cap': 295000,
            'sector': 'Power',
            'dividend_yield': 3.2,
            'debt_to_equity': 1.75,
            'roe': 15.5,
            'revenue_growth': 11.2,
            'profit_margin': 19.5,
            'recommendation': 'Buy',
            'target_price': 370,
            'risk': 'Low',
            'reasons': ['Monopoly in transmission', 'Stable cash flows', 'Good dividend yield', 'Capex opportunities'],
            'concerns': ['Regulatory risks', 'High debt levels']
        },
        {
            'name': 'NTPC',
            'symbol': 'NTPC',
            'current_price': 365,
            'pe_ratio': 10.8,
            'market_cap': 355000,
            'sector': 'Power',
            'dividend_yield': 3.5,
            'debt_to_equity': 1.15,
            'roe': 14.8,
            'revenue_growth': 10.5,
            'profit_margin': 16.2,
            'recommendation': 'Buy',
            'target_price': 430,
            'risk': 'Low',
            'reasons': ['Largest power generator', 'Green energy push', 'Consistent dividends', 'Strong fundamentals'],
            'concerns': ['Coal dependency', 'Regulatory changes']
        },
        {
            'name': 'Tata Power',
            'symbol': 'TATAPOWER',
            'current_price': 425,
            'pe_ratio': 20.5,
            'market_cap': 136000,
            'sector': 'Power',
            'dividend_yield': 1.0,
            'debt_to_equity': 1.35,
            'roe': 13.5,
            'revenue_growth': 20.5,
            'profit_margin': 9.5,
            'recommendation': 'Buy',
            'target_price': 510,
            'risk': 'Medium',
            'reasons': ['Renewable energy focus', 'EV charging network', 'Diversified portfolio', 'Growth momentum'],
            'concerns': ['High debt', 'Execution risk', 'Valuation premium']
        },
        {
            'name': 'Vedanta',
            'symbol': 'VEDL',
            'current_price': 465,
            'pe_ratio': 7.8,
            'market_cap': 173000,
            'sector': 'Mining',
            'dividend_yield': 4.2,
            'debt_to_equity': 0.32,
            'roe': 24.5,
            'revenue_growth': 14.8,
            'profit_margin': 19.5,
            'recommendation': 'Strong Buy',
            'target_price': 575,
            'risk': 'Medium',
            'reasons': ['Low P/E ratio', 'High dividend yield', 'Commodity supercycle', 'Debt reduction'],
            'concerns': ['Commodity price volatility', 'Environmental concerns', 'Regulatory issues']
        },
        {
            'name': 'Coal India',
            'symbol': 'COALINDIA',
            'current_price': 485,
            'pe_ratio': 6.8,
            'market_cap': 299000,
            'sector': 'Mining',
            'dividend_yield': 4.8,
            'debt_to_equity': 0.03,
            'roe': 38.5,
            'revenue_growth': 9.5,
            'profit_margin': 29.5,
            'recommendation': 'Buy',
            'target_price': 570,
            'risk': 'Low',
            'reasons': ['Monopoly in coal', 'Very high ROE', 'Excellent dividend yield', 'Zero debt'],
            'concerns': ['ESG concerns', 'Renewable energy shift', 'Government control']
        },
        {
            'name': 'Indian Oil Corporation',
            'symbol': 'IOC',
            'current_price': 165,
            'pe_ratio': 9.8,
            'market_cap': 233000,
            'sector': 'Oil & Gas',
            'dividend_yield': 4.5,
            'debt_to_equity': 1.08,
            'roe': 13.5,
            'revenue_growth': 16.5,
            'profit_margin': 4.2,
            'recommendation': 'Buy',
            'target_price': 195,
            'risk': 'Medium',
            'reasons': ['Largest refiner', 'Strong retail network', 'Good dividend', 'Refining margins improving'],
            'concerns': ['Crude price volatility', 'Subsidy burden', 'Competition']
        },
        {
            'name': 'ONGC',
            'symbol': 'ONGC',
            'current_price': 285,
            'pe_ratio': 6.2,
            'market_cap': 359000,
            'sector': 'Oil & Gas',
            'dividend_yield': 6.2,
            'debt_to_equity': 0.22,
            'roe': 19.5,
            'revenue_growth': 24.5,
            'profit_margin': 27.8,
            'recommendation': 'Strong Buy',
            'target_price': 360,
            'risk': 'Low',
            'reasons': ['Very low P/E', 'Highest dividend yield', 'Strong cash flows', 'Exploration success'],
            'concerns': ['Government control', 'Crude price dependency', 'Dividend payout policy']
        },
        {
            'name': 'Bharat Electronics',
            'symbol': 'BEL',
            'current_price': 295,
            'pe_ratio': 26.5,
            'market_cap': 216000,
            'sector': 'Defense',
            'dividend_yield': 2.0,
            'debt_to_equity': 0.0,
            'roe': 24.5,
            'revenue_growth': 20.5,
            'profit_margin': 23.5,
            'recommendation': 'Buy',
            'target_price': 360,
            'risk': 'Medium',
            'reasons': ['Defense modernization', 'Export potential', 'Zero debt', 'Strong order book'],
            'concerns': ['High P/E', 'Government dependent', 'Execution delays']
        },
        {
            'name': 'Ashok Leyland',
            'symbol': 'ASHOKLEY',
            'current_price': 215,
            'pe_ratio': 16.5,
            'market_cap': 63000,
            'sector': 'Automobile',
            'dividend_yield': 1.0,
            'debt_to_equity': 0.12,
            'roe': 17.5,
            'revenue_growth': 24.5,
            'profit_margin': 7.5,
            'recommendation': 'Buy',
            'target_price': 270,
            'risk': 'Medium',
            'reasons': ['CV cycle upturn', 'Defense orders', 'EV foray', 'Market share gains'],
            'concerns': ['Competition', 'Economic slowdown', 'Margin pressure']
        },
        {
            'name': 'Jindal Steel & Power',
            'symbol': 'JINDALSTEL',
            'current_price': 925,
            'pe_ratio': 14.2,
            'market_cap': 93000,
            'sector': 'Steel',
            'dividend_yield': 1.6,
            'debt_to_equity': 0.38,
            'roe': 19.5,
            'revenue_growth': 13.5,
            'profit_margin': 16.5,
            'recommendation': 'Buy',
            'target_price': 1100,
            'risk': 'Medium',
            'reasons': ['Integrated operations', 'Capacity expansion', 'Debt reduction', 'Strong fundamentals'],
            'concerns': ['Commodity cycle', 'Competition', 'Valuation near ₹1000']
        },
        {
            'name': 'Adani Power',
            'symbol': 'ADANIPOWER',
            'current_price': 575,
            'pe_ratio': 11.5,
            'market_cap': 224000,
            'sector': 'Power',
            'dividend_yield': 0.4,
            'debt_to_equity': 2.65,
            'roe': 24.5,
            'revenue_growth': 30.5,
            'profit_margin': 19.5,
            'recommendation': 'Hold',
            'target_price': 640,
            'risk': 'High',
            'reasons': ['Capacity addition', 'Power demand growth', 'Improved operations', 'Strong cash flows'],
            'concerns': ['Very high debt', 'Regulatory risks', 'Group concerns', 'Governance issues']
        },
        {
            'name': 'Suzlon Energy',
            'symbol': 'SUZLON',
            'current_price': 68,
            'pe_ratio': 72.5,
            'market_cap': 92000,
            'sector': 'Renewable Energy',
            'dividend_yield': 0.0,
            'debt_to_equity': 0.75,
            'roe': 9.5,
            'revenue_growth': 48.5,
            'profit_margin': 3.5,
            'recommendation': 'Speculative Buy',
            'target_price': 85,
            'risk': 'Very High',
            'reasons': ['Wind energy boom', 'Order book growth', 'Turnaround story', 'Debt reduction'],
            'concerns': ['Very high P/E', 'Execution risk', 'Past track record', 'Profitability concerns']
        },
        {
            'name': 'Vodafone Idea',
            'symbol': 'IDEA',
            'current_price': 14,
            'pe_ratio': -1,
            'market_cap': 99000,
            'sector': 'Telecom',
            'dividend_yield': 0.0,
            'debt_to_equity': 14.5,
            'roe': -42.5,
            'revenue_growth': -6.5,
            'profit_margin': -23.5,
            'recommendation': 'Avoid',
            'target_price': 12,
            'risk': 'Very High',
            'reasons': ['Turnaround potential', 'Government support', 'Tariff hikes possible'],
            'concerns': ['Massive debt', 'Negative earnings', 'Subscriber loss', 'Dilution risk', 'Survival concerns']
        },
        {
            'name': 'Bank of Baroda',
            'symbol': 'BANKBARODA',
            'current_price': 245,
            'pe_ratio': 6.2,
            'market_cap': 127000,
            'sector': 'Banking',
            'dividend_yield': 2.3,
            'debt_to_equity': 0.0,
            'roe': 16.5,
            'revenue_growth': 15.5,
            'profit_margin': 29.5,
            'recommendation': 'Strong Buy',
            'target_price': 315,
            'risk': 'Low',
            'reasons': ['Very low P/E', 'Asset quality improvement', 'Strong capital position', 'Digital push'],
            'concerns': ['PSU bank challenges', 'NPA risks', 'Government control']
        },
        {
            'name': 'Punjab National Bank',
            'symbol': 'PNB',
            'current_price': 108,
            'pe_ratio': 7.8,
            'market_cap': 121000,
            'sector': 'Banking',
            'dividend_yield': 1.7,
            'debt_to_equity': 0.0,
            'roe': 13.5,
            'revenue_growth': 12.5,
            'profit_margin': 23.5,
            'recommendation': 'Buy',
            'target_price': 140,
            'risk': 'Medium',
            'reasons': ['Low P/E', 'Turnaround story', 'Branch network', 'Improving asset quality'],
            'concerns': ['Past NPA issues', 'Governance concerns', 'Competition']
        },
        {
            'name': 'Canara Bank',
            'symbol': 'CANBK',
            'current_price': 105,
            'pe_ratio': 5.8,
            'market_cap': 94000,
            'sector': 'Banking',
            'dividend_yield': 2.8,
            'debt_to_equity': 0.0,
            'roe': 14.5,
            'revenue_growth': 13.5,
            'profit_margin': 26.5,
            'recommendation': 'Strong Buy',
            'target_price': 135,
            'risk': 'Low',
            'reasons': ['Lowest P/E in sector', 'High dividend yield', 'Strong fundamentals', 'Asset quality improving'],
            'concerns': ['PSU bank risks', 'Government ownership', 'Slower growth']
        },
        {
            'name': 'Union Bank of India',
            'symbol': 'UNIONBANK',
            'current_price': 125,
            'pe_ratio': 7.2,
            'market_cap': 94000,
            'sector': 'Banking',
            'dividend_yield': 2.0,
            'debt_to_equity': 0.0,
            'roe': 12.8,
            'revenue_growth': 11.8,
            'profit_margin': 24.8,
            'recommendation': 'Buy',
            'target_price': 160,
            'risk': 'Medium',
            'reasons': ['Low P/E', 'Merger synergies', 'Branch network', 'Capital adequacy'],
            'concerns': ['Integration challenges', 'NPA legacy', 'Competition']
        }
    ]
    
    # Analyze and categorize
    strong_buy = [s for s in stocks if s['recommendation'] == 'Strong Buy']
    buy = [s for s in stocks if s['recommendation'] == 'Buy']
    hold = [s for s in stocks if s['recommendation'] == 'Hold']
    speculative = [s for s in stocks if s['recommendation'] == 'Speculative Buy']
    avoid = [s for s in stocks if s['recommendation'] == 'Avoid']
    
    # Filter stocks under ₹1000
    under_1000 = [s for s in stocks if s['current_price'] < 1000]
    
    # Best P/E ratios (excluding negative)
    best_pe = sorted([s for s in under_1000 if s['pe_ratio'] > 0], key=lambda x: x['pe_ratio'])[:5]
    
    # Best dividend yields
    best_dividend = sorted(under_1000, key=lambda x: x['dividend_yield'], reverse=True)[:5]
    
    # Best ROE
    best_roe = sorted([s for s in under_1000 if s['roe'] > 0], key=lambda x: x['roe'], reverse=True)[:5]
    
    return jsonify({
        'total_stocks': len(under_1000),
        'all_stocks': under_1000,
        'by_recommendation': {
            'strong_buy': strong_buy,
            'buy': buy,
            'hold': hold,
            'speculative': speculative,
            'avoid': avoid
        },
        'top_picks': {
            'best_pe_ratio': best_pe,
            'best_dividend_yield': best_dividend,
            'best_roe': best_roe
        },
        'analysis_summary': {
            'avg_pe_ratio': sum([s['pe_ratio'] for s in under_1000 if s['pe_ratio'] > 0]) / len([s for s in under_1000 if s['pe_ratio'] > 0]),
            'avg_dividend_yield': sum([s['dividend_yield'] for s in under_1000]) / len(under_1000),
            'avg_roe': sum([s['roe'] for s in under_1000 if s['roe'] > 0]) / len([s for s in under_1000 if s['roe'] > 0])
        }
    })

# Expense and Income Templates
@app.route('/api/templates/expense', methods=['GET'])
def get_expense_templates():
    conn = get_db_connection()
    templates = conn.execute('SELECT * FROM expense_templates ORDER BY category').fetchall()
    conn.close()
    return jsonify([dict(t) for t in templates])

@app.route('/api/templates/expense', methods=['POST'])
def add_expense_template():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO expense_templates (category, subcategory, default_amount, description, is_recurring) VALUES (?, ?, ?, ?, ?)',
        (data['category'], data.get('subcategory', ''), data.get('default_amount', 0), 
         data.get('description', ''), data.get('is_recurring', 0))
    )
    conn.commit()
    template_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    return jsonify({'id': template_id, 'message': 'Template added successfully'})

@app.route('/api/templates/expense/<int:template_id>', methods=['PUT'])
def update_expense_template(template_id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        'UPDATE expense_templates SET category = ?, subcategory = ?, default_amount = ?, description = ?, is_recurring = ? WHERE id = ?',
        (data['category'], data.get('subcategory', ''), data.get('default_amount', 0),
         data.get('description', ''), data.get('is_recurring', 0), template_id)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Template updated successfully'})

@app.route('/api/templates/expense/<int:template_id>', methods=['DELETE'])
def delete_expense_template(template_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM expense_templates WHERE id = ?', (template_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Template deleted successfully'})

@app.route('/api/templates/income', methods=['GET'])
def get_income_templates():
    conn = get_db_connection()
    templates = conn.execute('SELECT * FROM income_templates ORDER BY category').fetchall()
    conn.close()
    return jsonify([dict(t) for t in templates])

@app.route('/api/templates/income', methods=['POST'])
def add_income_template():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO income_templates (category, subcategory, default_amount, description, is_recurring) VALUES (?, ?, ?, ?, ?)',
        (data['category'], data.get('subcategory', ''), data.get('default_amount', 0),
         data.get('description', ''), data.get('is_recurring', 0))
    )
    conn.commit()
    template_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    return jsonify({'id': template_id, 'message': 'Template added successfully'})

@app.route('/api/templates/income/<int:template_id>', methods=['PUT'])
def update_income_template(template_id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        'UPDATE income_templates SET category = ?, subcategory = ?, default_amount = ?, description = ?, is_recurring = ? WHERE id = ?',
        (data['category'], data.get('subcategory', ''), data.get('default_amount', 0),
         data.get('description', ''), data.get('is_recurring', 0), template_id)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Template updated successfully'})

@app.route('/api/templates/income/<int:template_id>', methods=['DELETE'])
def delete_income_template(template_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM income_templates WHERE id = ?', (template_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Template deleted successfully'})

# Get expense categories from templates
@app.route('/api/templates/expense/categories', methods=['GET'])
def get_expense_categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT DISTINCT category FROM expense_templates ORDER BY category').fetchall()
    conn.close()
    return jsonify([dict(c) for c in categories])

# Asset Templates APIs
@app.route('/api/templates/asset', methods=['GET'])
def get_asset_templates():
    conn = get_db_connection()
    templates = conn.execute('SELECT * FROM asset_templates ORDER BY category').fetchall()
    conn.close()
    return jsonify([dict(t) for t in templates])

@app.route('/api/templates/asset', methods=['POST'])
def add_asset_template():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO asset_templates (category, subcategory, default_amount, description) VALUES (?, ?, ?, ?)',
        (data['category'], data.get('subcategory', ''), data.get('default_amount', 0), 
         data.get('description', ''))
    )
    conn.commit()
    template_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    return jsonify({'id': template_id, 'message': 'Asset template added successfully'})

@app.route('/api/templates/asset/<int:template_id>', methods=['DELETE'])
def delete_asset_template(template_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM asset_templates WHERE id = ?', (template_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Asset template deleted successfully'})

@app.route('/api/templates/asset/categories', methods=['GET'])
def get_asset_categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT DISTINCT category FROM asset_templates ORDER BY category').fetchall()
    conn.close()
    return jsonify([dict(c) for c in categories])

# Liability Templates APIs
@app.route('/api/templates/liability', methods=['GET'])
def get_liability_templates():
    conn = get_db_connection()
    templates = conn.execute('SELECT * FROM liability_templates ORDER BY category').fetchall()
    conn.close()
    return jsonify([dict(t) for t in templates])

@app.route('/api/templates/liability', methods=['POST'])
def add_liability_template():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO liability_templates (category, subcategory, default_amount, description) VALUES (?, ?, ?, ?)',
        (data['category'], data.get('subcategory', ''), data.get('default_amount', 0), 
         data.get('description', ''))
    )
    conn.commit()
    template_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    return jsonify({'id': template_id, 'message': 'Liability template added successfully'})

@app.route('/api/templates/liability/<int:template_id>', methods=['DELETE'])
def delete_liability_template(template_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM liability_templates WHERE id = ?', (template_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Liability template deleted successfully'})

@app.route('/api/templates/liability/categories', methods=['GET'])
def get_liability_categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT DISTINCT category FROM liability_templates ORDER BY category').fetchall()
    conn.close()
    return jsonify([dict(c) for c in categories])

@app.route('/api/templates/income/categories', methods=['GET'])
def get_income_categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT DISTINCT category FROM income_templates ORDER BY category').fetchall()
    conn.close()
    return jsonify([dict(c) for c in categories])

# Income Data APIs
@app.route('/api/income', methods=['GET'])
def get_income():
    conn = get_db_connection()
    income = conn.execute('SELECT * FROM income ORDER BY date DESC').fetchall()
    conn.close()
    return jsonify([dict(i) for i in income])

@app.route('/api/income', methods=['POST'])
def add_income():
    data = request.json
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO income (source, category, amount, date, is_recurring)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['source'], data['category'], data['amount'], data['date'], data.get('is_recurring', 0)))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Income added successfully'})

@app.route('/api/income/<int:income_id>', methods=['PUT'])
def update_income(income_id):
    data = request.json
    conn = get_db_connection()
    conn.execute('''
        UPDATE income 
        SET source = ?, category = ?, amount = ?, date = ?, is_recurring = ?
        WHERE id = ?
    ''', (data['source'], data['category'], data['amount'], data['date'], 
          data.get('is_recurring', 0), income_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Income updated successfully'})

@app.route('/api/income/<int:income_id>', methods=['DELETE'])
def delete_income(income_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM income WHERE id = ?', (income_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Income deleted successfully'})


# Recurring Deposits APIs
@app.route('/api/rd', methods=['GET'])
def get_rds():
    conn = get_db_connection()
    rds = conn.execute('SELECT * FROM recurring_deposits ORDER BY start_date DESC').fetchall()
    result = []
    for rd in rds:
        rd_dict = dict(rd)
        payments = conn.execute('SELECT * FROM rd_payments WHERE rd_id = ? ORDER BY month_number', (rd['id'],)).fetchall()
        rd_dict['payments'] = [dict(p) for p in payments]
        rd_dict['paid_months'] = len(payments)
        rd_dict['total_paid'] = sum([p['amount'] for p in payments])
        result.append(rd_dict)
    conn.close()
    return jsonify(result)

@app.route('/api/rd', methods=['POST'])
def add_rd():
    data = request.get_json()
    conn = get_db_connection()
    
    # Calculate maturity date and amount
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    tenure = int(data['tenure'])
    # Simple month addition (approximate)
    maturity_date = start_date + timedelta(days=tenure * 30)
    
    # Simple RD maturity calculation
    monthly_amount = float(data['monthly_amount'])
    tenure = int(data['tenure'])
    rate = float(data['interest_rate']) / 100
    
    # RD maturity formula: M = P * n * (n+1) / 2 * (r/12)
    total_deposit = monthly_amount * tenure
    interest = monthly_amount * tenure * (tenure + 1) / 2 * (rate / 12)
    maturity_amount = total_deposit + interest
    
    cursor = conn.execute(
        'INSERT INTO recurring_deposits (bank_name, account_number, monthly_amount, interest_rate, tenure, start_date, maturity_date, maturity_amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (data['bank_name'], data.get('account_number', ''), monthly_amount, data['interest_rate'], 
         tenure, data['start_date'], maturity_date.strftime('%Y-%m-%d'), maturity_amount)
    )
    rd_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'id': rd_id, 'message': 'RD added successfully', 'maturity_amount': maturity_amount})

@app.route('/api/rd/<int:rd_id>/payment', methods=['POST'])
def add_rd_payment(rd_id):
    data = request.get_json()
    conn = get_db_connection()
    
    # Get current payment count
    payments = conn.execute('SELECT COUNT(*) as count FROM rd_payments WHERE rd_id = ?', (rd_id,)).fetchone()
    month_number = payments['count'] + 1
    
    conn.execute(
        'INSERT INTO rd_payments (rd_id, payment_date, amount, month_number) VALUES (?, ?, ?, ?)',
        (rd_id, data['payment_date'], data['amount'], month_number)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Payment added successfully'})

@app.route('/api/rd/<int:rd_id>', methods=['DELETE'])
def delete_rd(rd_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM rd_payments WHERE rd_id = ?', (rd_id,))
    conn.execute('DELETE FROM recurring_deposits WHERE id = ?', (rd_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'RD deleted successfully'})

# Chit Fund APIs
@app.route('/api/chit', methods=['GET'])
def get_chits():
    conn = get_db_connection()
    chits = conn.execute('SELECT * FROM chit_funds ORDER BY start_date DESC').fetchall()
    result = []
    for chit in chits:
        chit_dict = dict(chit)
        payments = conn.execute('SELECT * FROM chit_payments WHERE chit_id = ? ORDER BY month_number', (chit['id'],)).fetchall()
        chit_dict['payments'] = [dict(p) for p in payments]
        chit_dict['paid_months'] = len(payments)
        chit_dict['total_paid'] = sum([p['amount'] for p in payments])
        result.append(chit_dict)
    conn.close()
    return jsonify(result)

@app.route('/api/chit', methods=['POST'])
def add_chit():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO chit_funds (chit_name, total_value, monthly_amount, total_months, start_date, organizer) VALUES (?, ?, ?, ?, ?, ?)',
        (data['chit_name'], data['total_value'], data['monthly_amount'], data['total_months'], 
         data['start_date'], data.get('organizer', ''))
    )
    chit_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'id': chit_id, 'message': 'Chit fund added successfully'})

@app.route('/api/chit/<int:chit_id>/payment', methods=['POST'])
def add_chit_payment(chit_id):
    data = request.get_json()
    conn = get_db_connection()
    
    # Get current payment count
    payments = conn.execute('SELECT COUNT(*) as count FROM chit_payments WHERE chit_id = ?', (chit_id,)).fetchone()
    month_number = payments['count'] + 1
    
    conn.execute(
        'INSERT INTO chit_payments (chit_id, payment_date, amount, month_number) VALUES (?, ?, ?, ?)',
        (chit_id, data['payment_date'], data['amount'], month_number)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Payment added successfully'})

@app.route('/api/chit/<int:chit_id>', methods=['DELETE'])
def delete_chit(chit_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM chit_payments WHERE chit_id = ?', (chit_id,))
    conn.execute('DELETE FROM chit_funds WHERE id = ?', (chit_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Chit fund deleted successfully'})

# Gold Chit APIs
@app.route('/api/gold-chit', methods=['GET'])
def get_gold_chits():
    conn = get_db_connection()
    gold_chits = conn.execute('SELECT * FROM gold_chits ORDER BY start_date DESC').fetchall()
    result = []
    for gc in gold_chits:
        gc_dict = dict(gc)
        payments = conn.execute('SELECT * FROM gold_chit_payments WHERE gold_chit_id = ? ORDER BY month_number', (gc['id'],)).fetchall()
        gc_dict['payments'] = [dict(p) for p in payments]
        gc_dict['paid_months'] = len(payments)
        gc_dict['total_paid'] = sum([p['amount'] for p in payments])
        result.append(gc_dict)
    conn.close()
    return jsonify(result)

@app.route('/api/gold-chit', methods=['POST'])
def add_gold_chit():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO gold_chits (chit_name, gold_weight, monthly_amount, total_months, start_date, jeweller) VALUES (?, ?, ?, ?, ?, ?)',
        (data['chit_name'], data['gold_weight'], data['monthly_amount'], data['total_months'], 
         data['start_date'], data.get('jeweller', ''))
    )
    gc_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'id': gc_id, 'message': 'Gold chit added successfully'})

@app.route('/api/gold-chit/<int:gc_id>/payment', methods=['POST'])
def add_gold_chit_payment(gc_id):
    data = request.get_json()
    conn = get_db_connection()
    
    # Get current payment count
    payments = conn.execute('SELECT COUNT(*) as count FROM gold_chit_payments WHERE gold_chit_id = ?', (gc_id,)).fetchone()
    month_number = payments['count'] + 1
    
    conn.execute(
        'INSERT INTO gold_chit_payments (gold_chit_id, payment_date, amount, month_number) VALUES (?, ?, ?, ?)',
        (gc_id, data['payment_date'], data['amount'], month_number)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Payment added successfully'})

@app.route('/api/gold-chit/<int:gc_id>', methods=['DELETE'])
def delete_gold_chit(gc_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM gold_chit_payments WHERE gold_chit_id = ?', (gc_id,))
    conn.execute('DELETE FROM gold_chits WHERE id = ?', (gc_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Gold chit deleted successfully'})

# Financial Health Score
@app.route('/api/financial-health', methods=['GET'])
def financial_health():
    conn = get_db_connection()
    
    # Get current month data
    current_month = datetime.now().strftime('%Y-%m')
    
    # Calculate metrics
    assets = conn.execute('SELECT SUM(value) as total FROM assets WHERE month = ?', (current_month,)).fetchone()
    liabilities = conn.execute('SELECT SUM(amount) as total FROM liabilities WHERE month = ?', (current_month,)).fetchone()
    expenses = conn.execute('SELECT SUM(amount) as total FROM expenses WHERE month = ?', (current_month,)).fetchone()
    
    total_assets = assets['total'] if assets['total'] else 0
    total_liabilities = liabilities['total'] if liabilities['total'] else 0
    total_expenses = expenses['total'] if expenses['total'] else 0
    
    # Calculate scores
    net_worth = total_assets - total_liabilities
    debt_to_asset_ratio = (total_liabilities / total_assets * 100) if total_assets > 0 else 100
    
    # Generate score (0-100)
    score = 100
    if debt_to_asset_ratio > 50:
        score -= 30
    elif debt_to_asset_ratio > 30:
        score -= 15
    
    if net_worth < 0:
        score -= 25
    elif net_worth < total_expenses * 3:
        score -= 10
    
    # Generate recommendations
    recommendations = []
    if debt_to_asset_ratio > 40:
        recommendations.append("🎯 Focus on debt reduction - your debt-to-asset ratio is high")
    if net_worth < total_expenses * 6:
        recommendations.append("💰 Build emergency fund - aim for 6 months of expenses")
    if total_assets < total_expenses * 12:
        recommendations.append("📈 Increase savings rate - build long-term wealth")
    
    conn.close()
    
    return jsonify({
        'score': max(0, min(100, score)),
        'net_worth': net_worth,
        'debt_to_asset_ratio': debt_to_asset_ratio,
        'recommendations': recommendations,
        'metrics': {
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'monthly_expenses': total_expenses
        }
    })

if __name__ == '__main__':
    print("Personal Finance Tracker - Simple Backend Starting...")
    print("=" * 50)
    print("Backend URL: http://localhost:5000")
    print("Database: SQLite (finance_simple.db)")
    print("Environment: Development")
    print("-" * 50)
    # Initialize database
    init_db()
    print("Database initialized successfully")
    
    print("Starting Flask server...")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    # Run the server
    app.run(debug=True, host='0.0.0.0', port=5000)
