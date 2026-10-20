
import os

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI(
    title="POC QA Automation",
    version="1.1.0"
)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "qa-postgres"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "qa_database"),
    "user": os.getenv("DB_USER", "qa_user"),
    "password": os.getenv("DB_PASSWORD", ""),
}


class UsuarioCrear(BaseModel):
    nombre: str
    email: EmailStr
    activo: bool = True


@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "message": "API funcionando con Podman"
    }


@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):
    try:
        with psycopg.connect(**DB_CONFIG) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, nombre, email, activo
                    FROM usuarios
                    WHERE id = %s
                    """,
                    (usuario_id,)
                )
                usuario = cursor.fetchone()

        if usuario is None:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        return {
            "id": usuario[0],
            "nombre": usuario[1],
            "email": usuario[2],
            "activo": usuario[3]
        }

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="Base de datos no disponible"
        )


@app.post("/usuarios", status_code=201)
def crear_usuario(usuario: UsuarioCrear):
    try:
        with psycopg.connect(**DB_CONFIG) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO usuarios (nombre, email, activo)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (usuario.nombre, usuario.email, usuario.activo)
                )
                nuevo_id = cursor.fetchone()[0]

        return {
            "id": nuevo_id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "activo": usuario.activo
        }

    except psycopg.errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="El email ya está registrado"
        )
    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="Base de datos no disponible"
        )
