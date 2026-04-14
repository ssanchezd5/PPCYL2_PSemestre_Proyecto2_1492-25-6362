from backend import app

if __name__ == '__main__':
    print("Iniciando Servidor AcadNet UMG...")
    # Esto enciende el servidor en el puerto 5000
    app.run(debug=True, port=5000)