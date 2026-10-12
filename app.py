from flask import Flask, render_template
import pymysql

app = Flask(__name__)


def get_connection():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="tu_password",
        database="zoo",
        cursorclass=pymysql.cursors.DictCursor,
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/animales')
def animales():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, nombre, raza, comida FROM animal")
        datos = cursor.fetchall()
    conn.close()
    return {"animales": datos}


if __name__ == '__main__':
    app.run(debug=True)
