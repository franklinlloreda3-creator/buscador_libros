import requests
 
API_URL = "https://openlibrary.org/search.json"
CABECERAS = {"User-Agent": "BuscadorLibrosADSO (Franklinlloreda0@gmail.com)"}
CAMPOS = "key,title,author_name,first_publish_year,cover_i,ebook_access,ia"
 
 
class ErrorDeApi(Exception):
    """La API externa no respondió como se esperaba."""
 
 
def buscar_libros(texto, limite=12, solo_leibles=False):
    """Busca libros y devuelve una lista de diccionarios sencillos.

    Si solo_leibles es True, devuelve solo los que tienen versión digital.
    """
    # Si se filtra por leíbles, se piden más resultados para no quedar vacíos
    pedir = 60 if solo_leibles else limite
    parametros = {"q": texto, "limit": pedir, "fields": CAMPOS}
 
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
        lectura = _enlace_de_lectura(doc)
        if solo_leibles and not lectura:
            continue
        libros.append({
            "titulo": doc.get("title", "Sin título"),
            "autor": autores[0] if autores else "Autor desconocido",
            "anio": doc.get("first_publish_year", "No disponible"),
            "portada": doc.get("cover_i"),
            "clave": doc.get("key", ""),
            "lectura": lectura,
        })
    return libros[:limite]


def _enlace_de_lectura(doc):
    """Devuelve el enlace para leer el libro en Internet Archive, o None.

    ebook_access: "public" = se lee libre; "borrowable" = se pide prestado
    gratis con una cuenta de Internet Archive; otros valores = no hay ebook.
    """
    acceso = doc.get("ebook_access", "no_ebook")
    ids = doc.get("ia") or []
    if not ids or acceso not in ("public", "borrowable"):
        return None
    return {
        "url": f"https://archive.org/details/{ids[0]}",
        "libre": acceso == "public",
    }
