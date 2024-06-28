from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

password = os.getenv('DB_PASSWORD')
database = os.getenv('DB')
endpoint = os.getenv('DB_URL')

app = Flask(__name__)
CORS(app)

db_config = {
    'user': 'admin',
    'password': password,
    'host': endpoint,
    'database': database
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (first_name, last_name) VALUES (%s, %s)", (first_name, last_name))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'message': 'User added successfully!'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(users), 200

if __name__ == '__main__':
    app.run(debug=True)
