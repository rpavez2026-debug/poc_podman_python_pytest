
import os

import pandas as pd
import pandera.pandas as pa
import psycopg


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "5433")),
    "dbname": os.getenv("DB_NAME", "qa_database"),
    "user": os.getenv("DB_USER", "qa_user"),
    "password": os.getenv("DB_PASSWORD", "qa_password_local"),
}


schema_usuarios = pa.DataFrameSchema({
    "id": pa.Column(
        int,
        checks=pa.Check.gt(0),
        unique=True,
        nullable=False
    ),
    "nombre": pa.Column(
        str,
        checks=pa.Check.str_length(min_value=2),
        nullable=False
    ),
    "email": pa.Column(
        str,
        checks=pa.Check.str_matches(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        ),
        unique=True,
        nullable=False
    ),
    "activo": pa.Column(
        bool,
        nullable=False
    )
}, strict=True)


def test_calidad_datos_usuarios():
    with psycopg.connect(**DB_CONFIG) as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nombre, email, activo
                FROM usuarios
                ORDER BY id
                """
            )

            registros = cursor.fetchall()
            columnas = [
                descripcion.name
                for descripcion in cursor.description
            ]

    assert registros, "No existen usuarios para validar"

    dataframe = pd.DataFrame(
        registros,
        columns=columnas
    )

    schema_usuarios.validate(
        dataframe,
        lazy=True
    )
