import uuid
import pytest
import app as modulo_app


@pytest.fixture
def client():
    modulo_app.app.config["TESTING"] = True
    with modulo_app.app.test_client() as client:
        yield client


@pytest.fixture
def db_real():
    try:
        conn = modulo_app.get_connection()
    except Exception as e:
        pytest.skip(f"No hay base de datos disponible: {e}")
    conn.close()


def test_agregar_animal_en_base_real(client, db_real):
    nombre = "test-" + uuid.uuid4().hex[:8]
    r = client.post("/animales", json={"nombre": nombre, "raza": "prueba", "comida": "prueba"})
    assert r.status_code == 201
    nuevo_id = r.get_json()["id"]
    try:
        lista = client.get("/animales").get_json()
        assert any(a["id"] == nuevo_id and a["nombre"] == nombre for a in lista)
    finally:
        conn = modulo_app.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM animal WHERE id = %s", (nuevo_id,))
        conn.commit()
        conn.close()


def test_animales_guardados_son_validos(db_real):
    conn = modulo_app.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nombre, raza, comida FROM animal")
            filas = cursor.fetchall()
    finally:
        conn.close()

    for fila in filas:
        for campo in ("nombre", "raza", "comida"):
            valor = fila[campo]
            assert valor and valor.strip(), f"Animal {fila['id']}: {campo} está vacío"
            assert len(valor) <= 45, f"Animal {fila['id']}: {campo} pasa de 45 caracteres"