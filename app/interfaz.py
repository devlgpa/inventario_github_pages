import tkinter as tk
from tkinter import ttk, messagebox
from app.datos import cargar_datos, guardar_datos
from app.html import generar_html

ESTADOS = ["Disponible", "Bajo", "Agotado"]
inventario = cargar_datos()

def iniciar_interfaz():
    def actualizar_lista():
        for widget in contenedor.winfo_children():
            widget.destroy()

        for index, item in enumerate(inventario):
            fila = tk.Frame(contenedor)
            fila.pack(fill="x", pady=2, padx=5)

            texto = f"{item['Producto']} - {item['Estado']}"
            lbl = tk.Label(fila, text=texto, anchor="w")
            lbl.pack(side="left", fill="x", expand=True)

            btn = tk.Button(fila, text="⋮")
            btn.config(command=lambda idx=index, b=btn: mostrar_menu(idx, b))

            btn.pack(side="right")

    def mostrar_menu(index, boton):
        menu = tk.Menu(ventana, tearoff=0)
        for estado in ESTADOS:
            menu.add_command(label=f"Marcar como {estado}",
                             command=lambda e=estado: cambiar_estado(index, e))
        menu.add_separator()
        menu.add_command(label="❌ Eliminar",
                         command=lambda: eliminar_producto(index))

        # Mostrar el menú junto al botón
        x = boton.winfo_rootx()
        y = boton.winfo_rooty() + boton.winfo_height()
        menu.tk_popup(x, y)
        menu.grab_release()

    def cambiar_estado(index, nuevo_estado):
        inventario[index]["Estado"] = nuevo_estado
        guardar_datos(inventario)
        generar_html(inventario)
        actualizar_lista()

    def eliminar_producto(index):
        nombre = inventario[index]["Producto"]
        if messagebox.askyesno("Eliminar", f"¿Eliminar '{nombre}' del inventario?"):
            inventario.pop(index)
            guardar_datos(inventario)
            generar_html(inventario)
            actualizar_lista()

    def agregar():
        nombre = entrada.get().strip()
        estado = combo_estado.get()
        if nombre:
            inventario.append({"Producto": nombre, "Estado": estado})
            guardar_datos(inventario)
            generar_html(inventario)
            entrada.delete(0, tk.END)
            actualizar_lista()

    # --- VENTANA PRINCIPAL ---
    global ventana
    ventana = tk.Tk()
    ventana.title("Control de Stock")
    ventana.geometry("420x450")

    tk.Label(ventana, text="Producto:").pack()
    entrada = tk.Entry(ventana)
    entrada.pack(pady=5)

    tk.Label(ventana, text="Estado:").pack()
    combo_estado = ttk.Combobox(ventana, values=ESTADOS, state="readonly")
    combo_estado.set(ESTADOS[0])
    combo_estado.pack(pady=5)

    tk.Button(ventana, text="Agregar", command=agregar).pack(pady=5)

    # Contenedor de productos con botones
    contenedor = tk.Frame(ventana)
    contenedor.pack(fill="both", expand=True, padx=10, pady=10)

    actualizar_lista()
    ventana.mainloop()
