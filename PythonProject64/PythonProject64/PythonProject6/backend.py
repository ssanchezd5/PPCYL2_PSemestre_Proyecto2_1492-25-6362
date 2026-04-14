import sqlite3, json, xml.etree.ElementTree as ET
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = 'db.sqlite3'


def ejecutar_query(query, parametros=()):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, parametros)
        conn.commit()
        return cursor


# Crear tablas
with sqlite3.connect(DB_PATH) as conn:
    conn.execute('CREATE TABLE IF NOT EXISTS usuarios_sistema (usuario TEXT PRIMARY KEY, password TEXT, rol TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS datos_estudiantes (nombre TEXT PRIMARY KEY, notas TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS horarios_clases (materia TEXT PRIMARY KEY, horario TEXT)')
    conn.execute("INSERT OR IGNORE INTO usuarios_sistema VALUES ('admin_root', 'root', 'administrador')")


@app.route('/')
def home(): return "<h1>✅ API FUNCIONANDO CORRECTAMENTE</h1>"


@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    cursor = ejecutar_query("SELECT rol FROM usuarios_sistema WHERE usuario=? AND password=?",
                            (datos.get('usuario'), datos.get('password')))
    res = cursor.fetchone()
    if res: return jsonify({'rol': res[0], 'usuario': datos.get('usuario')})
    return jsonify({'error': 'invalid'}), 401


@app.route('/obtener_usuarios', methods=['GET'])
def obtener_usuarios():
    cursor = ejecutar_query("SELECT usuario, rol FROM usuarios_sistema")
    return jsonify([{"usuario": f[0], "rol": f[1]} for f in cursor.fetchall()])


@app.route('/gestionar_usuario', methods=['POST'])
def gestionar_usuario():
    d = request.get_json()
    ejecutar_query("INSERT OR REPLACE INTO usuarios_sistema VALUES (?, ?, ?)", (d['nombre'], d['pass'], d['rol']))
    return jsonify({'msj': 'ok'})


@app.route('/eliminar_usuario', methods=['POST'])
def eliminar_usuario():
    d = request.get_json()
    ejecutar_query("DELETE FROM usuarios_sistema WHERE usuario=?", (d.get('nombre'),))
    return jsonify({'msj': 'ok'})


@app.route('/subir_notas_xml', methods=['POST'])
def subir_notas_xml():
    try:
        xml_text = request.data.decode('utf-8').strip()
        root = ET.fromstring(xml_text)

        # CORRECCIÓN AQUÍ: Cambiamos 'alumno' por 'estudiante' para que coincida con tu XML
        for est in root.findall('estudiante'):
            nombre = est.find('nombre').text.strip()

            cursor = ejecutar_query("SELECT notas FROM datos_estudiantes WHERE nombre=?", (nombre,))
            res = cursor.fetchone()
            notas_db = json.loads(res[0]) if res else {}

            # Buscamos la etiqueta 'curso' como en tu archivo
            for c in est.findall('curso'):
                materia = c.find('materia').text.strip()
                nota = c.find('nota').text.strip()
                notas_db[materia] = nota

            ejecutar_query("INSERT OR REPLACE INTO datos_estudiantes VALUES (?, ?)", (nombre, json.dumps(notas_db)))

        return jsonify({'msj': 'ok'}), 200
    except Exception as e:
        print(f"Error procesando XML: {e}")
        return jsonify({'error': str(e)}), 400


@app.route('/obtener_todos_alumnos', methods=['GET'])
def obtener_todos_alumnos():
    cursor = ejecutar_query("SELECT nombre, notas FROM datos_estudiantes")
    return jsonify([{"nombre": f[0], "notas": json.loads(f[1])} for f in cursor.fetchall()])


@app.route('/obtener_alumno/<nombre>', methods=['GET'])
def obtener_alumno(nombre):
    cursor = ejecutar_query("SELECT notas FROM datos_estudiantes WHERE nombre=?", (nombre,))
    res = cursor.fetchone()
    return jsonify({'notas': json.loads(res[0])}) if res else jsonify({'notas': {}})


@app.route('/guardar_horario', methods=['POST'])
def guardar_horario():
    d = request.get_json()
    ejecutar_query("INSERT OR REPLACE INTO horarios_clases VALUES (?, ?)", (d['materia'], d['horario']))
    return jsonify({'msj': 'ok'})


@app.route('/obtener_todos_horarios', methods=['GET'])
def obtener_todos_horarios():
    cursor = ejecutar_query("SELECT materia, horario FROM horarios_clases")
    return jsonify([{"materia": f[0], "horario": f[1]} for f in cursor.fetchall()])


if __name__ == '__main__':
    app.run(debug=True, port=5000)