
import pandas as pd
import pytest
import pandera.pandas as pa

from pandera.errors import SchemaErrors
from generar_reporte_pandera import generar_reporte_pandera
from test_calidad_datos import schema_usuarios


def test_pandera_detecta_datos_invalidos():
    datos = pd.DataFrame([
        {
            "id": 1,
            "nombre": "Usuario QA",
            "email": "qa@test.com",
            "activo": True
        },
        {
            "id": 1,
            "nombre": "A",
            "email": "correo-invalido",
            "activo": False
        }
    ])

    with pytest.raises(SchemaErrors) as error:
        schema_usuarios.validate(datos, lazy=True)

    errores = error.value.failure_cases

    print("\nDefectos detectados por Pandera:")
    print(errores.to_string(index=False))

    reporte = generar_reporte_pandera(
        schema_usuarios,
        datos,
        errores,
        titulo="Calidad de Datos — Pandera (prueba negativa)",
        fuente="DataFrame de prueba",
        nombre_archivo="reporte_pandera_negativo",
    )
    print(f"\nReporte HTML: {reporte}")

    assert not errores.empty
