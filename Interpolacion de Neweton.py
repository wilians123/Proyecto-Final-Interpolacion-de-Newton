# Autor: [WILLIANS NAVAS]
# Carne: [0909-21-11752]
# Descripción: Este script realiza la interpolación de Newton utilizando valores de entrada proporcionados por el usuario,
# calcula las diferencias divididas, construye el polinomio de interpolación, evalúa el polinomio en los puntos dados
# y muestra los resultados en una interfaz gráfica con Tkinter y Matplotlib.

from tkinter import *  # Importa la librería Tkinter para crear la interfaz gráfica
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Importa el backend de Matplotlib para incrustar gráficos en Tkinter
import matplotlib.pyplot as plt  # Importa Matplotlib para generar gráficos
from tabulate import tabulate  # Importa tabulate para formatear tablas en texto

# Función para calcular diferencias divididas
def calcular_diferencias_divididas(x, y):
    n = len(x)
    diferencias = []
    for i in range(n):
        diferencias.append(y[i])
    
    for j in range(1, n):
        for i in range(n-1, j-1, -1):
            diferencias[i] = (diferencias[i] - diferencias[i-1]) / (x[i] - x[i-j])
    return diferencias

# Función para construir el polinomio de interpolación de Newton
def construir_polinomio(x, diferencias):
    polinomio = "{:.3f}".format(diferencias[0])
    n = len(x)
    for i in range(1, n):
        termino = "{:.3f}".format(diferencias[i])
        for j in range(i):
            if j == 0:
                termino += " * (x - {:.2f})".format(x[j])
            else:
                termino += " * (x - {:.2f})".format(x[j])
        polinomio += " + " + termino
    return polinomio

# Función para evaluar el polinomio en los puntos x
def evaluar_polinomio(polinomio, x):
    resultado = []
    for valor in x:
        res = eval(polinomio.replace('x', str(valor)))
        resultado.append(res)
    return resultado

# Función para mostrar los resultados en una nueva ventana
def mostrar_resultados(x, y):
    diferencias = calcular_diferencias_divididas(x, y)
    polinomio = construir_polinomio(x, diferencias)
    resultados = evaluar_polinomio(polinomio, x)
    errores = [abs(resultados[i] - y[i]) for i in range(len(x))]  # Calcula el error absoluto

    # Crea la ventana principal
    root = Tk()
    root.title("Resultados de Interpolación de Newton")

    # Crea un marco para los resultados
    resultados_frame = Frame(root)
    resultados_frame.pack()

    # Muestra la tabla de valores
    tabla_valores_label = Label(resultados_frame, text="TABLA DE VALORES", font=("Arial", 14, "bold"))
    tabla_valores_label.pack()
    tabla_valores_text = Label(resultados_frame, text=tabulate([(i, x[i], y[i]) for i in range(len(x))], headers=["j", "xj", "f(xj)"], tablefmt="grid"), font=("Courier", 12))
    tabla_valores_text.pack()

    # Muestra las iteraciones
    calculos_label = Label(resultados_frame, text="\nITERACIONES", font=("Arial", 14, "bold"))
    calculos_label.pack()
    f_x0_x1_label = Label(resultados_frame, text="f(x0, x1) = {:.5f}".format((y[1] - y[0]) / (x[1] - x[0])), font=("Arial", 12))
    f_x0_x1_label.pack()
    f_x1_x2_label = Label(resultados_frame, text="f(x1, x2) = {:.5f}".format((y[2] - y[1]) / (x[2] - x[1])), font=("Arial", 12))
    f_x1_x2_label.pack()
    f_x0_x1_x2_label = Label(resultados_frame, text="f(x0, x1, x2) = {:.5f}".format(((y[2] - y[1]) / (x[2] - x[1]) - (y[1] - y[0]) / (x[1] - x[0])) / (x[2] - x[0])), font=("Arial", 12))
    f_x0_x1_x2_label.pack()

    # Mostrar el polinomio
    polinomio_label = Label(resultados_frame, text="\nPOLINOMIO DE INTERPOLACION DE NEWTON", font=("Arial", 14, "bold"))
    polinomio_label.pack()
    polinomio_text = Label(resultados_frame, text="f(x) = " + polinomio, font=("Arial", 12))
    polinomio_text.pack()

    # Mostrar la comprobación con errores
    comprobacion_label = Label(resultados_frame, text="\nCOMPROBACION", font=("Arial", 14, "bold"))
    comprobacion_label.pack()
    for i in range(len(x)):
        comprobacion_text = Label(resultados_frame, text="f({}) = {:.5f}  (y = {},  Error = {:.5f})".format(x[i], resultados[i], y[i], errores[i]), font=("Arial", 12))
        comprobacion_text.pack()

    # Crear la figura para mostrar la gráfica
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    ax.plot(x, y, marker='o', color='red', linestyle='-', markersize=8, markerfacecolor='red')  # Puntos rojos
    ax.plot(x, y, color='blue', linestyle='-')  # Líneas azules
    ax.set_title('\nGRAFICA DEL POLINOMIO DE INTERPOLACION DE NEWTON', fontsize=14)
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.grid(True)

    # Anotar las coordenadas de cada punto
    for i in range(len(x)):
        ax.annotate(f'({x[i]}, {y[i]})', (x[i], y[i]), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=10)

    # Mostrar la gráfica en el marco de resultados
    canvas = FigureCanvasTkAgg(fig, master=resultados_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=1)

    # Iniciar el bucle principal de la interfaz gráfica
    root.mainloop()

# Función para ingresar valores de x y y
def ingresar_valores():
    def obtener_valores():
        # Obtener los valores ingresados y convertirlos a listas de floats
        x_valores = list(map(float, x_entry.get().split(',')))
        y_valores = list(map(float, y_entry.get().split(',')))
        ventana_ingreso.destroy()  # Cerrar la ventana de ingreso de valores
        mostrar_resultados(x_valores, y_valores)  # Mostrar resultados con los valores ingresados

    # Crear una ventana para ingresar los valores
    ventana_ingreso = Tk()
    ventana_ingreso.title("Ingresar valores")

    # Etiqueta y campo de entrada para los valores de x
    Label(ventana_ingreso, text="Ingrese los valores de x (separados por comas):", font=("Arial", 12)).pack()
    x_entry = Entry(ventana_ingreso, font=("Arial", 12))
    x_entry.pack()

    # Etiqueta y campo de entrada para los valores de y
    Label(ventana_ingreso, text="Ingrese los valores de y (separados por comas):", font=("Arial", 12)).pack()
    y_entry = Entry(ventana_ingreso, font=("Arial", 12))
    y_entry.pack()

    # Botón para enviar los valores ingresados
    Button(ventana_ingreso, text="Enviar", command=obtener_valores, font=("Arial", 12)).pack()

    ventana_ingreso.mainloop()  # Iniciar el bucle principal de la ventana de ingreso de valores

# Llamar a la función para ingresar valores al iniciar el programa
ingresar_valores()
