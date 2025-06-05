import os
import json
from datetime import datetime
import traceback
from utils.database.database import db
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from utils.models.models import Genre
from sqlalchemy import func, text
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, BOOLEAN
from sqlalchemy import Numeric as DECIMAL
from utils.queries.Genre.crear_genero import *

def procesar_generos_batch(generos, carpeta_destino="API/jsonprocesados"):
    os.makedirs(carpeta_destino, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_filename = f"{timestamp}_generos.json"
    error_filename = f"{timestamp}_errores.json"

    errores = []

    for idx, genero in enumerate(generos):
        genero_obj, err_resp, status = crearGeneroData(genero)
        if err_resp:
            error_json_str = err_resp.get_data(as_text=True)
            error_dict = json.loads(error_json_str)

            errores.append({
                "index": idx,
                "genero": genero,
                "error": error_dict.get("error", "Ya existe un género con este nombre"),
                "status_code": status
            })
            continue

        resp, status = guardarGeneroDB(genero_obj)
        if status >= 400:
            error_json_str = resp.get_data(as_text=True)
            error_dict = json.loads(error_json_str)

            errores.append({
                "index": idx,
                "genero": genero,
                "error": error_dict.get("error", "Ya existe un género con este nombre o el subgénero no está asociado a un género padre"),
                "status_code": status
            })

    # Guardar archivos
    ruta_original = os.path.join(carpeta_destino, original_filename)
    ruta_errores = os.path.join(carpeta_destino, error_filename)

    with open(ruta_original, "w", encoding="utf-8") as f:
        json.dump(generos, f, indent=2, ensure_ascii=False)

    with open(ruta_errores, "w", encoding="utf-8") as f:
        json.dump(errores, f, indent=2, ensure_ascii=False)

    return {
        "mensaje": "Procesamiento completado",
        "archivo_original": original_filename,
        "archivo_errores": error_filename,
        "errores": errores
    }
