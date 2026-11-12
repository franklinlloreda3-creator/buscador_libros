import requests
 
API_URL = "https://openlibrary.org/search.json"
CABECERAS = {"User-Agent": "BuscadorLibrosADSO (delia.herazot@campusucc.edu.co)"}
CAMPOS = "key,title,author_name,first_publish_year,cover_i"
 
 
class ErrorDeApi(Exception):
    """La API externa no respondió como se esperaba."""
 
 
def buscar_libros(texto, limite=10):
    """Busca libros y devuelve una lista de diccionarios sencillos."""
    parametros = {"q": texto, "limit": limite, "fields": CAMPOS}
 
    try:
        respuesta = requests.get(
            API_URL, params=parametros, headers=CABECERAS, timeout=10
        )
        respuesta.raise_for_status()
        datos = respuesta.json()
    except requests.exceptions.Timeout as error:
        raise ErrorDeApi(
            "La consulta tardó demasiado. Intenta nuevamente."
        ) from error
    except requests.exceptions.HTTPError as error:
        raise ErrorDeApi(
            "La API respondió con un error HTTP."
        ) from error
    except requests.exceptions.JSONDecodeError as error:
        raise ErrorDeApi(
            "La API devolvió una respuesta no válida."
        ) from error
    except requests.exceptions.RequestException as error:
        raise ErrorDeApi(
            "No fue posible conectar con la API."
        ) from error
 
    libros = []
    for doc in datos.get("docs", []):
        autores = doc.get("author_name") or []
        libros.append({
            "titulo": doc.get("title", "Sin título"),
            "autor": autores[0] if autores else "Autor desconocido",
            "anio": doc.get("first_publish_year", "No disponible"),
            "portada": doc.get("cover_i"),
            "clave": doc.get("key", ""),
        })
    return libros
