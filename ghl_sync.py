"""
IA Expo 2027 — Actualizador de Variables en GoHighLevel
Uso: python3 ghl_sync.py
Lee iaExpo_data.csv y actualiza las variables en GHL.

Sección 1 (Tipo=Producto):
  - Admisiones: usa el precio de la columna indicada en Etapa_Activa
    (Lanzamiento → Precio_Lanzamiento, Anticipado → Precio_Anticipado, Regular → Precio_Regular)
  - Patrocinios: usa Precio_Regular (precio fijo)

Sección 2 (Tipo=Variable):
  - Actualiza variables financieras y de capacidad directamente con Valor
"""

import csv
import json
import os
import urllib.request
import urllib.error

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2NhdGlvbl9pZCI6IjVSWGoxZURRSWpOeDdlQ0hLYVpBIiwidmVyc2lvbiI6MSwiaWF0IjoxNzUxNzQ0NjExMjQxLCJzdWIiOiI0WDMxeXZ5dnRMamkxMlgwSFpqMCJ9.nwv0zVHfGwqNz1H_Vjwx4btlIbTV73g_oK0-Fc81u7I"
LOCATION_ID = "5RXj1eDQIjNx7eCHKaZA"

# ─────────────────────────────────────────────
# LÓGICA — no necesitas editar esto
# ─────────────────────────────────────────────

CSV_FILE = os.path.join(os.path.dirname(__file__), "iaExpo_data.csv")

BASE_URL = "https://rest.gohighlevel.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
}

ETAPA_A_COLUMNA = {
    "Lanzamiento": "Precio_Lanzamiento",
    "Anticipado":  "Precio_Anticipado",
    "Regular":     "Precio_Regular",
}


def api_request(method, path, data=None):
    url = f"{BASE_URL}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "message": e.read().decode()}


def listar_custom_values():
    print("\n📋 Obteniendo Custom Values actuales...\n")
    result = api_request("GET", "/custom-values/")
    if "error" in result:
        print(f"  ❌ Error al conectar: {result}")
        return {}
    values = {}
    for cv in result.get("customValues", []):
        clean_key = cv["fieldKey"].strip("{} ")
        values[clean_key] = cv
        print(f"  • {cv['fieldKey']} = {cv.get('value', '(vacío)')}")
    return values


def actualizar_variable(field_key, nuevo_valor, custom_values_map):
    clean = field_key.strip("{} ").replace("custom_values.", "").replace("custom.", "")
    cv = (
        custom_values_map.get(f"custom_values.{clean}")
        or custom_values_map.get(f"custom.{clean}")
    )
    if cv:
        result = api_request(
            "PUT",
            f"/custom-values/{cv['id']}",
            {"name": cv["name"], "value": nuevo_valor},
        )
        if "error" in result:
            print(f"  ❌ {clean}: {result['message']}")
        else:
            print(f"  ✅ {clean} → {nuevo_valor}")
    else:
        print(f"  ⚠️  {clean}: no encontrada en GHL (verifica el nombre)")


def leer_csv():
    """
    Lee iaExpo_data.csv y devuelve un dict {variable_ghl: valor_a_sincronizar}.
    - Sección Producto: usa Etapa_Activa para escoger columna de precio (Admisiones)
      o Precio_Regular directo (Patrocinios sin Etapa_Activa).
    - Sección Variable: usa la columna Valor directamente.
    """
    variables = {}
    try:
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tipo = row.get("Tipo", "").strip()
                var_ghl = row.get("Variable_GHL", "").strip()

                if not var_ghl:
                    continue  # fila vacía o separador

                if tipo == "Producto":
                    etapa = row.get("Etapa_Activa", "").strip()
                    if etapa:
                        # Admisión — precio según etapa activa
                        col = ETAPA_A_COLUMNA.get(etapa)
                        if col:
                            precio = row.get(col, "").strip()
                            if precio:
                                variables[var_ghl] = precio
                        else:
                            print(f"  ⚠️  Etapa desconocida '{etapa}' para {var_ghl}")
                    else:
                        # Patrocinio — precio fijo
                        precio = row.get("Precio_Regular", "").strip()
                        if precio:
                            variables[var_ghl] = precio

                elif tipo == "Variable":
                    valor = row.get("Valor", "").strip()
                    if valor:
                        variables[var_ghl] = valor

    except FileNotFoundError:
        raise FileNotFoundError(f"No encontré el archivo {CSV_FILE}")

    return variables


def main():
    print("=" * 50)
    print("  IA Expo 2027 — Actualizador de Variables GHL")
    print("=" * 50)

    try:
        variables = leer_csv()
    except FileNotFoundError as e:
        print(f"\n⛔ {e}\n")
        return

    print(f"\n📄 Variables a actualizar desde iaExpo_data.csv: {len(variables)}")
    for k, v in variables.items():
        print(f"  • {k} = {v}")

    custom_values_map = listar_custom_values()
    if not custom_values_map:
        print("\n⛔ No se pudo conectar con GHL. Verifica la API key.\n")
        return

    print("\n🔄 Actualizando variables...\n")
    for campo, valor in variables.items():
        actualizar_variable(campo, valor, custom_values_map)

    print("\n✨ Listo.\n")


if __name__ == "__main__":
    main()
