# =========================================================
# SISTEMA RRHH EMPRESARIAL v8.2 EXECUTIVE PRO
# CORPORATIVO · PROFESIONAL · MODULAR
# PYTHON + STREAMLIT + SQLITE + PLOTLY
# =========================================================

import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
import holidays
from datetime import datetime, timedelta

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY = True
except ImportError:
    PLOTLY = False

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="RRHH Executive Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# AUTH
# =========================================================

USUARIO_ADMIN = "Marko"
CLAVE_ADMIN   = "Maah2026*"

if "login_correcto" not in st.session_state:
    st.session_state.login_correcto = False

if "pagina" not in st.session_state:
    st.session_state.pagina = "Dashboard"

# =========================================================
# CSS ENTERPRISE PROFESIONAL
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/icon?family=Material+Icons+Round');

*, *::before, *::after {
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    box-sizing: border-box;
}

/* ── Ocultar elementos internos de Streamlit ── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

/* El texto "keyboard_double_..." que aparece en algunos themes */
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
[data-testid="collapsedControl"]          { display: none !important; }
button[aria-label="Collapse sidebar"]     { display: none !important; }
button[aria-label="Open sidebar"]         { display: none !important; }

/* ── APP BACKGROUND ── */
.stApp {
    background: #f1f5f9;
    background-image:
        url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%2394a3b8' fill-opacity='0.06' fill-rule='evenodd'%3E%3Ccircle cx='20' cy='20' r='1'/%3E%3C/g%3E%3C/svg%3E"),
        linear-gradient(155deg, #eef2ff 0%, #f1f5f9 50%, #f0fdf4 100%);
}

/* ══════════════════════════════════════════
   SIDEBAR ENTERPRISE
══════════════════════════════════════════ */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,
        #080d1a 0%,
        #0d1526 40%,
        #111d32 100%
    ) !important;
    border-right: 1px solid rgba(255,255,255,0.04) !important;
}

section[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}

/* ── Botones de navegación en sidebar ── */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #64748b !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    letter-spacing: 0.1px !important;
    box-shadow: none !important;
    text-align: left !important;
    justify-content: flex-start !important;
    transition: all 0.18s ease !important;
    margin: 1px 0 !important;
    transform: none !important;
    width: 100% !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.07) !important;
    color: #e2e8f0 !important;
    border-color: rgba(255,255,255,0.08) !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Botón activo (tipo primary) */
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: rgba(37,99,235,0.16) !important;
    color: #93c5fd !important;
    border-color: rgba(37,99,235,0.28) !important;
    border-left: 3px solid #3b82f6 !important;
    padding-left: 14px !important;
    font-weight: 700 !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ══════════════════════════════════════════
   BOTONES PRINCIPALES (fuera del sidebar)
══════════════════════════════════════════ */

.stButton > button {
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    box-shadow: 0 2px 8px rgba(29,78,216,0.28) !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.2px !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 18px rgba(29,78,216,0.36) !important;
}

.stButton > button[kind="secondary"] {
    background: linear-gradient(135deg, #b91c1c, #991b1b) !important;
    box-shadow: 0 2px 8px rgba(185,28,28,0.26) !important;
}

/* ══════════════════════════════════════════
   MÉTRICAS
══════════════════════════════════════════ */

div[data-testid="metric-container"] {
    background: white !important;
    border-radius: 16px !important;
    padding: 22px 20px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 6px rgba(15,23,42,0.05) !important;
    transition: all 0.2s ease !important;
    position: relative !important;
    overflow: hidden !important;
}

div[data-testid="metric-container"]::after {
    content: "";
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #1d4ed8, #6366f1);
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(15,23,42,0.09) !important;
}

div[data-testid="metric-container"] [data-testid="stMetricLabel"] p {
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.9px !important;
    color: #64748b !important;
}

div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    letter-spacing: -1px !important;
}

/* ══════════════════════════════════════════
   FORMULARIOS
══════════════════════════════════════════ */

[data-testid="stForm"] {
    background: white !important;
    border-radius: 18px !important;
    padding: 26px 30px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 6px rgba(15,23,42,0.04) !important;
}

/* ══════════════════════════════════════════
   INPUTS
══════════════════════════════════════════ */

.stTextInput input,
.stNumberInput input,
.stDateInput input {
    border-radius: 10px !important;
    border: 1.5px solid #e2e8f0 !important;
    background: #f8fafc !important;
    font-size: 14px !important;
    color: #0f172a !important;
    transition: all 0.2s ease !important;
}

.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: #1d4ed8 !important;
    box-shadow: 0 0 0 3px rgba(29,78,216,0.10) !important;
    background: white !important;
}

/* ══════════════════════════════════════════
   TABLAS
══════════════════════════════════════════ */

[data-testid="stDataFrame"] {
    background: white !important;
    border-radius: 14px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 4px rgba(15,23,42,0.04) !important;
    overflow: hidden !important;
}

/* ══════════════════════════════════════════
   TABS
══════════════════════════════════════════ */

.stTabs [data-baseweb="tab-list"] {
    background: #f1f5f9 !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid #e2e8f0 !important;
    gap: 2px !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    color: #64748b !important;
    transition: all 0.2s !important;
    padding: 8px 16px !important;
}

.stTabs [aria-selected="true"] {
    background: white !important;
    box-shadow: 0 1px 5px rgba(15,23,42,0.08) !important;
    color: #1d4ed8 !important;
}

/* ══════════════════════════════════════════
   EXPANDER
══════════════════════════════════════════ */

[data-testid="stExpander"] {
    background: white !important;
    border-radius: 12px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 3px rgba(15,23,42,0.04) !important;
}

/* ══════════════════════════════════════════
   DIVIDER
══════════════════════════════════════════ */

hr {
    border: none !important;
    border-top: 1px solid #e2e8f0 !important;
    margin: 22px 0 !important;
}

/* ══════════════════════════════════════════
   BANNERS DE MÓDULO
══════════════════════════════════════════ */

.module-banner {
    border-radius: 20px;
    padding: 44px 56px;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
    color: white;
}

.module-banner .geo1 {
    position: absolute;
    width: 460px; height: 460px;
    border-radius: 50%;
    background: radial-gradient(rgba(255,255,255,0.08), transparent 68%);
    top: -210px; right: -90px;
    pointer-events: none;
}

.module-banner .geo2 {
    position: absolute;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: radial-gradient(rgba(255,255,255,0.05), transparent 70%);
    bottom: -130px; left: -60px;
    pointer-events: none;
}

.module-banner .pattern {
    position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
    background-size: 38px 38px;
    pointer-events: none;
}

.module-banner .banner-badge {
    display: inline-flex;
    align-items: center;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 6px;
    padding: 4px 13px;
    font-size: 10px;
    font-weight: 700;
    color: rgba(255,255,255,0.82);
    margin-bottom: 14px;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    position: relative; z-index: 2;
}

.module-banner h1 {
    color: white !important;
    font-size: 34px !important;
    font-weight: 800 !important;
    letter-spacing: -0.8px !important;
    margin: 0 0 8px 0 !important;
    position: relative; z-index: 2;
    line-height: 1.1 !important;
}

.module-banner p {
    color: rgba(255,255,255,0.60) !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    margin: 0 !important;
    position: relative; z-index: 2;
    line-height: 1.6 !important;
    letter-spacing: 0.1px;
}

/* Colores banner por módulo */
.banner-dashboard  { background: linear-gradient(135deg, #0a0e27 0%, #0e1f5e 45%, #1a3a9f 75%, #1d4ed8 100%); }
.banner-empleados  { background: linear-gradient(135deg, #060d28 0%, #0c1e5a 45%, #134090 75%, #1558b0 100%); }
.banner-vacaciones { background: linear-gradient(135deg, #011c12 0%, #044a30 45%, #065f46 75%, #047857 100%); }
.banner-turnos     { background: linear-gradient(135deg, #120326 0%, #2a0860 45%, #4a1a95 75%, #5b21b6 100%); }
.banner-reportes   { background: linear-gradient(135deg, #1a0700 0%, #431407 45%, #7c2d12 75%, #b45309 100%); }

/* ══════════════════════════════════════════
   CARDS
══════════════════════════════════════════ */

.card {
    background: white;
    border-radius: 16px;
    padding: 22px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 5px rgba(15,23,42,0.04);
    margin-bottom: 14px;
    transition: box-shadow 0.2s ease;
}

.card:hover { box-shadow: 0 5px 22px rgba(15,23,42,0.08); }

.nav-item {
    display: flex; align-items: center; gap: 13px;
    padding: 12px 16px;
    background: #f8fafc; border-radius: 12px;
    margin-bottom: 8px; border: 1px solid #e2e8f0;
    transition: all 0.18s;
}

.nav-item:hover { background: #eff6ff; border-color: #bfdbfe; }

/* ══════════════════════════════════════════
   LOGIN
══════════════════════════════════════════ */

.login-card {
    background: white;
    border-radius: 24px;
    padding: 46px 42px;
    box-shadow: 0 20px 60px rgba(15,23,42,0.12), 0 0 0 1px rgba(226,232,240,0.6);
    max-width: 420px;
    margin: 52px auto 0;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGIN
# =========================================================

if not st.session_state.login_correcto:

    col1, col2, col3 = st.columns([1, 1.1, 1])

    with col2:
        st.markdown("""
        <div class="login-card">
          <div style="text-align:center; margin-bottom:30px;">
            <div style="margin:0 auto 18px; width:72px; filter:drop-shadow(0 8px 20px rgba(29,78,216,0.38));">
            <svg width="72" height="72" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="lg_login" x1="0" y1="0" x2="100" y2="100" gradientUnits="userSpaceOnUse">
                  <stop stop-color="#60a5fa"/>
                  <stop offset="0.5" stop-color="#2563eb"/>
                  <stop offset="1" stop-color="#1e40af"/>
                </linearGradient>
                <linearGradient id="lg_shine" x1="50" y1="0" x2="50" y2="55" gradientUnits="userSpaceOnUse">
                  <stop stop-color="white" stop-opacity="0.13"/>
                  <stop offset="1" stop-color="white" stop-opacity="0"/>
                </linearGradient>
              </defs>
              <rect width="100" height="100" rx="28" fill="url(#lg_login)"/>
              <rect width="100" height="55" rx="28" fill="url(#lg_shine)"/>
              <circle cx="50" cy="24" r="14" fill="white"/>
              <path d="M24 60C24 44 76 44 76 60" fill="white"/>
              <circle cx="18" cy="71" r="10" fill="white" fill-opacity="0.82"/>
              <path d="M3 94C3 83 33 83 33 94" fill="white" fill-opacity="0.82"/>
              <circle cx="82" cy="71" r="10" fill="white" fill-opacity="0.82"/>
              <path d="M67 94C67 83 97 83 97 94" fill="white" fill-opacity="0.82"/>
              <rect x="48" y="60" width="4" height="10" rx="2" fill="white" fill-opacity="0.38"/>
              <rect x="18" y="67" width="64" height="3.5" rx="1.75" fill="white" fill-opacity="0.38"/>
            </svg>
            </div>
            <div style="font-size:21px; font-weight:800; color:#0f172a; letter-spacing:-0.5px;">RRHH Executive Pro</div>
            <div style="font-size:13px; color:#64748b; margin-top:5px;">Plataforma Corporativa de Recursos Humanos</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        usuario = st.text_input("Usuario",    placeholder="Ingrese su usuario")
        clave   = st.text_input("Contraseña", type="password", placeholder="••••••••")

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        if st.button("Ingresar al Sistema", use_container_width=True):
            if usuario == USUARIO_ADMIN and clave == CLAVE_ADMIN:
                st.session_state.login_correcto = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas. Verifique usuario y contraseña.")

        st.markdown("""
        <div style="text-align:center; margin-top:18px; color:#94a3b8; font-size:11px; letter-spacing:0.4px;">
            Acceso restringido · Solo personal autorizado
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# =========================================================
# BASE DE DATOS
# =========================================================

DB_NAME = "gestion_personal.db"
conn    = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor  = conn.cursor()

def crear_tablas():
    cursor.execute("""CREATE TABLE IF NOT EXISTS empleados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL, cargo TEXT, dias_vacaciones INTEGER DEFAULT 15
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS vacaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empleado_id INTEGER, fecha_inicio TEXT, fecha_fin TEXT, dias_consumidos INTEGER
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS turnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empleado_id INTEGER, fecha_inicio TEXT, fecha_fin TEXT, tipo_turno TEXT
    )""")
    conn.commit()

crear_tablas()

# =========================================================
# FUNCIONES
# =========================================================

def obtener_empleados():
    return pd.read_sql_query("SELECT * FROM empleados ORDER BY nombre", conn)

def calcular_fecha_fin(fecha_inicio, dias_solicitados):
    chile_holidays = holidays.Chile()
    fecha_actual   = fecha_inicio
    dias = 0
    while dias < dias_solicitados:
        if fecha_actual.weekday() < 5 and fecha_actual not in chile_holidays:
            dias += 1
        if dias < dias_solicitados:
            fecha_actual += timedelta(days=1)
    return fecha_actual

def obtener_resumen_vacaciones(empleado_id):
    cursor.execute("SELECT dias_vacaciones FROM empleados WHERE id=?", (empleado_id,))
    r = cursor.fetchone()
    if r is None: return 0, 0, 0
    total = r[0]
    cursor.execute("SELECT COALESCE(SUM(dias_consumidos),0) FROM vacaciones WHERE empleado_id=?", (empleado_id,))
    c = cursor.fetchone()[0]
    return total, c, total - c

def render_banner(css_class, title, subtitle, badge=""):
    b = f'<div class="banner-badge">{badge}</div>' if badge else ""
    st.markdown(f"""
    <div class="module-banner {css_class}">
        <div class="geo1"></div><div class="geo2"></div><div class="pattern"></div>
        {b}<h1>{title}</h1><p>{subtitle}</p>
    </div>""", unsafe_allow_html=True)

def nav_btn(label, key):
    active = st.session_state.pagina == key
    t = "primary" if active else "secondary"
    if st.sidebar.button(label, key=f"nav_{key}", use_container_width=True, type=t):
        st.session_state.pagina = key
        st.rerun()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("""
<div style="padding:22px 10px 10px;">
  <div style="display:flex; align-items:center; gap:11px;">
    <div style="flex-shrink:0; filter:drop-shadow(0 3px 8px rgba(29,78,216,0.45));">
    <svg width="42" height="42" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="sb_bg" x1="0" y1="0" x2="100" y2="100" gradientUnits="userSpaceOnUse">
          <stop stop-color="#60a5fa"/><stop offset="1" stop-color="#1e40af"/>
        </linearGradient>
      </defs>
      <rect width="100" height="100" rx="26" fill="url(#sb_bg)"/>
      <rect width="100" height="46" rx="26" fill="white" fill-opacity="0.07"/>
      <circle cx="50" cy="25" r="13" fill="white"/>
      <path d="M26 59C26 45 74 45 74 59" fill="white"/>
      <circle cx="19" cy="71" r="9" fill="white" fill-opacity="0.80"/>
      <path d="M5 92C5 83 33 83 33 92" fill="white" fill-opacity="0.80"/>
      <circle cx="81" cy="71" r="9" fill="white" fill-opacity="0.80"/>
      <path d="M67 92C67 83 95 83 95 92" fill="white" fill-opacity="0.80"/>
      <rect x="48" y="59" width="4" height="11" rx="2" fill="white" fill-opacity="0.40"/>
      <rect x="19" y="67" width="62" height="3" rx="1.5" fill="white" fill-opacity="0.40"/>
    </svg>
    </div>
    <div>
      <div style="font-size:15px; font-weight:800; color:white; letter-spacing:-0.2px;">RRHH Pro</div>
      <div style="font-size:10px; color:rgba(255,255,255,0.35); letter-spacing:1px; text-transform:uppercase; margin-top:1px;">Executive Suite</div>
    </div>
  </div>
</div>
<div style="height:1px; background:rgba(255,255,255,0.06); margin:10px 10px 14px;"></div>
<div style="padding:0 10px 8px; font-size:10px; font-weight:700; color:rgba(255,255,255,0.25); letter-spacing:1.6px; text-transform:uppercase;">
    Navegación
</div>
""", unsafe_allow_html=True)

NAV = [
    ("  Dashboard",   "Dashboard"),
    ("  Empleados",   "Empleados"),
    ("  Vacaciones",  "Vacaciones"),
    ("  Turnos",      "Turnos"),
    ("  Reportes",    "Reportes"),
]

for label, key in NAV:
    nav_btn(label, key)

menu = st.session_state.pagina

# =========================================================
# DASHBOARD
# =========================================================

if menu == "Dashboard":

    render_banner("banner-dashboard",
        "Sistema de Gestión RRHH",
        "Plataforma Ejecutiva · Recursos Humanos · Turnos Operacionales · Prevención Laboral",
        "Executive Suite v8.2")

    components.html("""
    <div style="background:white;border-radius:16px;padding:18px 26px;border:1px solid #e2e8f0;
         box-shadow:0 1px 6px rgba(15,23,42,0.06);margin-bottom:4px;display:flex;align-items:center;gap:22px;">
      <div style="border-left:3px solid #1d4ed8; padding-left:16px;">
        <div id="hora" style="font-size:36px;font-weight:900;color:#1d4ed8;
             font-family:'Inter',system-ui;letter-spacing:-2px;line-height:1;">--:--:--</div>
        <div id="fecha" style="font-size:12px;color:#64748b;margin-top:5px;
             font-family:'Inter',system-ui;font-weight:500;letter-spacing:0.2px;">—</div>
      </div>
      <div style="height:54px;width:1px;background:#e2e8f0;flex-shrink:0;"></div>
      <div style="font-family:'Inter',system-ui;">
        <div style="font-weight:700;color:#0f172a;font-size:14px;letter-spacing:-0.2px;">Sistema Activo</div>
        <div style="font-size:11px;color:#64748b;margin-top:2px;">RRHH Executive Pro · Plataforma Corporativa</div>
        <div style="margin-top:8px;">
          <span style="background:#f0fdf4;color:#15803d;padding:2px 10px;border-radius:5px;
                font-size:10px;font-weight:700;letter-spacing:0.6px;border:1px solid #bbf7d0;">
            ● EN LÍNEA
          </span>
        </div>
      </div>
    </div>
    <script>
    const D=["Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado"];
    const M=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"];
    function tick(){const n=new Date();
      document.getElementById("hora").textContent=String(n.getHours()).padStart(2,"0")+":"+String(n.getMinutes()).padStart(2,"0")+":"+String(n.getSeconds()).padStart(2,"0");
      document.getElementById("fecha").textContent=D[n.getDay()]+" "+n.getDate()+" de "+M[n.getMonth()]+" de "+n.getFullYear();}
    tick();setInterval(tick,1000);
    </script>""", height=112)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    df_emp = obtener_empleados()
    cursor.execute("SELECT COALESCE(SUM(dias_consumidos),0) FROM vacaciones")
    total_vac = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM turnos")
    n_turnos = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(DISTINCT empleado_id) FROM vacaciones")
    emp_vac = cursor.fetchone()[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Empleados",       len(df_emp),  "Activos")
    col2.metric("Días Vacaciones", total_vac,    "Consumidos")
    col3.metric("Turnos",          n_turnos,     "Registrados")
    col4.metric("Con Vacaciones",  emp_vac,      "Empleados")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:12px;">Módulos del Sistema</div>', unsafe_allow_html=True)
        modulos = [
            ("#dbeafe","#1d4ed8","📊","Dashboard",  "Centro de control ejecutivo"),
            ("#ede9fe","#5b21b6","👤","Empleados",  "Registro y administración del personal"),
            ("#d1fae5","#065f46","📅","Vacaciones", "Control legal de descanso con festivos"),
            ("#fce7f3","#9d174d","⏱","Turnos",     "Gestión operacional 24H de turnos"),
            ("#fef3c7","#92400e","📈","Reportes",   "Analytics, gráficos y exportación CSV"),
        ]
        for bg, fg, ico, nom, desc in modulos:
            st.markdown(f"""
            <div class="nav-item">
              <div style="width:36px;height:36px;border-radius:10px;background:{bg};color:{fg};
                   display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;">{ico}</div>
              <div>
                <div style="font-weight:700;color:#0f172a;font-size:13px;">{nom}</div>
                <div style="font-size:12px;color:#64748b;margin-top:2px;">{desc}</div>
              </div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:12px;">Características del Sistema</div>', unsafe_allow_html=True)
        feats = [
            "Gestión integral de Recursos Humanos",
            "Cálculo automático de días hábiles y festivos",
            "Control legal de descanso — Código del Trabajo",
            "Turnos operacionales configurables 24H",
            "Base de datos SQLite local y segura",
            "Analytics en tiempo real con gráficos",
            "Exportación de reportes en formato CSV",
            "Acceso protegido con autenticación",
            "Prevención de fatiga laboral",
        ]
        rows = "".join([
            f'<div style="display:flex;align-items:center;gap:10px;padding:8px 0;'
            f'border-bottom:1px solid #f8fafc;font-size:13px;color:#374151;">'
            f'<span style="color:#16a34a;font-size:14px;flex-shrink:0;">✓</span>{t}</div>'
            for t in feats])
        st.markdown(f'<div class="card" style="padding:16px 20px;">{rows}</div>', unsafe_allow_html=True)

# =========================================================
# EMPLEADOS
# =========================================================

elif menu == "Empleados":

    render_banner("banner-empleados",
        "Gestión de Empleados",
        "Registro, consulta y administración integral del personal de la empresa",
        "RRHH · Directorio")

    tab1, tab2 = st.tabs(["  Nuevo Empleado  ", "  Directorio y Administración  "])

    with tab1:
        with st.form("form_empleado"):
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre completo *", placeholder="Ej: Juan Pérez González")
            with col2:
                cargo  = st.text_input("Cargo / Función", placeholder="Ej: Jefe de Operaciones")
            dias = st.number_input("Días de vacaciones asignados", min_value=0, max_value=60, step=1, value=15)
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            if st.form_submit_button("Registrar Empleado", use_container_width=True):
                if not nombre.strip():
                    st.error("El nombre es obligatorio.")
                else:
                    cursor.execute("INSERT INTO empleados (nombre,cargo,dias_vacaciones) VALUES (?,?,?)",
                                   (nombre.strip(), cargo.strip(), dias))
                    conn.commit()
                    st.success(f"Empleado **{nombre.strip()}** registrado correctamente.")
                    st.rerun()

    with tab2:
        df = obtener_empleados()
        if df.empty:
            st.info("No hay empleados registrados.")
        else:
            resumen = []
            for _, row in df.iterrows():
                t, c, s = obtener_resumen_vacaciones(row["id"])
                resumen.append({"ID": row["id"], "Nombre": row["nombre"], "Cargo": row["cargo"],
                                "Total": t, "Consumidos": c, "Saldo": s})
            df_r = pd.DataFrame(resumen)
            st.markdown(f'<div style="font-size:12px;color:#64748b;margin-bottom:8px;"><b>{len(df_r)}</b> empleado(s)</div>', unsafe_allow_html=True)
            st.dataframe(df_r, use_container_width=True, hide_index=True)
            st.divider()
            st.markdown('<div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:8px;">Eliminar Empleado</div>', unsafe_allow_html=True)
            st.caption("Se eliminarán también sus registros de vacaciones y turnos.")
            col1, col2 = st.columns([3, 1])
            with col1:
                ops = {f"{r['Nombre']}  —  {r['Cargo']}": r["ID"] for _, r in df_r.iterrows()}
                sel = st.selectbox("Seleccionar", list(ops.keys()), label_visibility="collapsed")
            with col2:
                if st.button("Eliminar", type="secondary", use_container_width=True):
                    eid = ops[sel]
                    cursor.execute("DELETE FROM empleados  WHERE id=?", (eid,))
                    cursor.execute("DELETE FROM vacaciones WHERE empleado_id=?", (eid,))
                    cursor.execute("DELETE FROM turnos     WHERE empleado_id=?", (eid,))
                    conn.commit()
                    st.success("Empleado eliminado.")
                    st.rerun()

# =========================================================
# VACACIONES
# =========================================================

elif menu == "Vacaciones":

    render_banner("banner-vacaciones",
        "Control de Vacaciones",
        "Administración legal de descanso · Cálculo automático de días hábiles y festivos nacionales",
        "Código del Trabajo · Chile")

    df_emp = obtener_empleados()

    if df_emp.empty:
        st.warning("No hay empleados registrados.")
    else:
        emp_nom = st.selectbox("Seleccionar trabajador", df_emp["nombre"])
        emp     = df_emp[df_emp["nombre"] == emp_nom].iloc[0]
        emp_id  = int(emp["id"])
        total, consumidos, saldo = obtener_resumen_vacaciones(emp_id)

        col1, col2, col3 = st.columns(3)
        col1.metric("Días Totales",     total)
        col2.metric("Consumidos",       consumidos)
        col3.metric("Saldo Disponible", saldo,
                    "Disponible" if saldo > 0 else "Sin saldo",
                    delta_color="normal" if saldo > 0 else "inverse")

        st.divider()
        tab1, tab2 = st.tabs(["  Solicitar Vacaciones  ", "  Historial  "])

        with tab1:
            if saldo <= 0:
                st.error("Sin saldo de vacaciones disponible.")
            else:
                with st.form("form_vacaciones"):
                    col1, col2 = st.columns(2)
                    with col1: fecha_inicio = st.date_input("Fecha de inicio")
                    with col2: dias_sol = st.number_input("Días hábiles", min_value=1, max_value=int(saldo), step=1, value=1)
                    fecha_fin = calcular_fecha_fin(fecha_inicio, dias_sol)
                    st.info(f"Término calculado: **{fecha_fin.strftime('%d de %B de %Y')}**  ·  {dias_sol} días hábiles  ·  Excluye festivos")
                    if st.form_submit_button("Registrar Vacaciones", use_container_width=True):
                        cursor.execute("INSERT INTO vacaciones (empleado_id,fecha_inicio,fecha_fin,dias_consumidos) VALUES (?,?,?,?)",
                                       (emp_id, str(fecha_inicio), str(fecha_fin), dias_sol))
                        conn.commit()
                        st.success(f"Vacaciones registradas: {fecha_inicio} → {fecha_fin}  ·  {dias_sol} días")
                        st.rerun()

        with tab2:
            df_h = pd.read_sql_query(
                "SELECT id,fecha_inicio,fecha_fin,dias_consumidos FROM vacaciones WHERE empleado_id=? ORDER BY fecha_inicio DESC",
                conn, params=(emp_id,))
            if df_h.empty:
                st.info("Sin historial de vacaciones.")
            else:
                df_h.columns = ["ID","Inicio","Término","Días"]
                st.dataframe(df_h, use_container_width=True, hide_index=True)
                with st.expander("Eliminar registro"):
                    id_el = st.number_input("ID del registro", min_value=1, step=1)
                    if st.button("Eliminar registro", key="del_vac"):
                        cursor.execute("DELETE FROM vacaciones WHERE id=? AND empleado_id=?", (id_el, emp_id))
                        conn.commit()
                        st.success("Registro eliminado.")
                        st.rerun()

# =========================================================
# TURNOS
# =========================================================

elif menu == "Turnos":

    render_banner("banner-turnos",
        "Gestión de Turnos 24H",
        "Asignación y control de turnos operacionales · Prevención de fatiga laboral",
        "Módulo Operacional")

    TIPOS = {
        "Turno Día  (07:00 – 19:00)":   "Turno Día",
        "Turno Noche  (19:00 – 07:00)": "Turno Noche",
        "Guardia 24H  (00:00 – 24:00)": "Guardia 24H",
        "Día Libre / Descanso":          "Día Libre",
    }
    COLORES = {
        "Turno Día":   ("#dbeafe","#1d4ed8"),
        "Turno Noche": ("#ede9fe","#5b21b6"),
        "Guardia 24H": ("#fce7f3","#9d174d"),
        "Día Libre":   ("#dcfce7","#15803d"),
    }

    df_emp = obtener_empleados()

    if df_emp.empty:
        st.warning("No hay empleados registrados.")
    else:
        tab1, tab2 = st.tabs(["  Asignar Turno  ", "  Turnos Registrados  "])

        with tab1:
            with st.form("form_turno"):
                col1, col2 = st.columns(2)
                with col1:
                    emp_sel    = st.selectbox("Empleado", df_emp["nombre"])
                    tipo_label = st.selectbox("Tipo de turno", list(TIPOS.keys()))
                with col2:
                    f_ini = st.date_input("Fecha inicio", key="ti")
                    f_fin = st.date_input("Fecha fin",    key="tf")
                tipo_val = TIPOS[tipo_label]
                bg, fg   = COLORES[tipo_val]
                st.markdown(f'<div style="display:inline-flex;align-items:center;background:{bg};color:{fg};'
                            f'padding:5px 14px;border-radius:7px;font-size:13px;font-weight:700;margin-top:5px;">'
                            f'Turno seleccionado: {tipo_val}</div>', unsafe_allow_html=True)
                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
                if st.form_submit_button("Asignar Turno", use_container_width=True):
                    if f_fin < f_ini:
                        st.error("La fecha fin no puede ser anterior al inicio.")
                    else:
                        emp_id = int(df_emp[df_emp["nombre"]==emp_sel].iloc[0]["id"])
                        cursor.execute("INSERT INTO turnos (empleado_id,fecha_inicio,fecha_fin,tipo_turno) VALUES (?,?,?,?)",
                                       (emp_id, str(f_ini), str(f_fin), tipo_val))
                        conn.commit()
                        d = (f_fin - f_ini).days + 1
                        st.success(f"Turno **{tipo_val}** asignado a **{emp_sel}** · {f_ini} → {f_fin} · {d} día(s)")
                        st.rerun()

        with tab2:
            df_t = pd.read_sql_query(
                "SELECT t.id,e.nombre AS Empleado,t.tipo_turno AS Turno,t.fecha_inicio AS Inicio,t.fecha_fin AS Fin "
                "FROM turnos t JOIN empleados e ON t.empleado_id=e.id ORDER BY t.fecha_inicio DESC", conn)
            if df_t.empty:
                st.info("No hay turnos registrados.")
            else:
                col1, col2 = st.columns(2)
                with col1: fil_e = st.selectbox("Filtrar empleado", ["Todos"]+df_emp["nombre"].tolist(), key="fe")
                with col2: fil_t = st.selectbox("Filtrar turno",    ["Todos"]+list(TIPOS.values()),       key="ft")
                df_v = df_t.copy()
                if fil_e != "Todos": df_v = df_v[df_v["Empleado"]==fil_e]
                if fil_t != "Todos": df_v = df_v[df_v["Turno"]==fil_t]
                st.markdown(f'<div style="font-size:12px;color:#64748b;margin-bottom:8px;"><b>{len(df_v)}</b> turno(s)</div>', unsafe_allow_html=True)
                st.dataframe(df_v, use_container_width=True, hide_index=True)
                with st.expander("Eliminar turno"):
                    id_t = st.number_input("ID del turno", min_value=1, step=1)
                    if st.button("Eliminar turno", key="del_t"):
                        cursor.execute("DELETE FROM turnos WHERE id=?", (id_t,))
                        conn.commit()
                        st.success("Turno eliminado.")
                        st.rerun()

# =========================================================
# REPORTES
# =========================================================

elif menu == "Reportes":

    render_banner("banner-reportes",
        "Reportes y Analytics",
        "Visualización ejecutiva · Vacaciones · Turnos · Personal · Exportación de datos",
        "Business Intelligence")

    df_emp = obtener_empleados()

    if df_emp.empty:
        st.warning("Sin datos para reportar.")
    else:
        cursor.execute("SELECT COUNT(*) FROM empleados")
        ne = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(SUM(dias_consumidos),0) FROM vacaciones")
        tv = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM turnos")
        nt = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(DISTINCT empleado_id) FROM vacaciones")
        ev = cursor.fetchone()[0]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Empleados",      ne)
        col2.metric("Días Vacac. Usados",   tv)
        col3.metric("Total Turnos",         nt)
        col4.metric("Empl. con Vacaciones", ev)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:12px;">Vacaciones por Empleado</div>', unsafe_allow_html=True)
            dv = []
            for _, row in df_emp.iterrows():
                t, c, s = obtener_resumen_vacaciones(row["id"])
                dv.append({"Empleado": row["nombre"], "Consumidos": c, "Saldo": s})
            df_vc = pd.DataFrame(dv)
            if PLOTLY:
                fig = go.Figure()
                fig.add_trace(go.Bar(name="Consumidos", x=df_vc["Empleado"], y=df_vc["Consumidos"],
                                     marker_color="#1d4ed8", marker_line_width=0))
                fig.add_trace(go.Bar(name="Saldo",      x=df_vc["Empleado"], y=df_vc["Saldo"],
                                     marker_color="#10b981", marker_line_width=0))
                fig.update_layout(barmode="stack", height=300,
                                  plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                  margin=dict(l=0,r=0,t=10,b=0),
                                  legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                                  font=dict(family="Inter,system-ui",size=12))
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.bar_chart(df_vc.set_index("Empleado"))

        with col2:
            st.markdown('<div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:12px;">Distribución de Turnos</div>', unsafe_allow_html=True)
            cursor.execute("SELECT tipo_turno, COUNT(*) FROM turnos GROUP BY tipo_turno")
            rt = cursor.fetchall()
            if rt:
                df_pie = pd.DataFrame(rt, columns=["Tipo","Total"])
                if PLOTLY:
                    fig2 = px.pie(df_pie, values="Total", names="Tipo", hole=0.46,
                                  color_discrete_sequence=["#1d4ed8","#5b21b6","#9d174d","#15803d"])
                    fig2.update_traces(textposition="inside", textinfo="percent+label",
                                       textfont_size=12,
                                       marker=dict(line=dict(color="white",width=2)))
                    fig2.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)",
                                       margin=dict(l=0,r=0,t=10,b=0), showlegend=False,
                                       font=dict(family="Inter,system-ui",size=12))
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.dataframe(df_pie, use_container_width=True, hide_index=True)
            else:
                st.info("Sin turnos para graficar.")

        st.divider()
        st.markdown('<div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:12px;">Resumen Ejecutivo</div>', unsafe_allow_html=True)

        df_full = []
        for _, row in df_emp.iterrows():
            t, c, s = obtener_resumen_vacaciones(row["id"])
            cursor.execute("SELECT COUNT(*) FROM turnos WHERE empleado_id=?", (row["id"],))
            nti = cursor.fetchone()[0]
            df_full.append({"Nombre": row["nombre"], "Cargo": row["cargo"],
                            "Total": t, "Consumidos": c, "Saldo": s, "Turnos": nti})
        df_fd = pd.DataFrame(df_full)
        st.dataframe(df_fd, use_container_width=True, hide_index=True)

        csv = df_fd.to_csv(index=False).encode("utf-8")
        st.download_button("Exportar Reporte CSV", csv,
                           f"reporte_rrhh_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", "text/csv")

# =========================================================
# SIDEBAR FOOTER
# =========================================================

st.sidebar.markdown("""
<div style="height:1px;background:rgba(255,255,255,0.06);margin:14px 10px;"></div>
<div style="padding:14px 16px;background:rgba(255,255,255,0.04);border-radius:12px;
     border:1px solid rgba(255,255,255,0.06);text-align:center;margin:0 4px;">
  <div style="font-size:12px;font-weight:700;color:rgba(255,255,255,0.6);">RRHH Executive Pro</div>
  <div style="font-size:10px;color:rgba(255,255,255,0.28);margin-top:3px;letter-spacing:0.5px;">
    v8.2 · Corporativo · Confidencial
  </div>
</div>
""", unsafe_allow_html=True)
