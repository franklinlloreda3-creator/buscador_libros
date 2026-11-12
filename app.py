import os

from flask import Flask, render_template, request
 
from open_library import ErrorDeApi, buscar_libros
 
app = Flask(__name__)
 
 
@app.route("/")
def inicio():
    busqueda = request.args.get("q", "").strip()
    libros = []
    mensaje = ""
 
    if busqueda:
        try:
            libros = buscar_libros(busqueda)
            if not libros:
                mensaje = "No se encontraron libros para esa búsqueda."
        except ErrorDeApi as error:
            mensaje = str(error)
 
    return render_template(
        "index.html", libros=libros, busqueda=busqueda, mensaje=mensaje
    )
 
 
if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
