#!/usr/bin/env python3
"""
sync-plan.py — Sincroniza variables de Finanzas.xlsx → plan.html
Uso: python3 sync-plan.py

Lee los named ranges de Finanzas.xlsx y actualiza:
  1. El bloque XLSX_DATA en el <script> de plan.html
  2. Los elementos HTML con id="*" que muestran valores financieros

Named ranges usados:
  Presupuesto       → costo total del evento (con IVA)
  Meta_Conservadora → meta de ingresos conservadora  ← fuente de "Meta de Ingresos"
  Meta_Base         → meta de ingresos base
  Meta_Optimista    → meta de ingresos optimista
  Gastos            → gastos ejercidos a la fecha
  Ingresos          → ingresos recaudados a la fecha
  Balance           → Ingresos − Gastos
  MetaPorcentaje    → % de avance hacia la meta
  Capacidad_Evento  → número de asistentes
  Capacidad_VIPs    → cupos VIP
  Capacidad_Talleres → cupos totales de talleres
"""

import re
import sys
from pathlib import Path
from datetime import datetime

try:
    import openpyxl
except ImportError:
    print("Instalando openpyxl...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "openpyxl",
                    "--break-system-packages", "-q"], check=True)
    import openpyxl

# ── Rutas ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
HTML_FILE  = SCRIPT_DIR / "plan.html"
XLSX_FILE  = SCRIPT_DIR.parents[1] / "Finanzas" / "Finanzas.xlsx"

# ── Leer named ranges del xlsx ───────────────────────────────────────────────
def leer_named_range(wb, name, default=None):
    if name not in wb.defined_names:
        return default
    dests = list(wb.defined_names[name].destinations)
    if not dests:
        return default
    sheet_name, coord = dests[0]
    return wb[sheet_name][coord].value

def leer_valores():
    wb = openpyxl.load_workbook(XLSX_FILE, data_only=True)

    presupuesto       = leer_named_range(wb, "Presupuesto",       0)
    meta_conservadora = leer_named_range(wb, "Meta_Conservadora", 0)
    meta_base         = leer_named_range(wb, "Meta_Base",         0)
    meta_optimista    = leer_named_range(wb, "Meta_Optimista",    0)
    gastos            = leer_named_range(wb, "Gastos",            0)
    ingresos          = leer_named_range(wb, "Ingresos",          0)
    balance           = leer_named_range(wb, "Balance",           0)
    meta_porcentaje   = leer_named_range(wb, "MetaPorcentaje",    0)

    # Partidas del presupuesto
    bar_produccion   = leer_named_range(wb, "Audiovisual",    0)
    bar_escenografia = leer_named_range(wb, "Escenografía",   0)
    bar_salones      = leer_named_range(wb, "Salones",        0)
    bar_marketing    = leer_named_range(wb, "Marketing",      0)
    bar_ponentes     = leer_named_range(wb, "Speakers",       0)
    bar_software     = leer_named_range(wb, "Software",       0)
    bar_seguro       = leer_named_range(wb, "Contingencia",   0)
    bar_materiales   = leer_named_range(wb, "Materiales",     0)

    # Capacidades
    cap_evento      = int(leer_named_range(wb, "Capacidad_Evento",     200))
    cap_vips        = int(leer_named_range(wb, "Capacidad_VIPs",       20))
    cap_talleres    = int(leer_named_range(wb, "Capacidad_Talleres",   80))
    cap_networking  = int(leer_named_range(wb, "Capacidad_Networking", 25))

    # Meta_Base es la referencia principal para plan.html
    superavit = meta_base - presupuesto

    return {
        # KPIs principales
        "Presupuesto":       presupuesto,
        "Meta_Conservadora": meta_conservadora,
        "Meta_Base":         meta_base,
        "Meta_Optimista":    meta_optimista,
        "Gastos":            gastos,
        "Ingresos":          ingresos,
        "Balance":           balance,
        "MetaPorcentaje":    meta_porcentaje,
        "Superavit":         superavit,
        "Meta":              meta_base,
        # Barras de presupuesto
        "Bar_Produccion":    bar_produccion,
        "Bar_Escenografia":  bar_escenografia,
        "Bar_Salones":       bar_salones,
        "Bar_Marketing":     bar_marketing,
        "Bar_Ponentes":      bar_ponentes,
        "Bar_Software":      bar_software,
        "Bar_Seguro":        bar_seguro,
        "Bar_Materiales":    bar_materiales,
        # Capacidades
        "Cap_Evento":        cap_evento,
        "Cap_VIPs":          cap_vips,
        "Cap_Talleres":      cap_talleres,
        "Cap_Networking":    cap_networking,
    }

# ── Formateo ─────────────────────────────────────────────────────────────────
def fmt_mxn(n):
    """1663437.5 → '$1,663,438'"""
    return f"${abs(n):,.0f}"

def fmt_signed(n):
    """2360884 → '+$2,360,884'  /  -500 → '-$500'"""
    sign = "+" if n >= 0 else "-"
    return f"{sign}${abs(n):,.0f}"

def fmt_pct(n):
    """0.12 → '12%'  /  12 → '12%'"""
    val = n * 100 if abs(n) <= 1 else n
    return f"{val:.0f}%"

# ── Helpers HTML ─────────────────────────────────────────────────────────────
def set_inner(html: str, elem_id: str, new_inner: str) -> str:
    open_pat = rf'<(\w+)(?=[^>]*\bid="{re.escape(elem_id)}")[^>]*>'
    m = re.search(open_pat, html)
    if not m:
        print(f"  ⚠️  ID no encontrado: {elem_id}")
        return html
    tag = m.group(1)
    pattern = rf'(<{tag}(?=[^>]*\bid="{re.escape(elem_id)}")[^>]*>)(.*?)(</{tag}>)'
    result, n = re.subn(pattern,
                        lambda x: x.group(1) + new_inner + x.group(3),
                        html, count=1, flags=re.DOTALL)
    if n == 0:
        print(f"  ⚠️  No se pudo reemplazar: {elem_id}")
    return result

def update_xlsx_data_block(html: str, v: dict) -> str:
    """Reemplaza el bloque XLSX_DATA entre los marcadores de sync."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_block = f"""/* <<XLSX-SYNC:finanzas_valores>> */
  // Actualizado automáticamente: {ts}
  const XLSX_DATA = {{
    presupuesto:        {v['Presupuesto']},
    meta:               {v['Meta_Base']},
    meta_conservadora:  {v['Meta_Conservadora']},
    meta_base:          {v['Meta_Base']},
    meta_optimista:     {v['Meta_Optimista']},
    gastos:             {v['Gastos']},
    ingresos:           {v['Ingresos']},
    balance:            {v['Balance']},
    meta_porcentaje:    {v['MetaPorcentaje']},
    superavit:          {v['Superavit']},
    bar_produccion:     {v['Bar_Produccion']},
    bar_escenografia:   {v['Bar_Escenografia']},
    bar_salones:        {v['Bar_Salones']},
    bar_marketing:      {v['Bar_Marketing']},
    bar_ponentes:       {v['Bar_Ponentes']},
    bar_software:       {v['Bar_Software']},
    bar_seguro:         {v['Bar_Seguro']},
    bar_materiales:     {v['Bar_Materiales']},
    capacidad_evento:   {v['Cap_Evento']},
    capacidad_vips:     {v['Cap_VIPs']},
    capacidad_talleres: {v['Cap_Talleres']},
    capacidad_networking: {v['Cap_Networking']},
  }};
  /* <</XLSX-SYNC:finanzas_valores>> */"""

    pattern = r'/\* <<XLSX-SYNC:finanzas_valores>> \*/.*?/\* <</XLSX-SYNC:finanzas_valores>> \*/'
    result, n = re.subn(pattern, new_block, html, count=1, flags=re.DOTALL)
    if n == 0:
        print("  ⚠️  Marcador XLSX-SYNC no encontrado en plan.html")
    else:
        print("  ✅ XLSX_DATA block")
    return result

# ── Actualizar elementos HTML ─────────────────────────────────────────────────
def actualizar(html: str, v: dict) -> str:
    html = update_xlsx_data_block(html, v)

    p = v["Presupuesto"]
    mc = v["Meta_Base"]
    sup = v["Superavit"]
    pct = v["MetaPorcentaje"]
    ing = v["Ingresos"]
    gas = v["Gastos"]
    bal = v["Balance"]

    cambios = [
        # Sección Inicio
        ("ini-presupuesto",  fmt_mxn(p)),
        ("ini-meta",         fmt_mxn(mc)),
        ("ini-ingresos",     fmt_mxn(ing)),
        ("ini-gastos",       fmt_mxn(gas)),
        ("ini-balance",      fmt_signed(bal)),
        ("ini-meta-pct",     fmt_pct(pct)),

        # Sección Presupuesto
        ("pres-total-iva",   fmt_mxn(p)),
        ("pres-total-iva-2", fmt_mxn(p)),
        ("pres-meta",        fmt_mxn(mc)),
        ("pres-superavit",   fmt_signed(sup)),

        # Sección Ingresos
        ("ing-presupuesto",   fmt_mxn(p)),
        ("ing-vs-pres-label", f"vs Presupuesto {fmt_mxn(p)}"),

        # Barras del presupuesto
        ("pres-bar-produccion",   fmt_mxn(v["Bar_Produccion"])),
        ("pres-bar-escenografia", fmt_mxn(v["Bar_Escenografia"])),
        ("pres-bar-salones",      fmt_mxn(v["Bar_Salones"])),
        ("pres-bar-marketing",    fmt_mxn(v["Bar_Marketing"])),
        ("pres-bar-ponentes",     fmt_mxn(v["Bar_Ponentes"])),
        ("pres-bar-software",     fmt_mxn(v["Bar_Software"])),
        ("pres-bar-seguro",       fmt_mxn(v["Bar_Seguro"])),
        ("pres-contingencia",     fmt_mxn(v["Bar_Seguro"])),
        ("pres-bar-diseno",       fmt_mxn(v["Bar_Materiales"])),

        # Capacidades
        ("ini-capacidad",  f"{v['Cap_Evento']} personas"),
        ("venue-cap",      f"{v['Cap_Evento']} personas"),
    ]

    for elem_id, inner in cambios:
        html = set_inner(html, elem_id, inner)
        print(f"  ✅ {elem_id}")

    return html

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print(f"\n📊 Leyendo {XLSX_FILE.name}…")
    v = leer_valores()
    print(f"   Presupuesto       : {fmt_mxn(v['Presupuesto'])}")
    print(f"   Meta_Conservadora : {fmt_mxn(v['Meta_Conservadora'])}")
    print(f"   Meta_Base (activa): {fmt_mxn(v['Meta_Base'])}")
    print(f"   Meta_Base         : {fmt_mxn(v['Meta_Base'])}")
    print(f"   Meta_Optimista    : {fmt_mxn(v['Meta_Optimista'])}")
    print(f"   Gastos            : {fmt_mxn(v['Gastos'])}")
    print(f"   Ingresos          : {fmt_mxn(v['Ingresos'])}")
    print(f"   Balance           : {fmt_signed(v['Balance'])}")
    print(f"   Superávit obj.    : {fmt_signed(v['Superavit'])}")

    print(f"\n📝 Actualizando {HTML_FILE.name}…")
    html = HTML_FILE.read_text(encoding="utf-8")
    html = actualizar(html, v)
    HTML_FILE.write_text(html, encoding="utf-8")

    print(f"\n🎉 Listo — plan.html actualizado ({len([x for x in ['XLSX_DATA'] + ['']*22])} elementos)")

if __name__ == "__main__":
    main()
