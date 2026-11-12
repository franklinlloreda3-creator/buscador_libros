# Buscador de libros

App web hecha con Flask que busca libros en la API de [Open Library](https://openlibrary.org/developers/api):
muestra portada, título, autor, año y un enlace a la ficha del libro.

## Cómo ejecutarlo en tu computador

Necesitas tener [Python 3](https://www.python.org/downloads/) instalado.

```bash
# 1. Descargar el proyecto
git clone https://github.com/TU_USUARIO/buscador_libros.git
cd buscador_libros

# 2. Crear y activar el entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac / Linux

# 3. Instalar las dependencias
pip install -r requirements.txt

# 4. Ejecutar
python app.py
```

Abre en el navegador: http://127.0.0.1:5000

## Estructura

- `app.py`: rutas de Flask
- `open_library.py`: consulta a la API de Open Library
- `templates/index.html`: página principal
- `static/estilos.css`: estilos
