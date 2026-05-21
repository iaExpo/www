#!/usr/bin/env python3
"""
sync-2027.py — Sincroniza variables de Finanzas.xlsx → 2027.html
Uso: python3 sync-2027.py

Lee los named ranges de Finanzas.xlsx y actualiza los elementos
con id="ev-*" en 2027.html.

Named ranges usados:
  Capacidad_Evento    → líderes / lugares en toda la página
  Venue               → nombre del venue (sede)
  Capacidad_Taller    → cupo por taller (grupo pequeño)
  Capacidad_Talleres  → cupo total de todos los talleres
  Capacidad_Networking → número de líderes en sesión de networking
  Precio_Expo         → precio normal boleto Expo
  Precio_Taller       → precio normal boleto Talleres
  Precio_Conferencias → precio normal boleto Conferencias
  Precio_Networking   → precio normal boleto Networking
  Precio_VIP          → precio normal boleto VIP
  USD                 → tipo de cambio USD/MXN (referencia)
"""

import re
import sys
from pathlib import Path

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
HTML_FILE  = SCRIPT_DIR / "2027.html"
XLSX_FILE  = SCRIPT_DIR.parents[1] / "Finanzas" / "Finanzas.xlsx"

# ── Leer named ranges del xlsx ───────────────────────────────────────────────
def leer_named_range(wb, name, default=None):
    """Lee el valor de un named range por su nombre."""
    if name not in wb.defined_names:
        return default
    dests = list(wb.defined_names[name].destinations)
    if not dests:
        return default
    sheet_name, coord = dests[0]
    return wb[sheet_name][coord].value

def leer_valores():
    wb = openpyxl.load_workbook(XLSX_FILE, data_only=True)
    return {
        "Capacidad_Evento":    int(leer_named_range(wb, "Capacidad_Evento",    200)),
        "Venue":               str(leer_named_range(wb, "Venue",               "Por confirmar")),
        "Capacidad_Taller":    int(leer_named_range(wb, "Capacidad_Taller",    20)),
        "Capacidad_Talleres":  int(leer_named_range(wb, "Capacidad_Talleres",  80)),
        "Capacidad_Networking":int(leer_named_range(wb, "Capacidad_Networking",25)),
        "Precio_Expo":         leer_named_range(wb, "Precio_Expo",         9900),
        "Precio_Taller":       leer_named_range(wb, "Precio_Taller",       9900),
        "Precio_Conferencias": leer_named_range(wb, "Precio_Conferencias", 29900),
        "Precio_Networking":   leer_named_range(wb, "Precio_Networking",   39900),
        "Precio_VIP":          leer_named_range(wb, "Precio_VIP",          49900),
        "USD":                 leer_named_range(wb, "USD",                 17.26),
    }

# ── Formateo ─────────────────────────────────────────────────────────────────
def fmt_precio(n):
    """9900 → '$9,900 MXN'"""
    return f"${int(n):,} MXN"

def fmt_launch(n):
    """9900 → '$4,950'  (50% OFF, sin decimales)"""
    return f"${int(n / 2):,}"

# ── Helpers ──────────────────────────────────────────────────────────────────
def set_inner(html: str, elem_id: str, new_inner: str) -> str:
    """Reemplaza el innerHTML del elemento con id dado.
    Detecta el tag de apertura para hacer match correcto del cierre."""
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

def set_attr(html: str, elem_id: str, attr: str, new_val: str) -> str:
    """Reemplaza el valor de un atributo en el tag con el id dado.
    Útil para <meta content="..."> y similares."""
    pattern = (rf'(<\w+(?=[^>]*\bid="{re.escape(elem_id)}")[^>]*\s'
               rf'{re.escape(attr)}=")([^"]*?)(")')
    result, n = re.subn(pattern,
                        lambda m: m.group(1) + new_val + m.group(3),
                        html, count=1)
    if n == 0:
        print(f"  ⚠️  Atributo no encontrado: {elem_id}[{attr}]")
    return result

# ── Actualizar todos los elementos ev-* ──────────────────────────────────────
def actualizar(html: str, v: dict) -> str:
    cap   = v["Capacidad_Evento"]
    venue = v["Venue"]
    ct    = v["Capacidad_Taller"]

    # ── Atributos (meta tags, etc.) ──
    attrs = [
        # id              atributo   nuevo valor
        ("ev-meta-desc", "content",
         f"El evento de inteligencia artificial más inspirador de LATAM. "
         f"3 días, 8 tracks, {cap} líderes. Ciudad de México, 28–30 Enero 2027."),
    ]

    cn   = v["Capacidad_Networking"]
    expo = v["Precio_Expo"]
    tal  = v["Precio_Taller"]
    conf = v["Precio_Conferencias"]
    net  = v["Precio_Networking"]

    # ── innerHTML de elementos normales ──
    inners = [
        # id                   nuevo innerHTML
        ("ev-hero-loc",
         f"📍 {venue} · Ciudad de México"),

        ("ev-hero-desc",
         f"El evento de inteligencia artificial más inspirador de LATAM regresa "
         f"más grande y más poderoso. "
         f"<strong>3 días, 8 tracks temáticos, 4 talleres prácticos y líderes de alto impacto</strong> "
         f"que ya están usando la IA para transformar industrias reales."),

        ("ev-stat-asistentes",
         str(cap)),

        ("ev-expo-cap",
         f"Solo <strong>{cap} lugares</strong> disponibles. "
         f"Precio de lanzamiento con 50% de descuento por tiempo limitado."),

        ("ev-talleres-cupo",
         f"Grupos de máximo {ct} personas — aprendizaje profundo y aplicado"),

        ("ev-network-cap",
         f"{cap} C-Levels y tomadores de decisión de toda LATAM"),

        ("ev-cfp-desc",
         f"¿Tu investigación está cambiando el mundo con IA? "
         f"Envía tu paper y preséntalo ante {cap} líderes, "
         f"académicos e innovadores de LATAM."),

        ("ev-reg-desc",
         f"Precio de lanzamiento con 50% OFF · Solo {cap} lugares disponibles"),

        ("ev-info-sede",
         f"{venue} • Ciudad de México"),

        # ── Precios de boletos ──
        ("ev-tkt-expo-launch",  fmt_launch(expo)),
        ("ev-tkt-expo-orig",    fmt_precio(expo)),

        ("ev-tkt-taller-launch",fmt_launch(tal)),
        ("ev-tkt-taller-orig",  fmt_precio(tal)),

        ("ev-tkt-conf-launch",  fmt_launch(conf)),
        ("ev-tkt-conf-orig",    fmt_precio(conf)),

        ("ev-tkt-net-desc",
         f"Sesión de matchmaking estructurado con los {cn} líderes más relevantes "
         f"del ecosistema IA de LATAM."),
        ("ev-tkt-net-launch",   fmt_launch(net)),
        ("ev-tkt-net-orig",     fmt_precio(net)),

        ("ev-tkt-vip-launch",   fmt_launch(v["Precio_VIP"])),
        ("ev-tkt-vip-orig",     fmt_precio(v["Precio_VIP"])),

        # ── Precios en tabla comparativa ──
        ("ev-cmp-expo-price",   fmt_launch(expo)),
        ("ev-cmp-taller-price", fmt_launch(tal)),
        ("ev-cmp-conf-price",   fmt_launch(conf)),
        ("ev-cmp-net-price",    fmt_launch(net)),
        ("ev-cmp-vip-price",    fmt_launch(v["Precio_VIP"])),

        # ── Badges con cupos ──
        ("ev-tkt-taller-badge", f"50% OFF · Solo {v['Capacidad_Talleres']} cupos"),
        ("ev-tkt-conf-badge",   f"50% OFF · Solo {v['Capacidad_Evento']} cupos"),
        ("ev-tkt-net-badge",    f"50% OFF · Solo {v['Capacidad_Networking']} cupos"),
    ]

    for elem_id, attr, val in attrs:
        html = set_attr(html, elem_id, attr, val)
        print(f"  ✅ {elem_id}[{attr}]")

    for elem_id, inner in inners:
        html = set_inner(html, elem_id, inner)
        print(f"  ✅ {elem_id}")

    return html

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print(f"\n📊 Leyendo {XLSX_FILE.name}…")
    v = leer_valores()
    print(f"   Capacidad_Evento    : {v['Capacidad_Evento']}")
    print(f"   Venue               : {v['Venue']}")
    print(f"   Capacidad_Taller    : {v['Capacidad_Taller']}")
    print(f"   Capacidad_Talleres  : {v['Capacidad_Talleres']}")
    print(f"   Capacidad_Networking: {v['Capacidad_Networking']}")
    print(f"   Precio_Expo         : ${v['Precio_Expo']:,}")
    print(f"   Precio_Taller       : ${v['Precio_Taller']:,}")
    print(f"   Precio_Conferencias : ${v['Precio_Conferencias']:,}")
    print(f"   Precio_Networking   : ${v['Precio_Networking']:,}")
    print(f"   Precio_VIP          : ${v['Precio_VIP']:,}")
    print(f"   USD                 : ${v['USD']}")

    print(f"\n📝 Actualizando {HTML_FILE.name}…")
    html = HTML_FILE.read_text(encoding="utf-8")
    html = actualizar(html, v)
    HTML_FILE.write_text(html, encoding="utf-8")

    total = 1 + 29   # 1 atributo + 29 innerHTML
    print(f"\n🎉 Listo — {total} elementos actualizados en {HTML_FILE.name}")

if __name__ == "__main__":
    main()
