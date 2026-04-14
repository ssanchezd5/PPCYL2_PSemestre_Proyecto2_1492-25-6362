import xml.etree.ElementTree as ET


def procesar_xml_especifico(contenido_string):
    try:
        # Limpieza básica por si el XML viene con etiquetas de bloque de código
        limpio = contenido_string.replace('```xml', '').replace('```', '').strip()
        root = ET.fromstring(limpio)
        materia_xml = root.attrib.get('materia')

        estudiantes = []
        for est in root.findall('estudiante'):
            estudiantes.append({
                "nombre": est.find('nombre').text.strip(),
                "nota": est.find('nota').text.strip()
            })
        return {"materia": materia_xml, "estudiantes": estudiantes}
    except Exception as e:
        return {"error": str(e)}