import os

RUTA_HTML = os.path.join("docs", "index.html")
ESTADOS = ["Disponible", "Bajo", "Agotado"]

def generar_html(inventario):
    grupos = {e: [] for e in ESTADOS}
    for item in inventario:
        grupos[item["Estado"]].append(item["Producto"])

    with open(RUTA_HTML, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
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
""")

        for estado, emoji in zip(ESTADOS, ["🟢", "🟡", "🔴"]):
            clase = "" if estado == "Disponible" else "poco" if estado == "Bajo" else "agotado"
            f.write(f'    <div class="categoria">\n')
            f.write(f'      <h2>{emoji} Stock {estado.lower()}</h2>\n')
            f.write('      <ul>\n')
            for producto in grupos[estado]:
                clase_li = f' class="{clase}"' if clase else ""
                f.write(f'        <li{clase_li}>{producto}</li>\n')
            f.write('      </ul>\n')
            f.write('    </div>\n')

        f.write("""  </div>

  <script>
    const categorias = document.querySelectorAll('.categoria');
    categorias.forEach(categoria => {
      const titulo = categoria.querySelector('h2');
      titulo.addEventListener('click', () => {
        categoria.classList.toggle('activa');
      });
    });
  </script>

</body>
</html>
""")
