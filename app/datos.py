import csv, os

RUTA_CSV = os.path.join("docs", "datos.csv")

def cargar_datos():
    datos = []
    if os.path.exists(RUTA_CSV):
        with open(RUTA_CSV, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            datos.extend(reader)
    return datos

def guardar_datos(inventario):
    with open(RUTA_CSV, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Producto", "Estado"])
        writer.writeheader()
        writer.writerows(inventario)
