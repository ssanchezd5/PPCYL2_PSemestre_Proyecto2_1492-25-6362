import sqlite3
import json
import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)
DB_PATH = 'db.sqlite3'


# -----------------------
# BASE DE DATOS
# -----------------------
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


# -----------------------
# FUNCIÓN GENERAR XML
# -----------------------
def generar_xml_salida(tutores, estudiantes, asign_tutores, asign_estudiantes):
    root = ET.Element("configuraciones_aplicadas")

    ET.SubElement(root, "tutores_cargados").text = str(tutores)
    ET.SubElement(root, "estudiantes_cargados").text = str(estudiantes)

    asignaciones = ET.SubElement(root, "asignaciones")

    tutores_xml = ET.SubElement(asignaciones, "tutores")
    ET.SubElement(tutores_xml, "total").text = str(asign_tutores["total"])
    ET.SubElement(tutores_xml, "correcto").text = str(asign_tutores["correcto"])
    ET.SubElement(tutores_xml, "incorrecto").text = str(asign_tutores["incorrecto"])

    est_xml = ET.SubElement(asignaciones, "estudiantes")
    ET.SubElement(est_xml, "total").text = str(asign_estudiantes["total"])
    ET.SubElement(est_xml, "correcto").text = str(asign_estudiantes["correcto"])
    ET.SubElement(est_xml, "incorrecto").text = str(asign_estudiantes["incorrecto"])

    tree = ET.ElementTree(root)
    tree.write("salida.xml", encoding="utf-8", xml_declaration=True)

    print("🔥 XML GENERADO CORRECTAMENTE")


# -----------------------
# ENDPOINTS
# -----------------------

@app.route('/')
def home():
    return "<h1>✅ API FUNCIONANDO</h1>"


@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    cursor = ejecutar_query(
        "SELECT rol FROM usuarios_sistema WHERE usuario=? AND password=?",
        (datos.get('usuario'), datos.get('password'))
    )
    res = cursor.fetchone()
    if res:
        return jsonify({'rol': res[0], 'usuario': datos.get('usuario')})
    return jsonify({'error': 'invalid'}), 401


@app.route('/obtener_usuarios', methods=['GET'])
def obtener_usuarios():
    cursor = ejecutar_query("SELECT usuario, rol FROM usuarios_sistema")
    return jsonify([{"usuario": f[0], "rol": f[1]} for f in cursor.fetchall()])


@app.route('/gestionar_usuario', methods=['POST'])
def gestionar_usuario():
    d = request.get_json()
    ejecutar_query(
        "INSERT OR REPLACE INTO usuarios_sistema VALUES (?, ?, ?)",
        (d['nombre'], d['pass'], d['rol'])
    )
    return jsonify({'msj': 'ok'})


@app.route('/eliminar_usuario', methods=['POST'])
def eliminar_usuario():
    d = request.get_json()
    ejecutar_query("DELETE FROM usuarios_sistema WHERE usuario=?", (d.get('nombre'),))
    return jsonify({'msj': 'ok'})


# -----------------------
# 🔥 CARGAR CONFIG XML
# -----------------------
@app.route('/cargar_configuracion_xml', methods=['POST'])
def cargar_configuracion_xml():
    try:
        xml_text = request.data.decode('utf-8').strip()

        print("🔥 XML RECIBIDO:")
        print(xml_text[:300])

        if not xml_text:
            return jsonify({"error": "XML vacío"}), 400

        root = ET.fromstring(xml_text)

        tutores = 0
        estudiantes = 0

        asign_tutores = {"total": 0, "correcto": 0, "incorrecto": 0}
        asign_estudiantes = {"total": 0, "correcto": 0, "incorrecto": 0}

        cursos = set()

        # Cursos
        for c in root.findall('.//curso'):
            codigo = c.attrib.get("codigo")
            if codigo:
                cursos.add(codigo)

        # Tutores
        tutores_ids = set()
        for t in root.findall('.//tutor'):
            usuario = t.attrib.get("registro_personal")
            password = t.attrib.get("contrasenia")

            if usuario and password:
                ejecutar_query(
                    "INSERT OR REPLACE INTO usuarios_sistema VALUES (?, ?, ?)",
                    (usuario, password, "tutor")
                )
                tutores_ids.add(usuario)
                tutores += 1

        # Estudiantes
        estudiantes_ids = set()
        for e in root.findall('.//estudiante'):
            carnet = e.attrib.get("carnet")
            password = e.attrib.get("contrasenia")

            if carnet and password:
                ejecutar_query(
                    "INSERT OR REPLACE INTO usuarios_sistema VALUES (?, ?, ?)",
                    (carnet, password, "estudiante")
                )
                estudiantes_ids.add(carnet)
                estudiantes += 1

        # Asignaciones tutores
        for t in root.findall('.//tutor_curso'):
            asign_tutores["total"] += 1
            codigo = t.attrib.get("codigo")
            tutor_id = t.text.strip() if t.text else None

            if codigo in cursos and tutor_id in tutores_ids:
                asign_tutores["correcto"] += 1
            else:
                asign_tutores["incorrecto"] += 1

        # Asignaciones estudiantes
        for e in root.findall('.//estudiante_curso'):
            asign_estudiantes["total"] += 1
            codigo = e.attrib.get("codigo")
            carnet = e.text.strip() if e.text else None

            if codigo in cursos and carnet in estudiantes_ids:
                asign_estudiantes["correcto"] += 1
            else:
                asign_estudiantes["incorrecto"] += 1

        # 🔥 GENERAR XML
        generar_xml_salida(tutores, estudiantes, asign_tutores, asign_estudiantes)

        return jsonify({"mensaje": "ok"})

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": str(e)}), 400


# -----------------------
# DESCARGAR XML
# -----------------------
@app.route('/descargar_xml', methods=['GET'])
def descargar_xml():
    try:
        return send_file("salida.xml", as_attachment=True)
    except:
        return jsonify({"error": "No existe el archivo"}), 404


# -----------------------
# NOTAS XML
# -----------------------
@app.route('/subir_notas_xml', methods=['POST'])
def subir_notas_xml():
    try:
        xml_text = request.data.decode('utf-8').strip()
        root = ET.fromstring(xml_text)

        for est in root.findall('estudiante'):
            nombre = est.find('nombre').text.strip()

            cursor = ejecutar_query("SELECT notas FROM datos_estudiantes WHERE nombre=?", (nombre,))
            res = cursor.fetchone()
            notas_db = json.loads(res[0]) if res else {}

            for c in est.findall('curso'):
                materia = c.find('materia').text.strip()
                nota = c.find('nota').text.strip()
                notas_db[materia] = nota

            ejecutar_query(
                "INSERT OR REPLACE INTO datos_estudiantes VALUES (?, ?)",
                (nombre, json.dumps(notas_db))
            )

        return jsonify({'msj': 'ok'})

    except Exception as e:
        print("❌ ERROR NOTAS:", e)
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


# -----------------------
# HORARIOS
# -----------------------
@app.route('/guardar_horario', methods=['POST'])
def guardar_horario():
    d = request.get_json()
    ejecutar_query("INSERT OR REPLACE INTO horarios_clases VALUES (?, ?)", (d['materia'], d['horario']))
    return jsonify({'msj': 'ok'})


@app.route('/obtener_todos_horarios', methods=['GET'])
def obtener_todos_horarios():
    cursor = ejecutar_query("SELECT materia, horario FROM horarios_clases")
    return jsonify([{"materia": f[0], "horario": f[1]} for f in cursor.fetchall()])


# -----------------------
# RUN
# -----------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)