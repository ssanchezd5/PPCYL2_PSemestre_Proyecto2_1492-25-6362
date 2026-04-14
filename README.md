[Documentaclon Proyecto2G7.pdf](https://github.com/user-attachments/files/26729993/Documentaclon.Proyecto2G7.pdf)

Universidad Mariano Gálvez de Guatemala
Ingeniera, matemática y ciencias físicas
Ingeniería eléctrica 
Programación para la Ciencia y la Ingeniería II
Ing. Carlos Alberto Arias López









Proyecto #2  










Grupo número 7
1492
Sección “A” vespertina
13/04/2026
Introducción
El presente proyecto consiste en el desarrollo de un sistema web orientado a la gestión de información académica, específicamente en el manejo y visualización de notas estudiantiles. Para su implementación se emplearon tecnologías modernas del entorno Python, destacando el uso de Django como framework principal para la construcción de la interfaz de usuario y Flask como componente encargado del procesamiento de datos.
El sistema se diseñó bajo un enfoque modular, permitiendo la separación de responsabilidades entre la capa de presentación y la lógica de procesamiento. Esta decisión arquitectónica facilita la escalabilidad del sistema, así como su mantenimiento y posible extensión futura. Asimismo, se incorpora el uso de archivos XML como medio de entrada de datos estructurados, los cuales son procesados y transformados en información útil para el usuario final.
Además, el desarrollo de este sistema permite evidenciar la aplicación práctica de conceptos fundamentales de ingeniería de software, tales como la separación de capas, la comunicación entre servicios y el uso de estructuras de datos para la optimización del rendimiento. De igual forma, se busca que el sistema no solo cumpla una función operativa, sino que también sirva como base para futuras mejoras, tales como la integración con bases de datos más complejas o la implementación de interfaces más interactivas.
Objetivos
i.	General
Desarrollar un sistema web que permita gestionar y visualizar notas mediante el uso de tecnologías backend y estructuras de datos eficientes.
ii.	Especlflcos
•	Implementar un API a través de lenguaje Python que pueda ser consumida utilizando el protocolo HTTP.
•	Utilizar el paradigma de programación orientada a objetos para construir software.
•	Utilizar bases de datos para almacenar información de forma persistente.
•	Utilizar archivos XML como insumos para la comunicación con el API desarrollado.
•	Utilizar expresiones regulares para extraer contenido de texto (utilizando estructuras de pilas).
Marco Teórico
A.	Django
Django es un framework web de alto nivel que permite el desarrollo rápido de aplicaciones robustas y seguras. Se basa en el patrón MTV (Model-Template-View), el cual separa la lógica de negocio, la presentación y el control de flujo. En este proyecto, Django se encarga de gestionar las vistas, manejar sesiones de usuario y renderizar las interfaces HTML.
Proporciona herramientas integradas para la gestión de usuarios, seguridad y manejo de formularios, lo que reduce significativamente el tiempo de desarrollo y minimiza errores comunes. Su estructura organizada permite mantener un código limpio y escalable, lo cual es fundamental en aplicaciones que pueden crecer en complejidad con el tiempo.
B.	Flask
Flask es un microframework ligero que permite construir servicios web de manera flexible. A diferencia de Django, Flask no impone una estructura rígida, lo que lo hace ideal para implementar microservicios. En el contexto del proyecto, Flask se utiliza como una API que recibe solicitudes HTTP desde Django, procesa archivos XML y devuelve resultados estructurados. Este tipo de interacción es común en arquitecturas modernas donde los sistemas se dividen en servicios independientes.
Otra ventaja importante de Flask es su capacidad de integrarse fácilmente con otras tecnologías, lo que lo convierte en una opción ideal para desarrollar APIs. En este proyecto, su uso permite aislar el procesamiento de datos, logrando que la lógica del sistema sea más clara y mantenible.
C.	 XML
El lenguaje XML (Extensible Markup Language) permite almacenar y transportar datos de forma estructurada. En el sistema desarrollado, el XML actúa como fuente de datos, conteniendo información como actividades, carnets y calificaciones, los cuales son posteriormente interpretados por el backend. 
El uso de XML en este contexto permite trabajar con datos provenientes de fuentes externas, lo cual es una práctica común en sistemas reales. Además, su estructura jerárquica facilita la organización de la información, permitiendo una lectura ordenada y lógica de los datos.
D.	Matriz Dispersa
Una matriz dispersa es una estructura de datos que almacena únicamente los valores distintos de cero o relevantes, optimizando el uso de memoria. En este proyecto, se utiliza para representar la relación entre estudiantes, actividades y notas, evitando almacenar información redundante. una matriz dispersa permite registrar únicamente las celdas que sí tienen datos, ignorando las vacías.
El funcionamiento de esta estructura consiste en ir registrando cada dato como un “nodo” o elemento individual dentro de una lista. Posteriormente, estos datos pueden recorrerse, organizarse o agruparse para realizar cálculos, como promedios por actividad o listados de mejores notas.
La principal ventaja de este enfoque es la optimización de recursos, ya que se reduce el uso de memoria y se mejora la eficiencia al trabajar únicamente con información útil. Además, proporciona flexibilidad para manejar datos que pueden crecer o cambiar con el tiempo.
No obstante, también presenta una limitación importante: al no estar organizada como una tabla completa, encontrar un dato específico puede requerir revisar varios elementos, lo que puede ser menos rápido en comparación con otras estructuras más rígidas.
 Arquitectura del Sistema
1.	El usuario interactúa con la interfaz desarrollada en Django.
2.	Se carga un archivo XML mediante un formulario web.
3.	Django recibe el archivo y lo envía mediante una solicitud HTTP POST al servidor Flask.
4.	Flask procesa el XML, extrae los datos y los organiza en estructuras internas.
5.	Los datos procesados se devuelven en formato JSON.
6.	Django recibe la respuesta y la presenta al usuario en forma de tabla.
7.	Este modelo sigue el principio de separación de responsabilidades, donde Django actúa como cliente y Flask como proveedor de servicios.
Este tipo de arquitectura también favorece la independencia entre componentes, lo que significa que cada parte del sistema puede ser modificada o mejorada sin afectar directamente a las demás. Por ejemplo, el módulo de procesamiento en Flask podría ser reemplazado por otro servicio más avanzado sin necesidad de cambiar la interfaz desarrollada en Django.
IMPLEMENTACIÓN
Este enfoque basado en servicios permite simular el funcionamiento de aplicaciones reales en la industria, donde múltiples sistemas interactúan entre sí a través de redes. Además, facilita la depuración de errores, ya que cada componente puede ser probado de manera independiente
•	Comunicación entre Django y Flask
La comunicación se realiza mediante solicitudes HTTP, específicamente utilizando el método POST para enviar archivos. Esto simula el comportamiento de una API REST, donde un cliente consume servicios proporcionados por otro servidor.
Esto demuestra la integración entre dos sistemas independientes dentro de una misma solución.
•	Procesamiento del XML
El archivo XML es interpretado utilizando librerías de Python, permitiendo recorrer cada nodo y extraer atributos relevantes. Cada elemento representa una relación entre actividad, estudiante y nota.
Durante este proceso, es importante validar la estructura del archivo XML para evitar errores en la interpretación de los datos. Una estructura mal definida podría generar inconsistencias en la información procesada, afectando los resultados finales del sistema.
•	Uso de la Matriz Dispersa
Los datos obtenidos del XML se almacenan en una estructura tipo lista enlazada (simulación de matriz dispersa), donde cada nodo contiene:
Actividad (fila)
Carnet (columna)
Nota (valor)
Esto permite realizar operaciones como:
cálculo de promedios
ordenamiento de notas
consultas por actividad
•	Manejo de Usuarios
El sistema implementa autenticación básica con roles:
Maestro → puede subir XML y gestionar datos
Alumno → puede visualizar información
Esto se maneja mediante sesiones en Django.
La implementación de roles dentro del sistema permite restringir el acceso a ciertas funcionalidades, garantizando así un mayor control sobre la información. Esto es fundamental en sistemas académicos, donde los datos deben ser manejados de manera segura y organizada.
RESULTADOS
El sistema desarrollado cumple con los objetivos planteados, permitiendo la carga, procesamiento y visualización de datos académicos de manera eficiente. Se logró una correcta integración entre Django y Flask, evidenciando la viabilidad de arquitecturas distribuidas en aplicaciones web.
Asimismo, la implementación de estructuras de datos como la matriz dispersa permitió optimizar el manejo de información, facilitando consultas rápidas y reduciendo redundancia.
Uno de los aspectos más relevantes del proyecto es la separación entre la capa de presentación y la lógica de procesamiento. Este enfoque no solo mejora la organización del código, sino que también permite escalar el sistema en el futuro, por ejemplo, reemplazando Flask por otro servicio más robusto o integrando bases de datos avanzadas.

CONCLUSIONES
El desarrollo del sistema permitió aplicar conceptos fundamentales de ingeniería de software, incluyendo arquitectura cliente-servidor, manejo de estructuras de datos y comunicación entre servicios. La combinación de Django y Flask demostró ser una solución efectiva para separar responsabilidades dentro de una aplicación web.
Finalmente, el uso de la matriz dispersa evidenció la importancia de seleccionar estructuras de datos adecuadas para optimizar el rendimiento y la eficiencia del sistema.

