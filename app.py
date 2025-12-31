import os
import time
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL config (no risky defaults)
app.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = os.environ['MYSQL_DB']

mysql = MySQL(app)

def init_db_with_retry(retries=10, delay=5):
    for i in range(retries):
        try:
            with app.app_context():
                cur = mysql.connection.cursor()
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        message TEXT
                    )
                """)
                mysql.connection.commit()
                cur.close()
            print("Database initialized successfully")
            return
        except Exception as e:
            print(f"Database not ready ({i+1}/{retries}), retrying...")
            time.sleep(delay)

    raise Exception("Database connection failed after retries")

@app.route('/')
def hello():
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', (new_message,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': new_message})

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    init_db_with_retry()
    app.run(host='0.0.0.0', port=5000)
