
import os
from datetime import datetime
from html import escape
from pathlib import Path

import pandas as pd

# Misma estructura que el proyecto Playwright: testresults/reports/<AAAAMMDD>/<AMBIENTE>/
DIRECTORIO_REPORTES = Path(__file__).resolve().parent.parent / "testresults" / "reports"


ESTILOS = """
    body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
    h1, h2 { color: #333; margin-top: 0; }
    .card { background: #fff; padding: 15px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,.15); }
    .cards-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 20px; }
    @media (max-width: 1100px) { .cards-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 600px) { .cards-grid { grid-template-columns: 1fr; } }
    .card-columna { padding: 12px 14px; }
    .card-header { font-size: 15px; font-weight: bold; color: #2e7d32; margin-bottom: 8px; }
    .qa-badge { display:inline-block; background:#e8f5e9; color:#1b5e20; font-size:11px; padding:1px 7px; border-radius:10px; margin-left:6px; font-weight:normal; }
    .tipo-badge { display:inline-block; background:#ede7f6; color:#4527a0; font-size:10px; padding:1px 7px; border-radius:10px; font-weight:normal; font-family:monospace; }
    .reglas-row { margin:4px 0 6px 0; display:flex; flex-wrap:wrap; gap:4px; }
    .regla-chip { display:inline-block; background:#e3f2fd; color:#1565c0; font-size:10px; font-weight:bold; padding:2px 7px; border-radius:10px; border:1px solid #90caf9; }
    .mini-table { width:100%; border-collapse:collapse; font-size:12px; }
    .mini-table td { padding:3px 4px; border:none; border-bottom:1px solid #f0f0f0; font-size:12px; }
    .mini-table td:last-child { text-align:right; font-weight:bold; }
    .mini-table td[colspan] { text-align:left; font-weight:normal; }
    .label-oscuro { color:#555 !important; text-shadow:none !important; }
    .mini-table tr:nth-child(even) { background: none; }
    .progress-bar-wrap { position:relative; height:16px; background:#e0e0e0; border-radius:8px; margin-bottom:10px; overflow:hidden; }
    .progress-bar { height:100%; border-radius:8px; }
    .progress-label { position:absolute; top:0; left:0; right:0; text-align:center; font-size:11px; line-height:16px; color:#fff; font-weight:bold; text-shadow:0 0 3px rgba(0,0,0,.5); }
    table { border-collapse: collapse; width: 100%; background: #fff; margin-bottom: 0; }
    th, td { border: 1px solid #ddd; padding: 3px 5px; font-size: 11px; }
    th { background: #4CAF50; color: #fff; position: sticky; top: 0; z-index: 2; white-space: nowrap; }
    tr:nth-child(even) { background: #f2f2f2; }
    .status-PASSED { color: #2e7d32; font-weight: bold; }
    .status-FAILED { color: #c62828; font-weight: bold; }
    .status-WARN   { color: #e65100; font-weight: bold; }
    .cel-coincide  { background: #e8f5e9; color: #1b5e20; font-weight: bold; }
    .cel-difiere   { background: #ffebee; color: #b71c1c; font-weight: bold; }
    .cel-neutro    { background: #f3e5f5; color: #4a148c; font-weight: bold; }
    .mono { font-family: monospace; }
    .td-center { text-align: center; }
    .table-scroll { max-height: 60vh; overflow: auto; border: 1px solid #ddd; }
    .seccion-header { color: #2e7d32; border-bottom: 2px solid #4CAF50; padding-bottom: 6px; margin-bottom: 12px; }
    .alert-box { padding: 10px 16px; border-radius: 6px; margin-bottom: 16px; background: #fff3e0; border-left: 4px solid #ff9800; font-size: 13px; }
    .ok-box { background: #e8f5e9; border-left-color: #4CAF50; }
    .resumen-global { border-left: 4px solid #4CAF50; }
    .rg-title { font-size: 11px; font-weight: bold; color: #2e7d32; margin-bottom: 8px; }
    .rg-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
    @media (max-width: 900px) { .rg-grid { grid-template-columns: repeat(2, 1fr); } }
    .rg-bloque { background: #f9f9f9; border-radius: 5px; padding: 7px 9px; }
    .rg-label { font-size: 9px; font-weight: bold; color: #555; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 5px; }
    .rg-valor { font-size: 16px; font-weight: bold; color: #333; line-height: 1; margin-bottom: 4px; }
    .rg-sub { font-size: 10px; margin-bottom: 5px; }
    .rg-fila { font-size: 10px; display: flex; align-items: center; gap: 4px; margin-bottom: 3px; }
    .rg-fila strong { margin-left: auto; font-size: 11px; }
    .rg-icon { display:inline-block; width:18px; text-align:center; border-radius:3px; padding:1px 2px; font-size:11px; }
    .rg-bar-wrap { position:relative; height:14px; background:#e0e0e0; border-radius:7px; overflow:hidden; margin-top:6px; }
    .rg-bar { height:100%; border-radius:7px; }
    .rg-bar-label { position:absolute; top:0; left:0; right:0; text-align:center; font-size:10px; line-height:14px; color:#fff; font-weight:bold; text-shadow:0 0 3px rgba(0,0,0,.5); }
    .rg-cero { color: #aaa; }
    .nota-pie { color:#aaa; font-size:11px; margin-top:20px; }
"""


def describir_regla(regla):
    """Traduce el nombre de un check de pandera a un texto legible."""
    regla = str(regla)

    if regla == "field_uniqueness":
        return "Valor único"
    if regla == "not_nullable":
        return "Sin nulos"
    if regla.startswith("greater_than("):
        return f"Mayor que {regla[len('greater_than('):-1]}"
    if regla.startswith("str_length("):
        minimo, maximo = regla[len("str_length("):-1].split(", ")
        if maximo == "None":
            return f"Mínimo {minimo} caracteres"
        return f"Entre {minimo} y {maximo} caracteres"
    if regla.startswith("str_matches("):
        return "Formato válido (regex)"
    if regla.startswith("dtype("):
        return f"Tipo {regla[len('dtype('):-1]}"
    if regla == "column_in_schema":
        return "Columna no definida en el esquema"
    if regla == "column_in_dataframe":
        return "Columna obligatoria ausente"

    return regla


def _reglas_de_columna(columna):
    reglas = [describir_regla(check.error) for check in columna.checks]

    if columna.unique:
        reglas.append("Valor único")
    if not columna.nullable:
        reglas.append("Sin nulos")

    return reglas


def _porcentaje(parte, total):
    return round(parte * 100 / total) if total else 100


def _color_barra(porcentaje):
    if porcentaje == 100:
        return "#4CAF50"
    if porcentaje >= 50:
        return "#ff9800"
    return "#e53935"


def _barra(porcentaje, etiqueta, prefijo="progress"):
    """Barra de progreso; `prefijo` es "progress" (tarjetas) o "rg" (resumen global)."""
    clase_label = "progress-label" if prefijo == "progress" else "rg-bar-label"

    # Con poca barra rellena, el texto blanco queda sobre gris y no se lee
    if porcentaje < 20:
        clase_label += " label-oscuro"

    return (
        f'<div class="{prefijo}-bar-wrap">'
        f'<div class="{prefijo}-bar" style="width:{porcentaje}%;'
        f'background:{_color_barra(porcentaje)}"></div>'
        f'<span class="{clase_label}">{porcentaje}% {escape(etiqueta)}</span>'
        "</div>"
    )


def _valor_conteo(cantidad, clase_si_hay):
    clase = clase_si_hay if cantidad else "rg-cero"
    return f'<strong class="{clase}">{cantidad}</strong>'


def generar_reporte_pandera(
    schema,
    dataframe,
    failure_cases=None,
    titulo="Calidad de Datos — Pandera",
    fuente="DataFrame",
    nombre_archivo="reporte_pandera",
    ambiente=None,
    directorio=DIRECTORIO_REPORTES,
):
    """Genera un reporte HTML con el resultado de validar `dataframe` contra `schema`.

    `failure_cases` es `SchemaErrors.failure_cases`, o `None` si la validación pasó.
    `ambiente` por defecto se toma de la variable de entorno AMBIENTE (o LOCAL).
    Devuelve la ruta del archivo generado.
    """
    ambiente = (ambiente or os.getenv("AMBIENTE", "LOCAL")).upper()

    if failure_cases is None:
        failure_cases = pd.DataFrame(
            columns=["schema_context", "column", "check", "check_number", "failure_case", "index"]
        )

    ahora = datetime.now()
    total_filas = len(dataframe)
    total_defectos = len(failure_cases)

    # Celdas con defecto: {(fila, columna): [reglas]}
    celdas_con_defecto = {}
    for caso in failure_cases.itertuples(index=False):
        if pd.notna(caso.index) and pd.notna(caso.column):
            celdas_con_defecto.setdefault((caso.index, caso.column), []).append(
                describir_regla(caso.check)
            )

    filas_con_defecto = {fila for fila, _ in celdas_con_defecto}
    filas_validas = total_filas - len(filas_con_defecto)
    pct_filas_validas = _porcentaje(filas_validas, total_filas)

    # Defectos que no apuntan a una celda concreta (columnas extra o ausentes, tipos)
    defectos_esquema = failure_cases[failure_cases["index"].isna()]

    defectos_por_columna = failure_cases["column"].fillna("(esquema)").value_counts()
    defectos_por_regla = failure_cases["check"].map(describir_regla).value_counts()

    columnas_esquema = list(schema.columns)
    columnas_extra = [c for c in dataframe.columns if c not in schema.columns]
    columnas_ausentes = [c for c in columnas_esquema if c not in dataframe.columns]

    # ── Encabezado y alerta ────────────────────────────────────────────────
    partes = [
        "<!DOCTYPE html>",
        '<html lang="es">',
        "<head>",
        '  <meta charset="utf-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1">',
        f"  <title>{escape(titulo)} {ahora:%Y%m%d}</title>",
        f"  <style>{ESTILOS}  </style>",
        "</head>",
        "<body>",
        f"  <h1>{escape(titulo)}</h1>",
        '  <p style="color:#666;margin-top:-10px">',
        f"    Fecha: {ahora:%Y%m%d} &nbsp;|&nbsp; Generado: {ahora:%Y-%m-%d %H:%M:%S} &nbsp;|&nbsp;",
        f"    Ambiente: <strong>{escape(ambiente)}</strong> &nbsp;|&nbsp;",
        f"    Fuente: <strong>{escape(fuente)}</strong> &nbsp;|&nbsp;",
        f"    Filas evaluadas: <strong>{total_filas}</strong> &nbsp;|&nbsp;",
        f'    <span class="status-PASSED">VÁLIDAS: {filas_validas}</span> &nbsp;|&nbsp;',
        f'    <span class="status-FAILED">CON DEFECTOS: {len(filas_con_defecto)}</span>',
        "  </p>",
    ]

    if total_defectos:
        partes.append(
            '  <div class="alert-box">'
            f'<span class="status-FAILED">&#x274C; {total_defectos} defectos detectados</span>'
            f' &nbsp;|&nbsp; <span class="status-WARN">&#x26A0;&#xFE0F; '
            f'{len(filas_con_defecto)} filas afectadas</span>'
            f' &nbsp;|&nbsp; <span class="status-WARN">'
            f'{len(defectos_por_columna)} columnas con defectos</span></div>'
        )
    else:
        partes.append(
            '  <div class="alert-box ok-box"><span class="status-PASSED">'
            "&#x2705; Sin defectos: todos los datos cumplen el esquema</span></div>"
        )

    # ── Resumen global ─────────────────────────────────────────────────────
    filas_por_columna = "".join(
        f'<div class="rg-fila"><span class="rg-icon '
        f'{"cel-difiere" if defectos_por_columna.get(c, 0) else "cel-coincide"}">'
        f'{"&#x274C;" if defectos_por_columna.get(c, 0) else "&#x2705;"}</span> '
        f'{escape(str(c))} {_valor_conteo(int(defectos_por_columna.get(c, 0)), "status-FAILED")}</div>'
        for c in columnas_esquema
    )

    filas_por_regla = "".join(
        f'<div class="rg-fila"><span class="rg-icon cel-difiere">&#x274C;</span> '
        f'{escape(regla)} {_valor_conteo(int(cantidad), "status-FAILED")}</div>'
        for regla, cantidad in defectos_por_regla.items()
    ) or (
        '<div class="rg-fila"><span class="rg-icon cel-coincide">&#x2705;</span> '
        'Todas las reglas cumplidas <strong class="status-PASSED">0</strong></div>'
    )

    partes += [
        '  <div class="card resumen-global">',
        f'    <div class="rg-title">&#x1F4CA; Resumen Global — {escape(fuente)}</div>',
        '    <div class="rg-grid">',
        '      <div class="rg-bloque">',
        '        <div class="rg-label">Filas evaluadas</div>',
        f'        <div class="rg-valor">{total_filas}</div>',
        '        <div class="rg-sub">',
        f'          <span class="status-PASSED">&#x2705; VÁLIDAS: {filas_validas}</span> &nbsp;|&nbsp;',
        f'          <span class="status-FAILED">&#x274C; CON DEFECTOS: {len(filas_con_defecto)}</span>',
        "        </div>",
        f"        {_barra(pct_filas_validas, 'VÁLIDAS', 'rg')}",
        "      </div>",
        '      <div class="rg-bloque">',
        '        <div class="rg-label">Defectos por columna</div>',
        f"        {filas_por_columna}",
        "      </div>",
        '      <div class="rg-bloque">',
        '        <div class="rg-label">Defectos por regla</div>',
        f"        {filas_por_regla}",
        "      </div>",
        '      <div class="rg-bloque">',
        '        <div class="rg-label">Esquema</div>',
        f'        <div class="rg-fila">Columnas definidas <strong>{len(columnas_esquema)}</strong></div>',
        f'        <div class="rg-fila">Modo estricto <strong>{"Sí" if schema.strict else "No"}</strong></div>',
        f'        <div class="rg-fila">Columnas extra {_valor_conteo(len(columnas_extra), "status-FAILED")}</div>',
        f'        <div class="rg-fila">Columnas ausentes {_valor_conteo(len(columnas_ausentes), "status-FAILED")}</div>',
        "      </div>",
        "    </div>",
        "  </div>",
    ]

    # ── Tarjeta por columna ────────────────────────────────────────────────
    partes.append('  <div class="cards-grid">')

    for nombre, columna in schema.columns.items():
        filas_mal = {fila for fila, col in celdas_con_defecto if col == nombre}
        validas = total_filas - len(filas_mal)
        pct = _porcentaje(validas, total_filas)
        reglas = _reglas_de_columna(columna)
        chips = "".join(f'<span class="regla-chip">{escape(r)}</span> ' for r in reglas) or (
            '<span class="regla-chip">Solo tipo</span>'
        )
        defectos_columna = failure_cases[failure_cases["column"] == nombre]
        filas_reglas = "".join(
            f'<tr><td>&#x274C; {escape(regla)}</td><td class="status-FAILED">{cantidad}</td></tr>'
            for regla, cantidad in defectos_columna["check"].map(describir_regla).value_counts().items()
        ) or '<tr><td>&#x2705; Sin defectos</td><td class="status-PASSED">0</td></tr>'

        partes += [
            '    <div class="card card-columna">',
            f'      <div class="card-header">{escape(nombre)} '
            f'<span class="tipo-badge">{escape(str(columna.dtype))}</span></div>',
            f'      <div class="reglas-row">{chips}</div>',
            f"      {_barra(pct, 'VÁLIDOS')}",
            '      <table class="mini-table">',
            f"        <tr><td>Valores evaluados</td><td><strong>{total_filas}</strong></td></tr>",
            f'        <tr><td>Válidos</td><td class="status-PASSED">{validas}</td></tr>',
            f'        <tr><td>Con defecto</td><td class="{"status-FAILED" if filas_mal else "rg-cero"}">'
            f"{len(filas_mal)}</td></tr>",
            '        <tr><td colspan="2" style="border-top:1px solid #eee;padding-top:4px">'
            "<em>Reglas incumplidas</em></td></tr>",
            f"        {filas_reglas}",
            "      </table>",
            "    </div>",
        ]

    partes.append("  </div>")

    # ── Detalle de defectos ────────────────────────────────────────────────
    partes += [
        '  <div class="card">',
        f'    <h2 class="seccion-header">Detalle de defectos <span class="qa-badge">{total_defectos}</span></h2>',
    ]

    if total_defectos:
        filas_detalle = "".join(
            "<tr>"
            f'<td class="td-center"><strong>{n}</strong></td>'
            '<td class="status-FAILED">FAILED</td>'
            f'<td class="td-center">{"-" if pd.isna(caso.index) else int(caso.index)}</td>'
            f'<td class="mono">{escape("-" if pd.isna(caso.column) else str(caso.column))}</td>'
            f"<td>{escape(describir_regla(caso.check))}</td>"
            f'<td class="mono" style="color:#555">{escape(str(caso.check))}</td>'
            f'<td class="cel-difiere mono">{escape(str(caso.failure_case))}</td>'
            "</tr>"
            for n, caso in enumerate(failure_cases.itertuples(index=False), start=1)
        )
        partes += [
            '    <div class="table-scroll">',
            "    <table>",
            "      <thead><tr><th>N°</th><th>Estado</th><th>Fila</th><th>Columna</th>"
            "<th>Regla</th><th>Check pandera</th><th>Valor fallido</th></tr></thead>",
            f"      <tbody>{filas_detalle}</tbody>",
            "    </table>",
            "    </div>",
        ]
    else:
        partes.append('    <p class="status-PASSED">&#x2705; No se encontraron defectos.</p>')

    if len(defectos_esquema):
        partes.append(
            '    <p style="color:#888;font-size:11px;margin-top:4px">'
            f"{len(defectos_esquema)} defectos son del esquema (columnas o tipos) "
            "y no corresponden a una fila concreta.</p>"
        )

    partes.append("  </div>")

    # ── Datos evaluados ────────────────────────────────────────────────────
    encabezados = "".join(f"<th>{escape(str(c))}</th>" for c in dataframe.columns)
    filas_datos = []

    for n, (indice, fila) in enumerate(dataframe.iterrows(), start=1):
        tiene_defecto = indice in filas_con_defecto
        celdas = []

        for columna in dataframe.columns:
            reglas = celdas_con_defecto.get((indice, columna))
            valor = escape(str(fila[columna]))

            if reglas:
                titulo_celda = escape(" · ".join(reglas))
                celdas.append(f'<td class="cel-difiere" title="{titulo_celda}">'
                              f"&#x274C; {valor}</td>")
            elif columna in columnas_extra:
                celdas.append(f'<td class="cel-neutro">{valor}</td>')
            else:
                celdas.append(f'<td class="cel-coincide">{valor}</td>')

        estado = "FAILED" if tiene_defecto else "PASSED"
        filas_datos.append(
            f'<tr><td class="td-center"><strong>{n}</strong></td>'
            f'<td class="td-center">{escape(str(indice))}</td>'
            f'<td class="status-{estado}">{estado}</td>{"".join(celdas)}</tr>'
        )

    partes += [
        '  <div class="card">',
        f'    <h2 class="seccion-header">Datos evaluados <span class="qa-badge">{total_filas} filas</span></h2>',
        '    <div class="table-scroll">',
        "    <table>",
        f"      <thead><tr><th>N°</th><th>Fila</th><th>Estado</th>{encabezados}</tr></thead>",
        f"      <tbody>{''.join(filas_datos)}</tbody>",
        "    </table>",
        "    </div>",
        '    <p style="color:#888;font-size:11px;margin-top:4px">'
        "Pasa el cursor sobre una celda roja para ver la regla que incumple.</p>",
        "  </div>",
        '  <p class="nota-pie">',
        "    <strong>Lectura:</strong> verde = el valor cumple todas las reglas de su columna; "
        "rojo = incumple al menos una. "
        "Un mismo valor repetido aparece como defecto en cada fila donde se repite (regla Valor único). "
        "La validación es <em>lazy</em>: pandera reporta todos los defectos de una sola vez.",
        "  </p>",
        "</body>",
        "</html>",
    ]

    directorio = Path(directorio) / f"{ahora:%Y%m%d}" / ambiente
    directorio.mkdir(parents=True, exist_ok=True)
    ruta = directorio / f"{nombre_archivo}_{ambiente}_{ahora:%Y%m%d_%H%M%S}.html"
    ruta.write_text("\n".join(partes), encoding="utf-8")

    return ruta
