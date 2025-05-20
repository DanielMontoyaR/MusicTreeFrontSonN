import random
import string

# --- Generación de genre_id compatible con tu esquema ---
def generar_codigo(length=12):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generar_genre_id(es_subgenero):
    genero_id = "G-" + generar_codigo()
    sub_id = "S-000000000000" if es_subgenero else "S-" + generar_codigo()
    return f"{genero_id}{sub_id}"