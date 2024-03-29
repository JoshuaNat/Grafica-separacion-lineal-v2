import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
     FigureCanvasTkAgg)
import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np

#Variable global para almacenar las coordenadas
Xs = []

def leer_archivo():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Archivo de coordenadas",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
    
    try:
        with open(filename) as f:
            for linea in f:
                coords = linea.split(",")
                if (len(coords)==2):
                    if (is_float(coords[0]) and is_float(coords[1])):
                        x = float(coords[0])
                        y = float(coords[1])
                        agregar_elementos(x, y)
                    else:
                        continue
                else:
                    continue
    except IOError:
        messagebox.showerror("Error al abrir el archivo")

def agregar_elementos(coord_x, coord_y):
    Xs.append([1, coord_x, coord_y])
    plt.plot(coord_x, coord_y, "ok")
    canvas.draw()

def graficar_linea():
    texto1 = peso_1.get("1.0", "end-1c")
    texto2 = peso_2.get("1.0", "end-1c")
    texto3 = bias.get("1.0", "end-1c")

    if (is_float(texto1) and is_float(texto2) and is_float(texto3)):
        crear_grafica()

        w1 = float(texto1)
        w2 = float(texto2)
        b = float(texto3)

        m = -w1/w2
        c = -b/w2

        plt.axline((0,c), slope=m, linewidth = 4)
        canvas.draw()
        prod_p(w1, w2, b)
    
    else:
        messagebox.showerror("Valor invalido", "Todos los valores deben ser numeros flotantes")
        


def prod_p(p1, p2, b):
    if Xs:
        W = np.array([b, p1, p2])
        X = np.array(Xs)
        y = np.dot(W, X.T) >= 0
        
        for i in range(len(y)):
            if (y[i] == 0):
                plt.plot(X[i][1], X[i][2], 'or')
            else:
                plt.plot(X[i][1], X[i][2], 'ob')
    
    canvas.draw()

def crear_grafica():
    plt.clf()
    plt.title("Practica 1")
    plt.grid("on")
    plt.xlim([-2,2])
    plt.ylim([-2,2])
    plt.xlabel(r"x1")
    plt.ylabel(r"x2")
    plt.draw()

def limpiar():
    ms1 = "W1"
    ms2 = "W2"
    ms3 = "Bias"
    Xs.clear()
    peso_1.delete("1.0", "end-1c")
    peso_1.insert(tk.END, ms1)
    peso_2.delete("1.0", "end-1c")
    peso_2.insert(tk.END, ms2)
    bias.delete("1.0", "end-1c")
    bias.insert(tk.END, ms3)
    crear_grafica()

def is_float(numero):
    try:
        float(numero)
        return(True)
    except:
        return False


# Initialize Tkinter and Matplotlib Figure
root = tk.Tk()
fig, ax = plt.subplots()
 
# Tkinter Application
frame = tk.Frame(root)
frame.pack()

#Creaciones de texto
peso_1 = tk.Text(root, height = 1, width = 15)
peso_2 = tk.Text(root, height = 1, width = 15)
bias = tk.Text(root, height = 1, width = 15)
ms1 = "W1"
ms2 = "W2"
ms3 = "Bias"
peso_1.pack()
peso_1.insert(tk.END, ms1)
peso_2.pack()
peso_2.insert(tk.END, ms2)
bias.pack()
bias.insert(tk.END, ms3)

#Creación del boton
graficar = tk.Button(root, height=2, width=15, text="Graficar", command=lambda:graficar_linea())
graficar.pack()
resetear = tk.Button(root, height=2, width=15, text="Reiniciar", command=lambda:limpiar())
resetear.pack()
leer = tk.Button(root, height=2, width=15, text="Buscar archivo", command=lambda:leer_archivo())
leer.pack()
 
# Create Canvas
canvas = FigureCanvasTkAgg(fig, master=root)  
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
 
# Plot data on Matplotlib Figure
t = np.arange(0, 2*np.pi, .01)
crear_grafica()
canvas.draw()
 
root.mainloop()