from flask import Flask, request, jsonify, make_response
from flask_cors import CORS  
import pandas as pd
import sqlite3

app = Flask(__name__)
CORS(app)  

def get_schedule(class_name, path):
    df = pd.read_excel(path, header=None)  
    
    schedule = []
    
    class_row = 1 
    class_col = None
    
    for col in range(3, len(df.columns)): 
        if str(df.iloc[class_row, col]) == class_name:
            class_col = col
            break
    
    if class_col is None:
        return []
    
    for row in range(2, len(df)):
        lesson_number = df.iloc[row, 1]
        if pd.isna(lesson_number):
            continue
            
        time = df.iloc[row, 2]
        lesson_info = df.iloc[row, class_col]
        
        classroom = df.iloc[row + 1, class_col]

        if pd.isna(lesson_info):
            continue
            
        if pd.isna(classroom):
            classroom = ""
        temp = []
        temp.append(int(lesson_number))
        temp.append(time)
        temp.append(lesson_info)
        temp.append(classroom)
        schedule.append(temp)

       

    return [list(map(lambda x: x.encode('utf-8').decode('utf-8') if isinstance(x, str) else x, item)) for item in schedule]

@app.route('/api/v1/get_schedule', methods=['GET'])
def get_schedule_api():
    class_name = request.args.get('class')
    day = request.args.get('day')
    
    if class_name and day:
        path = f'{day}.xlsx'
        schedule = get_schedule(class_name, path)
        response = make_response(jsonify(schedule), 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    else:
        response = make_response(jsonify({"error": "Class and day parameters are required"}), 400)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response


@app.route('/api/main/initdb', methods=['GET'])
def initdb():
    key = request.args.get('key')

    if key == '1234567890':
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        org_key TEXT NOT NULL,
        fio TEXT NOT NULL,
        class TEXT NOT NULL,
        login TEXT NOT NULL,
        password TEXT NOT NULL,
        status BOOLEAN NOT NULL DEFAULT 0
        )
        ''')
        connection.commit()
        connection.close()
        return make_response(jsonify({"message": "database initialized! Table Users created"}), 200)
    else:
        return make_response(jsonify({"error": "Invalid key"}), 401)

@app.route('/api/main/initadmin', methods=['GET'])
def initadmin():
    key = request.args.get('key')


    if key == '1234567890':
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Users (org_key, fio, class, login, password, status) VALUES (?, ?, ?, ?, ?, ?)', ('0000000000', 'admin', 'admin', 'admin', 'admin', 1))
        connection.commit()
        connection.close()
        return make_response(jsonify({"message": "admin created"}), 200)


    else:
        return make_response(jsonify({"error": "Invalid key"}), 401)


@app.route('/api/v1/login', methods=['POST'])
def login():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    cursor.execute('SELECT * FROM Users WHERE login = ? AND password = ? AND status = 1', (username, password))
    user = cursor.fetchone()

    if user:
        return make_response(jsonify({"message": "Login successful"}), 200)
    else:

        return make_response(jsonify({"error": "Invalid credentials"}), 401)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)