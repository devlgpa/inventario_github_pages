import tkinter as tk
from tkinter import ttk
from app.datos import cargar_datos, guardar_datos
from app.html import generar_html

ESTADOS = ["Disponible", "Bajo", "Agotado"]
inventario = cargar_datos()

def iniciar_interfaz():
    def agregar():
        nombre = entrada.get().strip()
        estado = estado_var.get()
        if nombre:
            inventario.append({"Producto": nombre, "Estado": estado})
            guardar_datos(inventario)
            generar_html(inventario)
            entrada.delete(0, tk.END)
            actualizar_lista()

    def actualizar_lista():
        lista.delete(0, tk.END)
        for item in inventario:
            lista.insert(tk.END, f"{item['Producto']} - {item['Estado']}")

    ventana = tk.Tk()
    ventana.title("Control de Stock")
    ventana.geometry("400x350")

    entrada = tk.Entry(ventana)
    entrada.pack(pady=5)

    estado_var = tk.StringVar(value=ESTADOS[0])
    ttk.Combobox(ventana, textvariable=estado_var, values=ESTADOS, state="readonly").pack(pady=5)

    tk.Button(ventana, text="Agregar", command=agregar).pack(pady=5)

    lista = tk.Listbox(ventana)
    lista.pack(fill=tk.BOTH, expand=True)

    actualizar_lista()
    ventana.mainloop()
