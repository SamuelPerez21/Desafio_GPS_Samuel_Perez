#Desarrollado por: Samuel Perez
from flask import Flask, request, jsonify
import time
import psycopg2 
import os

app = Flask(__name__)

# Conexion a la base de datos PostgreSQL
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

def get_conncection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def create_table():
    conn = get_conncection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evaluaciones (
            id SERIAL PRIMARY KEY,
            rut_estudiante VARCHAR REFERENCES estudiantes(rut) ,
            semestre VARCHAR,
            asignatura VARCHAR,
            evaluacion NUMERIC
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/evaluaciones", methods=["POST"])
def crear_evaluacion():
    data = request.json
    try:
        nota = float(data["evaluacion"])
        if nota < 1 or nota > 7:
            return jsonify({"error": "La nota debe estar entre 1 y 7"}), 400
    except:
        return jsonify({"error": "La nota debe ser un número"}), 400

    try:
        conn = get_conncection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO evaluaciones (rut_estudiante, semestre, asignatura, evaluacion)
            VALUES (%s, %s, %s, %s)
        """, (data["rut_estudiante"], data["semestre"], data["asignatura"], nota))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensaje": "Evaluación registrada"}), 201

    except psycopg2.errors.ForeignKeyViolation:
        return jsonify({"error": "El estudiante no existe. Debe crearlo antes de asignar evaluaciones."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/evaluaciones", methods=["GET"])
def listar_evaluaciones():
    conn = get_conncection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM evaluaciones")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    evaluaciones = [
        {"id": r[0], "rut_estudiante": r[1], "semestre": r[2], "asignatura": r[3], "evaluacion": float(r[4])} for r in rows
    ]
    return jsonify(evaluaciones), 200

@app.route("/evaluaciones/<rut>", methods=["GET"])
def obtener_por_rut(rut):
    conn = get_conncection()
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM evaluaciones WHERE rut_estudiante = %s", (rut,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    if not rows:
        return jsonify({"error": "No se encontraron evaluaciones para el rut proporcionado"}), 404
    
    evaluaciones = [
        {"id": r[0], "rut_estudiante": r[1], "semestre": r[2], "asignatura": r[3], "evaluacion": float(r[4])} for r in rows
    ]
    return jsonify(evaluaciones)


if __name__ == "__main__":
    wait_for_db()
    create_table()
    app.run(host="0.0.0.0", port=5001)
