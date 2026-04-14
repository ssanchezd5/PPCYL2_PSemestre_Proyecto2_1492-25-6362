import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse


# 1. LOGIN
def login_view(request):
    if request.method == 'POST':
        u, p = request.POST.get('usuario'), request.POST.get('password')
        try:
            r = requests.post('http://127.0.0.1:5000/login', json={'usuario': u, 'password': p})
            if r.status_code == 200:
                res = r.json()
                request.session['rol'], request.session['usuario'] = res['rol'], res['usuario']
                if res['rol'] == 'administrador': return redirect('/admin_panel/')
                if res['rol'] == 'maestro': return redirect('/subir/')
                if res['rol'] == 'alumno': return redirect('/alumno/')
            return HttpResponse("Credenciales incorrectas")
        except:
            return HttpResponse("Backend apagado")
    return render(request, 'login.html')


# 2. PANEL ADMIN (🔥 XML CONFIG AQUÍ)
def admin_panel(request):
    if request.session.get('rol') != 'administrador':
        return redirect('/')

    mensaje = None

    # 🔥 CARGAR XML CONFIG
    if request.method == 'POST':
        archivo = request.FILES.get('archivo_config')

        if not archivo:
            mensaje = "❌ No seleccionaste archivo"
        else:
            xml_bytes = archivo.read()

            print("Tamaño XML:", len(xml_bytes))  # DEBUG

            if len(xml_bytes) == 0:
                mensaje = "❌ El archivo está vacío"
            else:
                try:
                    r = requests.post(
                        'http://127.0.0.1:5000/cargar_configuracion_xml',
                        data=xml_bytes
                    )

                    print("Respuesta backend:", r.text)  # DEBUG

                    if r.status_code == 200:
                        mensaje = "✅ Configuración cargada correctamente"
                    else:
                        mensaje = f"❌ Error backend: {r.text}"

                except Exception as e:
                    mensaje = f"❌ Error conexión: {e}"

    # Obtener usuarios
    try:
        r = requests.get('http://127.0.0.1:5000/obtener_usuarios')
        usuarios = r.json() if r.status_code == 200 else []
    except:
        usuarios = []

    return render(request, 'admin_panel.html', {
        'usuarios_sistema': usuarios,
        'usuario': request.session.get('usuario'),
        'mensaje': mensaje
    })


# 3. CREAR USUARIO
def crear_usuario_view(request):
    if request.method == 'POST':
        d = {
            'nombre': request.POST.get('nuevo_nom'),
            'pass': request.POST.get('nuevo_pass'),
            'rol': request.POST.get('nuevo_rol')
        }
        requests.post('http://127.0.0.1:5000/gestionar_usuario', json=d)
    return redirect('/admin_panel/')


# 4. ELIMINAR USUARIO
def eliminar_usuario_view(request):
    if request.method == 'POST':
        requests.post('http://127.0.0.1:5000/eliminar_usuario', json={
            'nombre': request.POST.get('nombre_eliminar')
        })
    return redirect('/admin_panel/')


# 5. PANEL MAESTRO
def subir_xml(request):
    if request.session.get('rol') != 'maestro': return redirect('/')
    u = request.session.get('usuario', '')

    if "mate" in u.lower():
        materia_maestro = "Matematica"
    elif "prog" in u.lower():
        materia_maestro = "Programacion"
    elif "bio" in u.lower():
        materia_maestro = "Biologia"
    elif "calc" in u.lower():
        materia_maestro = "Calculo"
    else:
        materia_maestro = "General"

    if request.method == 'POST':
        if request.FILES.get('archivo_xml'):
            archivo = request.FILES['archivo_xml']
            requests.post('http://127.0.0.1:5000/subir_notas_xml', data=archivo.read())

        elif 'nuevo_horario' in request.POST:
            requests.post('http://127.0.0.1:5000/guardar_horario', json={
                'materia': materia_maestro,
                'horario': request.POST.get('nuevo_horario')
            })

    try:
        r = requests.get('http://127.0.0.1:5000/obtener_todos_alumnos')
        todos = r.json() if r.status_code == 200 else []

        lista_filtrada = []
        for x in todos:
            notas = x.get('notas', {})
            for m_db, calif in notas.items():
                if materia_maestro.lower() in m_db.lower():
                    lista_filtrada.append({'nombre': x['nombre'], 'nota': calif})
                    break
    except:
        lista_filtrada = []

    return render(request, 'subir_xml.html', {
        'materia': materia_maestro,
        'alumnos': lista_filtrada,
        'usuario': u
    })


# 6. PANEL ALUMNO
def alumno_view(request):
    u = request.session.get('usuario')
    if not u: return redirect('/')
    try:
        r_n = requests.get(f'http://127.0.0.1:5000/obtener_alumno/{u}')
        r_h = requests.get('http://127.0.0.1:5000/obtener_todos_horarios')
        notas = r_n.json().get('notas', {}) if r_n.status_code == 200 else {}
        horarios = r_h.json() if r_h.status_code == 200 else []
    except:
        notas, horarios = {}, []

    return render(request, 'alumno.html', {
        'usuario': u,
        'notas': notas,
        'horarios': horarios
    })


# 7. LOGOUT
def cerrar_sesion(request):
    request.session.flush()
    return redirect('/')
