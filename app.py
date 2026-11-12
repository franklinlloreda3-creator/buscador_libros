import os

from flask import Flask, render_template, request
 
from open_library import ErrorDeApi, buscar_libros
 
app = Flask(__name__)
 
 
@app.route("/")
def inicio():
    busqueda = request.args.get("q", "").strip()
    solo_leibles = request.args.get("leibles") == "1"
    libros = []
    mensaje = ""
 
    if busqueda:
        try:
            libros = buscar_libros(busqueda, solo_leibles=solo_leibles)
            if not libros:
                mensaje = (
                    "No se encontraron libros que se puedan leer en línea."
                    if solo_leibles
                    else "No se encontraron libros para esa búsqueda."
                )
        except ErrorDeApi as error:
            mensaje = str(error)
 
    return render_template(
        "index.html",
        libros=libros,
        busqueda=busqueda,
        mensaje=mensaje,
        solo_leibles=solo_leibles,
    )
 
 
if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
