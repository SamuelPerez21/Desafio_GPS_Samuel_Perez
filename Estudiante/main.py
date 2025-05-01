from flask import Flask, request, jsonify
import time
import psycopg2
import os

app = Flask(__name__)

#Conexion a la base de datos PostgreSQL
DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

def wait_for_db():
    while True:
        try:
            conn = get_conncection()
            conn.close()
            break
        except psycopg2.OperationalError:
            print("Esperando a que la base de datos esté disponible...")
            time.sleep(5)

def get_conncection ():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

#Creacion de la tabla si es que no existe
def create_table():
    conn = get_conncection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes (
            rut VARCHAR PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            edad INTEGER NOT NULL,
            curso VARCHAR(100) NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/estudiantes", methods=["POST"])
def crear_estudiante():
    data = request.json
    try:
        conn = get_conncection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO estudiantes (rut, nombre, edad, curso) VALUES (%s, %s, %s, %s)", (data["rut"], data["nombre"], data["edad"], data["curso"]))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Estudiante creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route("/estudiantes", methods=["GET"])
def listar_estudiantes():
    conn = get_conncection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM estudiantes")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    estudiantes = [
        {"rut": r[0], "nombre": r[1], "edad": r[2], "curso": r[3]} for r in rows
    ]
    return jsonify(estudiantes), 200

@app.route("/estudiantes/<rut>", methods=["GET"])
def obtener_estudiante(rut):
    conn = get_conncection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM estudiantes WHERE rut = %s", (rut,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        estudiante = {"rut": row[0], "nombre": row[1], "edad": row[2], "curso": row[3]}
        return jsonify(estudiante), 200
    else:
        return jsonify({"error": "Estudiante no encontrado"}), 404
    
if __name__ == "__main__":
    wait_for_db()
    create_table()
    app.run(host="0.0.0.0", port=5000)