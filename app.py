from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)


def get_connection():
    return pymysql.connect(
        host="localhost",
        port=9999,
        user="root",
        password="64571ok.",  # <- pon tu contraseña real
        database="zoodb",
        cursorclass=pymysql.cursors.DictCursor,
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/animales', methods=['GET'])
def listar_animales():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, raza, comida FROM animal ORDER BY id DESC"
            )
            datos = cursor.fetchall()
        return jsonify(datos)
    finally:
        conn.close()


@app.route('/animales', methods=['POST'])
def guardar_animal():
    datos = request.get_json(silent=True) or {}
    nombre = (datos.get('nombre') or '').strip()
    raza = (datos.get('raza') or '').strip()
    comida = (datos.get('comida') or '').strip()

    if not nombre or not raza or not comida:
        return jsonify({"error": "Nombre, raza y comida son obligatorios."}), 400
    if max(len(nombre), len(raza), len(comida)) > 45:
        return jsonify({"error": "Cada campo admite máximo 45 caracteres."}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO animal (nombre, raza, comida) VALUES (%s, %s, %s)",
                (nombre, raza, comida),
            )
            nuevo_id = cursor.lastrowid
        conn.commit()
        return jsonify({"id": nuevo_id, "nombre": nombre, "raza": raza, "comida": comida}), 201
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)