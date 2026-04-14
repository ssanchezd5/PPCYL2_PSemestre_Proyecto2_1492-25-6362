class Nodo:
    def __init__(self, actividad, estudiante, nota):
        self.actividad = actividad   # fila
        self.estudiante = estudiante # columna
        self.nota = int(nota)

        self.derecha = None
        self.abajo = None


class MatrizDispersa:
    def __init__(self):
        self.filas = {}      # actividades
        self.columnas = {}   # estudiantes

    def insertar(self, actividad, estudiante, nota):
        nota = int(nota)

        # Validación (IMPORTANTE para el proyecto)
        if nota < 0 or nota > 100:
            return

        nuevo = Nodo(actividad, estudiante, nota)

        # 🔹 Insertar en fila
        if actividad not in self.filas:
            self.filas[actividad] = nuevo
        else:
            temp = self.filas[actividad]
            while temp.derecha:
                temp = temp.derecha
            temp.derecha = nuevo

        # 🔹 Insertar en columna
        if estudiante not in self.columnas:
            self.columnas[estudiante] = nuevo
        else:
            temp = self.columnas[estudiante]
            while temp.abajo:
                temp = temp.abajo
            temp.abajo = nuevo

    def recorrer(self):
        datos = []
        for actividad in self.filas:
            temp = self.filas[actividad]
            while temp:
                datos.append({
                    "actividad": temp.actividad,
                    "estudiante": temp.estudiante,
                    "nota": temp.nota
                })
                temp = temp.derecha
        return datos

    def generar_graphviz(self):
        dot = "digraph G {\nnode [shape=box];\n"

        for actividad in self.filas:
            temp = self.filas[actividad]
            while temp:
                nombre = f"{temp.actividad}_{temp.estudiante}"
                dot += f'"{nombre}" [label="{temp.actividad}\\n{temp.estudiante}\\n{temp.nota}"];\n'

                if temp.derecha:
                    derecha = f"{temp.derecha.actividad}_{temp.derecha.estudiante}"
                    dot += f'"{nombre}" -> "{derecha}" [dir=both];\n'

                if temp.abajo:
                    abajo = f"{temp.abajo.actividad}_{temp.abajo.estudiante}"
                    dot += f'"{nombre}" -> "{abajo}" [dir=both];\n'

                temp = temp.derecha

        dot += "}"

        with open("matriz.dot", "w") as f:
            f.write(dot)