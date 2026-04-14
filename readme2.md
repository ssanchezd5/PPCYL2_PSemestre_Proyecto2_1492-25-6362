[Guia de Inicio de Proyecto.pdf](https://github.com/user-attachments/files/26730625/Guia.de.Inicio.de.Proyecto.pdf)

Guía de Configuración y Ejecución del Proyecto (Flask & Django)
Esta guía detalla los pasos necesarios para inicializar el entorno virtual, ejecutar el backend en Flask y poner en marcha la interfaz en Django.
Paso 1: Configuración del Entorno Virtual (.venv)
Es fundamental aislar las librerías del proyecto. Sigue estos comandos en tu terminal principal:
1.
Creación del entorno: Si es la primera vez que abres el proyecto, crea el entorno virtual ejecutando:
Bash
py -m venv .venv
2.
Activación: Para que el sistema reconozca las dependencias, activa el entorno con el siguiente comando:
Bash
.\.venv\Scripts\Activate
Nota: Sabrás que está activo porque aparecerá (.venv) al inicio de la línea de comandos.
Paso 2: Ejecución del Backend (Servidor Flask)
El backend gestiona los datos y debe estar activo para que la web funcione correctamente.
1.
Localización del proyecto: Abre una terminal y dirígete a la carpeta donde se encuentra el archivo backend.py. Si no estás en la ruta, usa:
Bash
cd "C:\Ruta\Hacia\Tu\Proyecto\pythonproyect6"
2.
Lanzamiento del servidor: Ejecuta el script principal de Flask:
Bash
python backend.py
Verificación: La terminal debe mostrar que el servidor está escuchando en http://127.0.0.1:5000.
Paso 3: Ejecución del Frontend (Servidor Django)
Sin cerrar la terminal anterior, necesitamos una nueva sesión para el servidor web.
1.
Nueva Terminal: Abre una segunda pestaña o ventana de terminal en tu editor.
2.
Navegación: Dirígete a la carpeta raíz de la aplicación Django (donde se encuentra el archivo manage.py):
Bash
cd "C:\Ruta\Hacia\Tu\Proyecto\django_views"
3.
Inicio de la Web: Ejecuta el servidor de desarrollo de Django con el comando:
Bash
python manage.py runserver
Paso 4: Acceso a la Aplicación
Una vez que ambas terminales estén en ejecución:
1.
Abre tu navegador de preferencia.
2.
Ingresa a la dirección local: http://127.0.0.1:8000
3.
Verifica que la página cargue correctamente y que los datos (provenientes del puerto 5000) se visualicen sin errores.
