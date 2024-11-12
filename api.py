# app.py

from flask import Flask, request, jsonify
import pyodbc
from config import DATABASE_CONFIG
from config import CLIENT_CONFIG

app = Flask(__name__)

# Função para conectar ao SQL Server
def get_db_connection():
    conn = pyodbc.connect(
        f"DRIVER={{{DATABASE_CONFIG['driver']}}};"
        f"SERVER={DATABASE_CONFIG['server']};"
        f"DATABASE={DATABASE_CONFIG['database']};"
        f"UID={DATABASE_CONFIG['username']};"
        f"PWD={DATABASE_CONFIG['password']}"
    )
    return conn

# Endpoint para adicionar dados
@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json
    name = data.get('name')
    age = data.get('age')

    if not name or not age:
        return jsonify({"error": "Os campos 'name' e 'age' são obrigatórios."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # query = "INSERT INTO Users (Name, Age) VALUES (?, ?)"
        cursor.execute(query, (name, age))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Dados inseridos com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para listar dados
@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC vw_list_picagem @BD = '"+CLIENT_CONFIG['database']+"', @search = '', @distinct = 0, @debug = 1")

        # Obtém os nomes das colunas a partir da descrição do cursor
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        # Transforma cada linha em um dicionário usando os nomes das colunas
        data = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        return jsonify(data), 200


    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
