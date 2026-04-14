from django.urls import path
from .views import (
    login_view, subir_xml, alumno_view, admin_panel,
    crear_usuario_view, eliminar_usuario_view, cerrar_sesion
)

urlpatterns = [
    path('', login_view, name='login'),
    path('subir/', subir_xml, name='subir'),
    path('alumno/', alumno_view, name='alumno'),
    path('admin_panel/', admin_panel, name='admin_panel'),
    path('crear_usuario/', crear_usuario_view, name='crear_usuario'),
    path('eliminar_usuario/', eliminar_usuario_view, name='eliminar_usuario'),
    path('logout/', cerrar_sesion, name='logout'),
]