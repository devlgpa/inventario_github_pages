import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

RUTA_CSV = os.path.join("docs", "datos.csv")

# Estados permitidos
estados = ["Disponible", "Bajo", "Agotado"]

# Lista del inventario
inventario = []

def cargar_csv():
    if os.path.exists(RUTA_CSV):
        with open(RUTA_CSV, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            inventario.clear()
            for row in reader:
                inventario.append(row)

def guardar_csv():
    with open(RUTA_CSV, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Producto", "Estado"])
        writer.writeheader()
        for item in inventario:
            writer.writerow(item)

def agregar_producto():
    nombre = entrada_nombre.get().strip()
    estado = estado_var.get()

    if not nombre:
        messagebox.showerror("Error", "El nombre del producto no puede estar vacío.")
        return

    inventario.append({
        "Producto": nombre,
        "Estado": estado
    })

    guardar_csv()
    actualizar_lista()
    entrada_nombre.delete(0, tk.END)

def actualizar_lista():
    lista.delete(0, tk.END)
    for item in inventario:
        lista.insert(tk.END, f"{item['Producto']} - {item['Estado']}")

# GUI
ventana = tk.Tk()
ventana.title("Control de Stock")
ventana.geometry("400x350")

tk.Label(ventana, text="Producto:").pack()
entrada_nombre = tk.Entry(ventana)
entrada_nombre.pack()

tk.Label(ventana, text="Estado del stock:").pack()
estado_var = tk.StringVar()
estado_var.set(estados[0])
combo_estado = ttk.Combobox(ventana, textvariable=estado_var, values=estados, state="readonly")
combo_estado.pack()

tk.Button(ventana, text="Agregar", command=agregar_producto).pack(pady=10)

tk.Label(ventana, text="Inventario actual:").pack()
lista = tk.Listbox(ventana)
lista.pack(fill=tk.BOTH, expand=True)

cargar_csv()
actualizar_lista()

def generar_html():
    html_path = os.path.join("docs", "index.html")

    # Clasificar productos
    categorias = {"Disponible": [], "Bajo": [], "Agotado": []}
    for item in inventario:
        estado = item["Estado"]
        nombre = item["Producto"]
        if estado in categorias:
            categorias[estado].append(nombre)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Inventario</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <h1>Inventario</h1>

  <div class="contenedor">
    <div class="categoria">
      <h2>🟢 Stock disponible</h2>
      <ul>
        {''.join(f'<li>{x}</li>' for x in categorias["Disponible"])}
      </ul>
    </div>

    <div class="categoria">
      <h2>🟡 Stock bajo</h2>
      <ul>
        {''.join(f'<li class="poco">{x}</li>' for x in categorias["Bajo"])}
      </ul>
    </div>

    <div class="categoria">
      <h2>🔴 Sin stock</h2>
      <ul>
        {''.join(f'<li class="agotado">{x}</li>' for x in categorias["Agotado"])}
      </ul>
    </div>
  </div>

  <script>
    const categorias = document.querySelectorAll('.categoria');
    categorias.forEach(categoria => {{
      const titulo = categoria.querySelector('h2');
      titulo.addEventListener('click', () => {{
        categoria.classList.toggle('activa');
      }});
    }});
  </script>
</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ HTML actualizado al cerrar.")

# Esta función se ejecutará al cerrar la ventana
def al_cerrar():
    guardar_csv()
    generar_html()
    ventana.destroy()

# Asociar el evento de cerrar ventana
ventana.protocol("WM_DELETE_WINDOW", al_cerrar)


ventana.mainloop()
