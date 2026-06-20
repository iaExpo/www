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
    cap_vips        = int(leer_named_range(wb, "Capacidad_VIPs",        20))
    cap_talleres    = int(leer_named_range(wb, "Capacidad_Talleres",    80))
    cap_networking  = int(leer_named_range(wb, "Capacidad_Networking",  25))
    cap_expo        = int(leer_named_range(wb, "Capacidad_Expo",       100))
    # VIP All Access y Networking Estructurado incluyen conferencias → se restan
    cap_conf        = cap_evento - cap_vips - cap_networking

    # Precios de boletos
    p_vip    = leer_named_range(wb, "Precio_VIP",          49900)
    p_net    = leer_named_range(wb, "Precio_Networking",   39900)
    p_conf   = leer_named_range(wb, "Precio_Conferencias", 29900)
    p_taller = leer_named_range(wb, "Precio_Taller",        9900)
    p_expo   = leer_named_range(wb, "Precio_Expo",          9900)

    # Precios de patrocinios
    p_diamante = leer_named_range(wb, "Precio_Diamante", 1000000)
    p_platino  = leer_named_range(wb, "Precio_Platino",   400000)
    p_oro      = leer_named_range(wb, "Precio_Oro",       200000)
    p_plata    = leer_named_range(wb, "Precio_Plata",     100000)

    # ── Fórmulas de precios por fase ──────────────────────────────
    # Lanzamiento = 50% del precio | Regular = 75% | Última = 100%
    def lanz(p):  return round(p * 0.50)
    def reg(p):   return round(p * 0.75)
    def full(p):  return int(p)

    # ── Ingresos por boleto por fase ──────────────────────────────
    # Distribución de capacidad: Lanzamiento 50% | Regular 35% | Última 15%
    def rev_l(p, c): return round(lanz(p) * c * 0.50)
    def rev_r(p, c): return round(reg(p)  * c * 0.35)
    def rev_f(p, c): return round(full(p) * c * 0.15)
    def rev_t(p, c): return rev_l(p,c) + rev_r(p,c) + rev_f(p,c)

    # ── Proyecciones de boletos ───────────────────────────────────
    vip_l  = rev_l(p_vip,    cap_vips);      vip_r  = rev_r(p_vip,    cap_vips)
    vip_f  = rev_f(p_vip,    cap_vips);      vip_t  = rev_t(p_vip,    cap_vips)
    net_l  = rev_l(p_net,    cap_networking); net_r  = rev_r(p_net,    cap_networking)
    net_f  = rev_f(p_net,    cap_networking); net_t  = rev_t(p_net,    cap_networking)
    conf_l = rev_l(p_conf,   cap_conf);      conf_r = rev_r(p_conf,   cap_conf)
    conf_f = rev_f(p_conf,   cap_conf);      conf_t = rev_t(p_conf,   cap_conf)
    tal_l  = rev_l(p_taller, cap_talleres);  tal_r  = rev_r(p_taller, cap_talleres)
    tal_f  = rev_f(p_taller, cap_talleres);  tal_t  = rev_t(p_taller, cap_talleres)
    exp_l  = rev_l(p_expo,   cap_expo);      exp_r  = rev_r(p_expo,   cap_expo)
    exp_f  = rev_f(p_expo,   cap_expo);      exp_t  = rev_t(p_expo,   cap_expo)

    sub_l = vip_l + net_l + conf_l + tal_l + exp_l
    sub_r = vip_r + net_r + conf_r + tal_r + exp_r
    sub_f = vip_f + net_f + conf_f + tal_f + exp_f
    sub_t = vip_t + net_t + conf_t + tal_t + exp_t
    cap_total = cap_vips + cap_networking + cap_evento + cap_talleres + cap_expo

    # ── Escenarios de patrocinios ─────────────────────────────────
    # Conservador: 0 Diamante, 1 Platino, 1 Oro, 1 Plata + micro
    micro_c = 265000;  micro_m = 360000;  micro_o = 375000
    pat_c_niveles = p_platino + p_oro + p_plata
    pat_m_niveles = p_diamante + p_platino + 2*p_oro + p_plata
    pat_o_niveles = p_diamante + 2*p_platino + 3*p_oro + 2*p_plata
    pat_c = pat_c_niveles + micro_c
    pat_m = pat_m_niveles + micro_m
    pat_o = pat_o_niveles + micro_o

    # ── Totales por escenario ─────────────────────────────────────
    total_c = sub_t + pat_c
    total_m = sub_t + pat_m
    total_o = sub_t + pat_o

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
        "Cap_Expo":          cap_expo,
        "Cap_Conf":          cap_conf,
        # Precios de boletos
        "P_VIP": p_vip, "P_Net": p_net, "P_Conf": p_conf,
        "P_Taller": p_taller, "P_Expo": p_expo,
        # Precios por fase
        "VIP_L": lanz(p_vip),  "VIP_R": reg(p_vip),  "VIP_F": full(p_vip),
        "Net_L": lanz(p_net),  "Net_R": reg(p_net),  "Net_F": full(p_net),
        "Conf_L":lanz(p_conf), "Conf_R":reg(p_conf), "Conf_F":full(p_conf),
        "Tal_L": lanz(p_taller),"Tal_R":reg(p_taller),"Tal_F":full(p_taller),
        "Exp_L": lanz(p_expo), "Exp_R": reg(p_expo), "Exp_F": full(p_expo),
        # Ingresos por boleto por fase
        "Vip_RevL":vip_l, "Vip_RevR":vip_r, "Vip_RevF":vip_f, "Vip_RevT":vip_t,
        "Net_RevL":net_l, "Net_RevR":net_r, "Net_RevF":net_f, "Net_RevT":net_t,
        "Conf_RevL":conf_l,"Conf_RevR":conf_r,"Conf_RevF":conf_f,"Conf_RevT":conf_t,
        "Tal_RevL":tal_l, "Tal_RevR":tal_r, "Tal_RevF":tal_f, "Tal_RevT":tal_t,
        "Exp_RevL":exp_l, "Exp_RevR":exp_r, "Exp_RevF":exp_f, "Exp_RevT":exp_t,
        "Sub_L":sub_l, "Sub_R":sub_r, "Sub_F":sub_f, "Sub_T":sub_t,
        "Cap_Total": cap_total,
        # Escenarios de patrocinios
        "Pat_C_Niveles": pat_c_niveles, "Pat_M_Niveles": pat_m_niveles, "Pat_O_Niveles": pat_o_niveles,
        "Pat_C": pat_c, "Pat_M": pat_m, "Pat_O": pat_o,
        "Pat_Diamante_M": p_diamante, "Pat_Diamante_O": p_diamante,
        # Totales por escenario
        "Total_C": total_c, "Total_M": total_m, "Total_O": total_o,
        "Vs_C": total_c - presupuesto, "Vs_M": total_m - presupuesto, "Vs_O": total_o - presupuesto,
        "Margen_C": total_c / presupuesto - 1,
        "Margen_M": total_m / presupuesto - 1,
        "Margen_O": total_o / presupuesto - 1,
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
        # ── Sección Inicio ──
        ("ini-presupuesto",  fmt_mxn(p)),
        ("ini-meta",         fmt_mxn(mc)),
        ("ini-ingresos",     fmt_mxn(ing)),
        ("ini-gastos",       fmt_mxn(gas)),
        ("ini-balance",      fmt_signed(bal)),
        ("ini-meta-pct",     fmt_pct(pct)),

        # ── Sección Presupuesto ──
        ("pres-total-iva",   fmt_mxn(p)),
        ("pres-total-iva-2", fmt_mxn(p)),
        ("pres-meta",        fmt_mxn(mc)),
        ("pres-superavit",   fmt_signed(sup)),

        # ── Barras del presupuesto ──
        ("pres-bar-produccion",   fmt_mxn(v["Bar_Produccion"])),
        ("pres-bar-escenografia", fmt_mxn(v["Bar_Escenografia"])),
        ("pres-bar-salones",      fmt_mxn(v["Bar_Salones"])),
        ("pres-bar-marketing",    fmt_mxn(v["Bar_Marketing"])),
        ("pres-bar-ponentes",     fmt_mxn(v["Bar_Ponentes"])),
        ("pres-bar-software",     fmt_mxn(v["Bar_Software"])),
        ("pres-bar-seguro",       fmt_mxn(v["Bar_Seguro"])),
        ("pres-contingencia",     fmt_mxn(v["Bar_Seguro"])),
        ("pres-bar-diseno",       fmt_mxn(v["Bar_Materiales"])),

        # ── Capacidades ──
        ("ini-capacidad",  f"{v['Cap_Evento']} personas"),
        ("venue-cap",      f"{v['Cap_Evento']} personas"),

        # ── Ingresos — KPI strip ──
        ("ing-presupuesto",    fmt_mxn(p)),
        ("ing-boletos-total",  fmt_mxn(v["Sub_T"])),
        ("ing-escenario-conserv", fmt_mxn(v["Total_C"])),
        ("ing-escenario-opt",     fmt_mxn(v["Total_O"])),
        ("ing-vs-pres-label",  f"vs Presupuesto {fmt_mxn(p)}"),

        # ── Tabla de precios por fase ──
        ("ing-cap-vip",    str(v["Cap_VIPs"])),
        ("ing-vip-launch", fmt_mxn(v["VIP_L"])),
        ("ing-vip-regular",fmt_mxn(v["VIP_R"])),
        ("ing-vip-full",   fmt_mxn(v["VIP_F"])),

        ("ing-cap-net",    str(v["Cap_Networking"])),
        ("ing-net-launch", fmt_mxn(v["Net_L"])),
        ("ing-net-regular",fmt_mxn(v["Net_R"])),
        ("ing-net-full",   fmt_mxn(v["Net_F"])),

        ("ing-cap-conf",     str(v["Cap_Conf"])),
        ("ing-conf-launch",  fmt_mxn(v["Conf_L"])),
        ("ing-conf-regular", fmt_mxn(v["Conf_R"])),
        ("ing-conf-full",    fmt_mxn(v["Conf_F"])),

        ("ing-cap-taller",     str(v["Cap_Talleres"])),
        ("ing-taller-launch",  fmt_mxn(v["Tal_L"])),
        ("ing-taller-regular", fmt_mxn(v["Tal_R"])),
        ("ing-taller-full",    fmt_mxn(v["Tal_F"])),

        ("ing-cap-expo",    str(v["Cap_Expo"])),
        ("ing-expo-launch", fmt_mxn(v["Exp_L"])),
        ("ing-expo-regular",fmt_mxn(v["Exp_R"])),
        ("ing-expo-full",   fmt_mxn(v["Exp_F"])),

        # ── Tabla de ingresos por boleto por fase ──
        ("ing-rev-vip-cap",    str(v["Cap_VIPs"])),
        ("ing-rev-vip-launch", fmt_mxn(v["Vip_RevL"])),
        ("ing-rev-vip-regular",fmt_mxn(v["Vip_RevR"])),
        ("ing-rev-vip-full",   fmt_mxn(v["Vip_RevF"])),
        ("ing-rev-vip-total",  fmt_mxn(v["Vip_RevT"])),

        ("ing-rev-net-cap",    str(v["Cap_Networking"])),
        ("ing-rev-net-launch", fmt_mxn(v["Net_RevL"])),
        ("ing-rev-net-regular",fmt_mxn(v["Net_RevR"])),
        ("ing-rev-net-full",   fmt_mxn(v["Net_RevF"])),
        ("ing-rev-net-total",  fmt_mxn(v["Net_RevT"])),

        ("ing-rev-conf-cap",    str(v["Cap_Conf"])),
        ("ing-rev-conf-launch", fmt_mxn(v["Conf_RevL"])),
        ("ing-rev-conf-regular",fmt_mxn(v["Conf_RevR"])),
        ("ing-rev-conf-full",   fmt_mxn(v["Conf_RevF"])),
        ("ing-rev-conf-total",  fmt_mxn(v["Conf_RevT"])),

        ("ing-rev-taller-cap",    str(v["Cap_Talleres"])),
        ("ing-rev-taller-launch", fmt_mxn(v["Tal_RevL"])),
        ("ing-rev-taller-regular",fmt_mxn(v["Tal_RevR"])),
        ("ing-rev-taller-full",   fmt_mxn(v["Tal_RevF"])),
        ("ing-rev-taller-total",  fmt_mxn(v["Tal_RevT"])),

        ("ing-rev-expo-cap",    str(v["Cap_Expo"])),
        ("ing-rev-expo-launch", fmt_mxn(v["Exp_RevL"])),
        ("ing-rev-expo-regular",fmt_mxn(v["Exp_RevR"])),
        ("ing-rev-expo-full",   fmt_mxn(v["Exp_RevF"])),
        ("ing-rev-expo-total",  fmt_mxn(v["Exp_RevT"])),

        ("ing-rev-sub-cap",     str(v["Cap_Total"])),
        ("ing-rev-sub-launch",  fmt_mxn(v["Sub_L"])),
        ("ing-rev-sub-regular", fmt_mxn(v["Sub_R"])),
        ("ing-rev-sub-full",    fmt_mxn(v["Sub_F"])),
        ("ing-rev-sub-total",   fmt_mxn(v["Sub_T"])),

        # ── Tabla de escenarios totales ──
        ("ing-scen-bol-conserv", fmt_mxn(v["Sub_T"])),
        ("ing-scen-bol-mod",     fmt_mxn(v["Sub_T"])),
        ("ing-scen-bol-opt",     fmt_mxn(v["Sub_T"])),

        ("ing-scen-pat-conserv",    fmt_mxn(v["Pat_C"])),
        ("ing-scen-pat-mod",        fmt_mxn(v["Pat_M"])),
        ("ing-scen-pat-opt",        fmt_mxn(v["Pat_O"])),

        ("ing-pat-diamante-mod",    fmt_mxn(v["Pat_Diamante_M"])),
        ("ing-pat-diamante-opt",    fmt_mxn(v["Pat_Diamante_O"])),
        ("ing-pat-niveles-conserv", fmt_mxn(v["Pat_C_Niveles"])),
        ("ing-pat-niveles-mod",     fmt_mxn(v["Pat_M_Niveles"])),
        ("ing-pat-niveles-opt",     fmt_mxn(v["Pat_O_Niveles"])),

        ("ing-scen-total-conserv",  fmt_mxn(v["Total_C"])),
        ("ing-scen-total-mod",      fmt_mxn(v["Total_M"])),
        ("ing-scen-total-opt",      fmt_mxn(v["Total_O"])),

        ("ing-vs-conservador", fmt_signed(v["Vs_C"])),
        ("ing-vs-moderado",    fmt_signed(v["Vs_M"])),
        ("ing-vs-optimista",   fmt_signed(v["Vs_O"])),

        ("ing-margen-conservador", fmt_pct(v["Margen_C"])),
        ("ing-margen-moderado",    fmt_pct(v["Margen_M"])),
        ("ing-margen-optimista",   fmt_pct(v["Margen_O"])),
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
