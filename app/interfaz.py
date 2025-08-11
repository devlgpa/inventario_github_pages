import tkinter as tk
import subprocess
from tkinter import ttk, messagebox
from datetime import datetime
from app.datos import cargar_datos, guardar_datos
from app.html import generar_html

ESTADOS = ["Disponible", "Bajo", "Agotado"]
inventario = cargar_datos()

def push_a_github():
    try:
        ahora = datetime.now().strftime("%d/%m %H:%M")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Actualización inventario {ahora}"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)  # Cambia 'main' si usas otro nombre
        messagebox.showinfo("GitHub", "Inventario subido correctamente a GitHub.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error GitHub", f"No se pudo subir a GitHub:\n{e}")


def iniciar_interfaz():
    def actualizar_lista():
        for widget in contenedor.winfo_children():
            widget.destroy()

        # Crear tres columnas para cada estado
        frames_columnas = {}
        for estado in ESTADOS:
            frame_col = tk.Frame(contenedor)
            frame_col.pack(side="left", fill="both", expand=True, padx=5)
            tk.Label(frame_col, text=estado, font=("Arial", 10, "bold")).pack(pady=(0, 5))
            frames_columnas[estado] = frame_col

        for index, item in enumerate(inventario):
            estado = item["Estado"]
            frame_col = frames_columnas[estado]
            fila = tk.Frame(frame_col)
            fila.pack(fill="x", pady=2, padx=2)

            texto = item['Producto']
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
        # Validación: nombre vacío o duplicado
        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre del producto no puede estar vacío.")
            return
        if any(item["Producto"].lower() == nombre.lower() for item in inventario):
            messagebox.showwarning("Advertencia", f"El producto '{nombre}' ya existe en el inventario.")
            return
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
    ventana.minsize(420, 450)

    # Contenedor horizontal para producto, estado y botón agregar
    fila_entrada = tk.Frame(ventana)
    fila_entrada.pack(pady=10, padx=10, fill="x")

    tk.Label(fila_entrada, text="Producto:").pack(side="left")

    entrada = tk.Entry(fila_entrada)
    entrada.pack(side="left", padx=(5, 10))

    tk.Label(fila_entrada, text="Estado:").pack(side="left")

    combo_estado = ttk.Combobox(fila_entrada, values=ESTADOS, state="readonly", width=12)
    combo_estado.set(ESTADOS[0])
    combo_estado.pack(side="left", padx=(5, 10))

    boton_agregar = tk.Button(fila_entrada, text="Agregar", command=agregar)
    boton_agregar.pack(side="left")

    # Botón para subir a GitHub
    tk.Button(ventana, text="Subir a GitHub", command=push_a_github, background="gray64").pack(pady=10)

    # Contenedor de productos con botones
    titulo = tk.Label(ventana, text="Inventario de Productos", font=("Arial", 12, "bold"))
    titulo.pack(pady=10)

    contenedor = tk.Frame(ventana)
    contenedor.pack(fill="both", expand=True, padx=10, pady=10)

    actualizar_lista()
    ventana.mainloop()