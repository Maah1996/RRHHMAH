# =========================================================
# SISTEMA RRHH EMPRESARIAL v8.1 EXECUTIVE PRO
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

# =========================================================
# CSS ENTERPRISE PROFESIONAL
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after {
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    box-sizing: border-box;
}

/* ── APP BACKGROUND ── */
.stApp {
    background: #f1f5f9;
    background-image:
        url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%2394a3b8' fill-opacity='0.07' fill-rule='evenodd'%3E%3Ccircle cx='20' cy='20' r='1'/%3E%3C/g%3E%3C/svg%3E"),
        linear-gradient(160deg, #eef2ff 0%, #f1f5f9 50%, #f0fdf4 100%);
}

/* ══════════════════════════════════════════
   SIDEBAR ENTERPRISE
══════════════════════════════════════════ */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,
        #0a0f1e 0%,
        #0f172a 40%,
        #131f35 100%
    ) !important;
    border-right: 1px solid rgba(255,255,255,0.04) !important;
    width: 260px !important;
}

section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Ocultar los puntos/círculos del radio button */
section[data-testid="stSidebar"] .stRadio label > div:first-child {
    display: none !important;
}

/* Eliminar el punto de selección predeterminado de Streamlit */
section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
    display: none !important;
}

/* Contenedor del radio group */
section[data-testid="stSidebar"] .stRadio > div {
    gap: 2px !important;
}

/* Cada ítem del menú */
section[data-testid="stSidebar"] .stRadio label {
    border-radius: 10px !important;
    padding: 11px 16px !important;
    margin: 1px 0 !important;
    transition: all 0.2s ease !important;
    border: 1px solid transparent !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.07) !important;
    border-color: rgba(255,255,255,0.08) !important;
    color: white !important;
}

/* Ítem seleccionado — usa :has() para detectar radio checked */
section[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: rgba(37,99,235,0.20) !important;
    border-color: rgba(37,99,235,0.40) !important;
    border-left: 3px solid #3b82f6 !important;
    padding-left: 14px !important;
}

section[data-testid="stSidebar"] .stRadio label:has(input:checked) p {
    color: #93c5fd !important;
    font-weight: 600 !important;
}

/* Ocultar label del radio group */
section[data-testid="stSidebar"] .stRadio > label {
    display: none !important;
}

/* Texto del ítem de menú */
section[data-testid="stSidebar"] .stRadio label p {
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
    margin: 0 !important;
    letter-spacing: 0.1px !important;
}

/* ══════════════════════════════════════════
   BOTONES
══════════════════════════════════════════ */

.stButton > button {
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: 0.2px !important;
    box-shadow: 0 2px 8px rgba(29,78,216,0.30) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(29,78,216,0.38) !important;
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
}

.stButton > button[kind="secondary"] {
    background: linear-gradient(135deg, #b91c1c, #991b1b) !important;
    box-shadow: 0 2px 8px rgba(185,28,28,0.28) !important;
}

/* ══════════════════════════════════════════
   MÉTRICAS
══════════════════════════════════════════ */

div[data-testid="metric-container"] {
    background: white !important;
    border-radius: 16px !important;
    padding: 24px 22px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 6px rgba(15,23,42,0.06) !important;
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
    box-shadow: 0 8px 24px rgba(15,23,42,0.10) !important;
}

div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    color: #64748b !important;
}

div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 30px !important;
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
    padding: 28px 32px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 6px rgba(15,23,42,0.05) !important;
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
   DATAFRAME / TABLA
══════════════════════════════════════════ */

[data-testid="stDataFrame"] {
    background: white !important;
    border-radius: 14px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 6px rgba(15,23,42,0.04) !important;
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
    padding: 8px 18px !important;
}

.stTabs [aria-selected="true"] {
    background: white !important;
    box-shadow: 0 1px 6px rgba(15,23,42,0.08) !important;
    color: #1d4ed8 !important;
}

/* ══════════════════════════════════════════
   EXPANDER
══════════════════════════════════════════ */

[data-testid="stExpander"] {
    background: white !important;
    border-radius: 12px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 4px rgba(15,23,42,0.04) !important;
}

/* ══════════════════════════════════════════
   DIVIDER
══════════════════════════════════════════ */

hr {
    border: none !important;
    border-top: 1px solid #e2e8f0 !important;
    margin: 24px 0 !important;
}

/* ══════════════════════════════════════════
   BANNERS DE MÓDULO
══════════════════════════════════════════ */

.module-banner {
    border-radius: 20px;
    padding: 44px 56px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    color: white;
}

.module-banner .geo1 {
    position: absolute;
    width: 480px; height: 480px;
    border-radius: 50%;
    background: radial-gradient(rgba(255,255,255,0.08), transparent 68%);
    top: -220px; right: -100px;
    pointer-events: none;
}

.module-banner .geo2 {
    position: absolute;
    width: 280px; height: 280px;
    border-radius: 50%;
    background: radial-gradient(rgba(255,255,255,0.05), transparent 70%);
    bottom: -140px; left: -70px;
    pointer-events: none;
}

.module-banner .pattern {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
}

.module-banner .banner-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 6px;
    padding: 4px 14px;
    font-size: 11px;
    font-weight: 700;
    color: rgba(255,255,255,0.85);
    margin-bottom: 16px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    position: relative;
    z-index: 2;
}

.module-banner h1 {
    color: white !important;
    font-size: 36px !important;
    font-weight: 800 !important;
    letter-spacing: -1px !important;
    margin: 0 0 8px 0 !important;
    position: relative;
    z-index: 2;
    line-height: 1.1 !important;
}

.module-banner p {
    color: rgba(255,255,255,0.62) !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    margin: 0 !important;
    position: relative;
    z-index: 2;
    line-height: 1.6 !important;
    letter-spacing: 0.1px;
}

/* Colores por módulo */
.banner-dashboard  { background: linear-gradient(135deg, #0a0e27 0%, #0e1f5e 45%, #1a3a9f 75%, #1d4ed8 100%); }
.banner-empleados  { background: linear-gradient(135deg, #060d28 0%, #0c1e5a 45%, #134090 75%, #1558b0 100%); }
.banner-vacaciones { background: linear-gradient(135deg, #011c12 0%, #044a30 45%, #065f46 75%, #047857 100%); }
.banner-turnos     { background: linear-gradient(135deg, #120326 0%, #2a0860 45%, #4a1a95 75%, #5b21b6 100%); }
.banner-reportes   { background: linear-gradient(135deg, #1a0700 0%, #431407 45%, #7c2d12 75%, #b45309 100%); }

/* ══════════════════════════════════════════
   CARD
══════════════════════════════════════════ */

.card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 6px rgba(15,23,42,0.05);
    margin-bottom: 16px;
    transition: box-shadow 0.2s ease;
}

.card:hover {
    box-shadow: 0 6px 24px rgba(15,23,42,0.08);
}

/* ══════════════════════════════════════════
   NAV ITEMS (filas de módulos en Dashboard)
══════════════════════════════════════════ */

.nav-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 16px;
    background: #f8fafc;
    border-radius: 12px;
    margin-bottom: 8px;
    border: 1px solid #e2e8f0;
    transition: all 0.18s;
}

.nav-item:hover {
    background: #eff6ff;
    border-color: #bfdbfe;
}

.nav-item-icon {
    width: 38px; height: 38px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 17px;
    flex-shrink: 0;
}

/* ══════════════════════════════════════════
   LOGIN
══════════════════════════════════════════ */

.login-card {
    background: white;
    border-radius: 24px;
    padding: 48px 44px;
    box-shadow:
        0 20px 60px rgba(15,23,42,0.12),
        0 0 0 1px rgba(226,232,240,0.6);
    max-width: 420px;
    margin: 56px auto 0;
}

/* ══════════════════════════════════════════
   ALERTAS
══════════════════════════════════════════ */

.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 12px !important;
    font-size: 14px !important;
}

/* ══════════════════════════════════════════
   SELECTBOX
══════════════════════════════════════════ */

[data-baseweb="select"] {
    border-radius: 10px !important;
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
          <div style="text-align:center; margin-bottom:32px;">
            <div style="
                width:64px; height:64px;
                background:linear-gradient(135deg,#1d4ed8,#1e40af);
                border-radius:16px;
                display:flex; align-items:center; justify-content:center;
                font-size:28px; margin:0 auto 18px;
                box-shadow:0 6px 20px rgba(29,78,216,0.30);
            ">🏢</div>
            <div style="font-size:22px; font-weight:800; color:#0f172a; letter-spacing:-0.5px;">
                RRHH Executive Pro
            </div>
            <div style="font-size:13px; color:#64748b; margin-top:5px; font-weight:400;">
                Plataforma Corporativa de Recursos Humanos
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        usuario = st.text_input("Usuario", placeholder="Ingrese su usuario")
        clave   = st.text_input("Contraseña", type="password", placeholder="••••••••")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("Ingresar al Sistema", use_container_width=True):
            if usuario == USUARIO_ADMIN and clave == CLAVE_ADMIN:
                st.session_state.login_correcto = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas. Verifique usuario y contraseña.")

        st.markdown("""
        <div style="text-align:center; margin-top:20px; color:#94a3b8; font-size:12px; letter-spacing:0.3px;">
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
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS empleados (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre          TEXT NOT NULL,
        cargo           TEXT,
        dias_vacaciones INTEGER DEFAULT 15
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacaciones (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        empleado_id     INTEGER,
        fecha_inicio    TEXT,
        fecha_fin       TEXT,
        dias_consumidos INTEGER
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS turnos (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        empleado_id     INTEGER,
        fecha_inicio    TEXT,
        fecha_fin       TEXT,
        tipo_turno      TEXT
    )""")
    conn.commit()

crear_tablas()

# =========================================================
# FUNCIONES
# =========================================================

def obtener_empleados():
    return pd.read_sql_query(
        "SELECT * FROM empleados ORDER BY nombre", conn
    )

def calcular_fecha_fin(fecha_inicio, dias_solicitados):
    chile_holidays = holidays.Chile()
    fecha_actual   = fecha_inicio
    dias           = 0
    while dias < dias_solicitados:
        if fecha_actual.weekday() < 5 and fecha_actual not in chile_holidays:
            dias += 1
        if dias < dias_solicitados:
            fecha_actual += timedelta(days=1)
    return fecha_actual

def obtener_resumen_vacaciones(empleado_id):
    cursor.execute("SELECT dias_vacaciones FROM empleados WHERE id = ?", (empleado_id,))
    r = cursor.fetchone()
    if r is None:
        return 0, 0, 0
    total = r[0]
    cursor.execute(
        "SELECT COALESCE(SUM(dias_consumidos),0) FROM vacaciones WHERE empleado_id = ?",
        (empleado_id,)
    )
    consumidos = cursor.fetchone()[0]
    return total, consumidos, total - consumidos

def render_banner(css_class, icon, title, subtitle, badge=""):
    badge_html = (
        f'<div class="banner-badge">{badge}</div>' if badge else ""
    )
    st.markdown(f"""
    <div class="module-banner {css_class}">
        <div class="geo1"></div><div class="geo2"></div><div class="pattern"></div>
        {badge_html}
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("""
<div style="padding:24px 12px 8px;">
    <div style="display:flex; align-items:center; gap:11px;">
        <div style="
            width:38px; height:38px;
            background:linear-gradient(135deg,#1d4ed8,#1e40af);
            border-radius:11px;
            display:flex; align-items:center; justify-content:center;
            font-size:18px;
            box-shadow:0 3px 10px rgba(29,78,216,0.4);
            flex-shrink:0;
        ">🏢</div>
        <div>
            <div style="font-size:15px; font-weight:800; color:white; letter-spacing:-0.2px;">RRHH Pro</div>
            <div style="font-size:10px; color:rgba(255,255,255,0.38); letter-spacing:1px; text-transform:uppercase; margin-top:1px;">Executive Suite</div>
        </div>
    </div>
</div>
<div style="height:1px; background:rgba(255,255,255,0.07); margin:12px 12px 16px;"></div>
<div style="padding:0 12px 6px; font-size:10px; font-weight:700; color:rgba(255,255,255,0.28); letter-spacing:1.5px; text-transform:uppercase;">
    Navegación
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "menu",
    [
        "Dashboard",
        "Empleados",
        "Vacaciones",
        "Turnos",
        "Reportes"
    ],
    label_visibility="collapsed"
)

# =========================================================
# DASHBOARD
# =========================================================

if menu == "Dashboard":

    render_banner(
        "banner-dashboard",
        "",
        "Sistema de Gestión RRHH",
        "Plataforma Ejecutiva · Recursos Humanos · Turnos Operacionales · Prevención Laboral",
        "Executive Suite v8.1"
    )

    # Reloj en tiempo real
    components.html("""
    <div style="
        background:white;
        border-radius:16px;
        padding:20px 28px;
        border:1px solid #e2e8f0;
        box-shadow:0 1px 6px rgba(15,23,42,0.06);
        margin-bottom:4px;
        display:flex;
        align-items:center;
        gap:24px;
    ">
        <div style="border-left:3px solid #1d4ed8; padding-left:18px;">
            <div id="hora" style="
                font-size:38px;
                font-weight:900;
                color:#1d4ed8;
                font-family:'Inter',system-ui;
                letter-spacing:-2px;
                line-height:1;
            ">--:--:--</div>
            <div id="fecha" style="
                font-size:13px;
                color:#64748b;
                margin-top:6px;
                font-family:'Inter',system-ui;
                font-weight:500;
                letter-spacing:0.2px;
            ">—</div>
        </div>
        <div style="height:60px; width:1px; background:#e2e8f0; flex-shrink:0;"></div>
        <div style="font-family:'Inter',system-ui;">
            <div style="font-weight:700; color:#0f172a; font-size:15px; letter-spacing:-0.2px;">Sistema Activo</div>
            <div style="font-size:12px; color:#64748b; margin-top:3px;">RRHH Executive Pro · Plataforma Corporativa</div>
            <div style="margin-top:10px;">
                <span style="
                    background:#f0fdf4; color:#15803d;
                    padding:3px 10px; border-radius:5px;
                    font-size:11px; font-weight:700; letter-spacing:0.5px;
                    border:1px solid #bbf7d0;
                ">● EN LÍNEA</span>
            </div>
        </div>
    </div>
    <script>
    const D=["Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado"];
    const M=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"];
    function tick(){
        const n=new Date();
        document.getElementById("hora").textContent=
            String(n.getHours()).padStart(2,"0")+":"+
            String(n.getMinutes()).padStart(2,"0")+":"+
            String(n.getSeconds()).padStart(2,"0");
        document.getElementById("fecha").textContent=
            D[n.getDay()]+" "+n.getDate()+" de "+M[n.getMonth()]+" de "+n.getFullYear();
    }
    tick(); setInterval(tick,1000);
    </script>
    """, height=120)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Métricas reales
    df_emp = obtener_empleados()
    cursor.execute("SELECT COALESCE(SUM(dias_consumidos),0) FROM vacaciones")
    total_vac = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM turnos")
    n_turnos = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(DISTINCT empleado_id) FROM vacaciones")
    emp_vac = cursor.fetchone()[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Empleados",          len(df_emp),  "Activos")
    col2.metric("Días Vacaciones",     total_vac,    "Consumidos")
    col3.metric("Turnos",             n_turnos,     "Registrados")
    col4.metric("Con Vacaciones",     emp_vac,      "Empleados")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="font-size:15px; font-weight:700; color:#0f172a; margin-bottom:14px; letter-spacing:-0.2px;">
            Módulos del Sistema
        </div>
        """, unsafe_allow_html=True)
        modulos = [
            ("#dbeafe","#1d4ed8","📊","Dashboard","Centro de control y monitoreo ejecutivo"),
            ("#ede9fe","#5b21b6","👤","Empleados","Registro y administración del personal"),
            ("#d1fae5","#065f46","📅","Vacaciones","Control legal de descanso con festivos"),
            ("#fce7f3","#9d174d","⏱","Turnos","Gestión operacional 24H de turnos"),
            ("#fef3c7","#92400e","📈","Reportes","Analytics, gráficos y exportación CSV"),
        ]
        for bg, fg, ico, nombre, desc in modulos:
            st.markdown(f"""
            <div class="nav-item">
                <div class="nav-item-icon" style="background:{bg}; color:{fg};">{ico}</div>
                <div>
                    <div style="font-weight:700; color:#0f172a; font-size:14px;">{nombre}</div>
                    <div style="font-size:12px; color:#64748b; margin-top:2px;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="font-size:15px; font-weight:700; color:#0f172a; margin-bottom:14px; letter-spacing:-0.2px;">
            Características del Sistema
        </div>
        """, unsafe_allow_html=True)
        features = [
            "Gestión integral de Recursos Humanos",
            "Cálculo automático de días hábiles y festivos",
            "Control legal de descanso — Código del Trabajo",
            "Turnos operacionales configurables 24H",
            "Base de datos SQLite local y segura",
            "Analytics en tiempo real con gráficos",
            "Exportación de reportes en CSV",
            "Acceso protegido con autenticación",
            "Prevención de fatiga laboral",
        ]
        rows = "".join([
            f'<div style="display:flex;align-items:center;gap:10px;padding:9px 0;'
            f'border-bottom:1px solid #f8fafc;font-size:13px;color:#374151;">'
            f'<span style="color:#16a34a;font-size:15px;flex-shrink:0;">✓</span>{t}</div>'
            for t in features
        ])
        st.markdown(f'<div class="card" style="padding:18px 22px;">{rows}</div>', unsafe_allow_html=True)

# =========================================================
# EMPLEADOS
# =========================================================

elif menu == "Empleados":

    render_banner(
        "banner-empleados", "",
        "Gestión de Empleados",
        "Registro, consulta y administración integral del personal de la empresa",
        "RRHH · Directorio de Personal"
    )

    tab1, tab2 = st.tabs(["  Nuevo Empleado  ", "  Directorio y Administración  "])

    with tab1:
        with st.form("form_empleado"):
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre completo *", placeholder="Ej: Juan Pérez González")
            with col2:
                cargo = st.text_input("Cargo / Función", placeholder="Ej: Jefe de Operaciones")

            dias = st.number_input(
                "Días de vacaciones legales asignados",
                min_value=0, max_value=60, step=1, value=15
            )
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

            if st.form_submit_button("Registrar Empleado", use_container_width=True):
                if not nombre.strip():
                    st.error("El nombre del empleado es obligatorio.")
                else:
                    cursor.execute(
                        "INSERT INTO empleados (nombre, cargo, dias_vacaciones) VALUES (?, ?, ?)",
                        (nombre.strip(), cargo.strip(), dias)
                    )
                    conn.commit()
                    st.success(f"Empleado **{nombre.strip()}** registrado correctamente.")
                    st.rerun()

    with tab2:
        df = obtener_empleados()
        if df.empty:
            st.info("No hay empleados registrados. Use la pestaña **Nuevo Empleado**.")
        else:
            resumen = []
            for _, row in df.iterrows():
                total, consumidos, saldo = obtener_resumen_vacaciones(row["id"])
                resumen.append({
                    "ID": row["id"], "Nombre": row["nombre"], "Cargo": row["cargo"],
                    "Vacac. Total": total, "Consumidos": consumidos, "Saldo": saldo,
                })
            df_r = pd.DataFrame(resumen)
            st.markdown(
                f'<div style="font-size:13px;color:#64748b;margin-bottom:10px;">'
                f'<b>{len(df_r)}</b> empleado(s) registrado(s)</div>',
                unsafe_allow_html=True
            )
            st.dataframe(df_r, use_container_width=True, hide_index=True)

            st.divider()
            st.markdown(
                '<div style="font-size:15px;font-weight:700;color:#0f172a;margin-bottom:10px;">Eliminar Empleado</div>',
                unsafe_allow_html=True
            )
            st.caption("Se eliminarán también los registros de vacaciones y turnos asociados.")
            col1, col2 = st.columns([3, 1])
            with col1:
                opciones = {f"{r['Nombre']}  —  {r['Cargo']}": r["ID"] for _, r in df_r.iterrows()}
                sel = st.selectbox("Seleccionar", list(opciones.keys()), label_visibility="collapsed")
            with col2:
                if st.button("Eliminar", type="secondary", use_container_width=True):
                    eid = opciones[sel]
                    cursor.execute("DELETE FROM empleados  WHERE id=?",          (eid,))
                    cursor.execute("DELETE FROM vacaciones WHERE empleado_id=?", (eid,))
                    cursor.execute("DELETE FROM turnos     WHERE empleado_id=?", (eid,))
                    conn.commit()
                    st.success("Empleado eliminado correctamente.")
                    st.rerun()

# =========================================================
# VACACIONES
# =========================================================

elif menu == "Vacaciones":

    render_banner(
        "banner-vacaciones", "",
        "Control de Vacaciones",
        "Administración legal de descanso · Cálculo automático de días hábiles y festivos nacionales",
        "Código del Trabajo · Chile"
    )

    df_emp = obtener_empleados()

    if df_emp.empty:
        st.warning("No hay empleados registrados. Agregue empleados primero.")
    else:
        empleado_nombre = st.selectbox("Seleccionar trabajador", df_emp["nombre"])
        empleado    = df_emp[df_emp["nombre"] == empleado_nombre].iloc[0]
        empleado_id = int(empleado["id"])

        total, consumidos, saldo = obtener_resumen_vacaciones(empleado_id)

        col1, col2, col3 = st.columns(3)
        col1.metric("Días Totales",      total)
        col2.metric("Consumidos",        consumidos)
        col3.metric("Saldo Disponible",  saldo,
                    "Disponible" if saldo > 0 else "Sin saldo",
                    delta_color="normal" if saldo > 0 else "inverse")

        st.divider()

        tab1, tab2 = st.tabs(["  Solicitar Vacaciones  ", "  Historial  "])

        with tab1:
            if saldo <= 0:
                st.error("Este empleado no tiene saldo de vacaciones disponible.")
            else:
                with st.form("form_vacaciones"):
                    col1, col2 = st.columns(2)
                    with col1:
                        fecha_inicio = st.date_input("Fecha de inicio")
                    with col2:
                        dias_sol = st.number_input(
                            "Días hábiles solicitados",
                            min_value=1, max_value=int(saldo), step=1, value=1
                        )
                    fecha_fin = calcular_fecha_fin(fecha_inicio, dias_sol)
                    st.info(
                        f"Fecha de término calculada: **{fecha_fin.strftime('%d de %B de %Y')}**  "
                        f"·  {dias_sol} días hábiles  ·  Excluye sábados, domingos y festivos"
                    )
                    if st.form_submit_button("Registrar Vacaciones", use_container_width=True):
                        if dias_sol > saldo:
                            st.error(f"Saldo insuficiente. Disponible: {saldo} días.")
                        else:
                            cursor.execute(
                                "INSERT INTO vacaciones (empleado_id,fecha_inicio,fecha_fin,dias_consumidos) VALUES (?,?,?,?)",
                                (empleado_id, str(fecha_inicio), str(fecha_fin), dias_sol)
                            )
                            conn.commit()
                            st.success(f"Vacaciones registradas: {fecha_inicio} → {fecha_fin}  ·  {dias_sol} días")
                            st.rerun()

        with tab2:
            df_hist = pd.read_sql_query(
                "SELECT id, fecha_inicio, fecha_fin, dias_consumidos FROM vacaciones WHERE empleado_id=? ORDER BY fecha_inicio DESC",
                conn, params=(empleado_id,)
            )
            if df_hist.empty:
                st.info("Sin historial de vacaciones para este empleado.")
            else:
                df_hist.columns = ["ID", "Inicio", "Término", "Días"]
                st.dataframe(df_hist, use_container_width=True, hide_index=True)
                with st.expander("Eliminar registro de vacaciones"):
                    id_el = st.number_input("ID del registro (ver columna ID)", min_value=1, step=1)
                    if st.button("Eliminar registro", key="btn_del_vac"):
                        cursor.execute("DELETE FROM vacaciones WHERE id=? AND empleado_id=?", (id_el, empleado_id))
                        conn.commit()
                        st.success("Registro eliminado.")
                        st.rerun()

# =========================================================
# TURNOS
# =========================================================

elif menu == "Turnos":

    render_banner(
        "banner-turnos", "",
        "Gestión de Turnos 24H",
        "Asignación y control de turnos operacionales · Prevención de fatiga laboral",
        "Módulo Operacional"
    )

    TIPOS_TURNO = {
        "Turno Día  (07:00 – 19:00)":    "Turno Día",
        "Turno Noche  (19:00 – 07:00)":  "Turno Noche",
        "Guardia 24H  (00:00 – 24:00)":  "Guardia 24H",
        "Día Libre / Descanso":           "Día Libre",
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
                    tipo_label = st.selectbox("Tipo de turno", list(TIPOS_TURNO.keys()))
                with col2:
                    f_inicio = st.date_input("Fecha inicio", key="ti")
                    f_fin    = st.date_input("Fecha fin",    key="tf")

                tipo_val = TIPOS_TURNO[tipo_label]
                bg, fg   = COLORES[tipo_val]
                st.markdown(
                    f'<div style="display:inline-flex;align-items:center;gap:8px;background:{bg};'
                    f'color:{fg};padding:6px 16px;border-radius:7px;font-size:13px;font-weight:700;'
                    f'margin-top:6px;border:1px solid {bg};">Turno seleccionado: {tipo_val}</div>',
                    unsafe_allow_html=True
                )
                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

                if st.form_submit_button("Asignar Turno", use_container_width=True):
                    if f_fin < f_inicio:
                        st.error("La fecha de fin no puede ser anterior al inicio.")
                    else:
                        emp_id = int(df_emp[df_emp["nombre"]==emp_sel].iloc[0]["id"])
                        cursor.execute(
                            "INSERT INTO turnos (empleado_id,fecha_inicio,fecha_fin,tipo_turno) VALUES (?,?,?,?)",
                            (emp_id, str(f_inicio), str(f_fin), tipo_val)
                        )
                        conn.commit()
                        dias_d = (f_fin - f_inicio).days + 1
                        st.success(f"Turno **{tipo_val}** asignado a **{emp_sel}** · {f_inicio} → {f_fin} · {dias_d} día(s)")
                        st.rerun()

        with tab2:
            df_t = pd.read_sql_query(
                """SELECT t.id, e.nombre AS Empleado, t.tipo_turno AS Turno,
                          t.fecha_inicio AS Inicio, t.fecha_fin AS Fin
                   FROM turnos t JOIN empleados e ON t.empleado_id=e.id
                   ORDER BY t.fecha_inicio DESC""", conn
            )
            if df_t.empty:
                st.info("No hay turnos registrados.")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    fil_emp  = st.selectbox("Filtrar empleado",  ["Todos"]+df_emp["nombre"].tolist(), key="filt_e")
                with col2:
                    fil_tipo = st.selectbox("Filtrar turno",     ["Todos"]+list(TIPOS_TURNO.values()), key="filt_t")

                df_v = df_t.copy()
                if fil_emp  != "Todos": df_v = df_v[df_v["Empleado"] == fil_emp]
                if fil_tipo != "Todos": df_v = df_v[df_v["Turno"]    == fil_tipo]

                st.markdown(
                    f'<div style="font-size:13px;color:#64748b;margin-bottom:10px;"><b>{len(df_v)}</b> turno(s) encontrado(s)</div>',
                    unsafe_allow_html=True
                )
                st.dataframe(df_v, use_container_width=True, hide_index=True)

                with st.expander("Eliminar turno"):
                    id_t = st.number_input("ID del turno a eliminar (ver columna ID)", min_value=1, step=1)
                    if st.button("Eliminar turno", key="del_t"):
                        cursor.execute("DELETE FROM turnos WHERE id=?", (id_t,))
                        conn.commit()
                        st.success("Turno eliminado.")
                        st.rerun()

# =========================================================
# REPORTES
# =========================================================

elif menu == "Reportes":

    render_banner(
        "banner-reportes", "",
        "Reportes y Analytics",
        "Visualización ejecutiva · Vacaciones · Turnos · Personal · Exportación de datos",
        "Business Intelligence"
    )

    df_emp = obtener_empleados()

    if df_emp.empty:
        st.warning("Sin datos para reportar. Registre empleados primero.")
    else:
        cursor.execute("SELECT COUNT(*) FROM empleados")
        n_emp = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(SUM(dias_consumidos),0) FROM vacaciones")
        total_vac = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM turnos")
        n_turnos = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(DISTINCT empleado_id) FROM vacaciones")
        emp_con_vac = cursor.fetchone()[0]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Empleados",       n_emp)
        col2.metric("Días Vacac. Usados",    total_vac)
        col3.metric("Total Turnos",          n_turnos)
        col4.metric("Empl. con Vacaciones",  emp_con_vac)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                '<div style="font-size:15px;font-weight:700;color:#0f172a;margin-bottom:14px;">Vacaciones por Empleado</div>',
                unsafe_allow_html=True
            )
            datos_vac = []
            for _, row in df_emp.iterrows():
                t, c, s = obtener_resumen_vacaciones(row["id"])
                datos_vac.append({"Empleado": row["nombre"], "Consumidos": c, "Saldo": s})
            df_vc = pd.DataFrame(datos_vac)

            if PLOTLY:
                fig = go.Figure()
                fig.add_trace(go.Bar(name="Consumidos", x=df_vc["Empleado"], y=df_vc["Consumidos"],
                                     marker_color="#1d4ed8", marker_line_width=0))
                fig.add_trace(go.Bar(name="Saldo",      x=df_vc["Empleado"], y=df_vc["Saldo"],
                                     marker_color="#10b981", marker_line_width=0))
                fig.update_layout(
                    barmode="stack", height=320,
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=0,r=0,t=10,b=0),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    font=dict(family="Inter,system-ui", size=12),
                )
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.bar_chart(df_vc.set_index("Empleado"))

        with col2:
            st.markdown(
                '<div style="font-size:15px;font-weight:700;color:#0f172a;margin-bottom:14px;">Distribución de Turnos</div>',
                unsafe_allow_html=True
            )
            cursor.execute("SELECT tipo_turno, COUNT(*) FROM turnos GROUP BY tipo_turno")
            rows_t = cursor.fetchall()
            if rows_t:
                df_pie = pd.DataFrame(rows_t, columns=["Tipo","Total"])
                if PLOTLY:
                    fig2 = px.pie(df_pie, values="Total", names="Tipo", hole=0.46,
                                  color_discrete_sequence=["#1d4ed8","#5b21b6","#9d174d","#15803d"])
                    fig2.update_traces(
                        textposition="inside", textinfo="percent+label",
                        textfont_size=12,
                        marker=dict(line=dict(color="white", width=2))
                    )
                    fig2.update_layout(
                        height=320, paper_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=0,r=0,t=10,b=0), showlegend=False,
                        font=dict(family="Inter,system-ui", size=12),
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.dataframe(df_pie, use_container_width=True, hide_index=True)
            else:
                st.info("Sin turnos registrados para graficar.")

        st.divider()

        st.markdown(
            '<div style="font-size:15px;font-weight:700;color:#0f172a;margin-bottom:14px;">Resumen Ejecutivo Completo</div>',
            unsafe_allow_html=True
        )
        df_full = []
        for _, row in df_emp.iterrows():
            t, c, s = obtener_resumen_vacaciones(row["id"])
            cursor.execute("SELECT COUNT(*) FROM turnos WHERE empleado_id=?", (row["id"],))
            nt = cursor.fetchone()[0]
            df_full.append({
                "Nombre": row["nombre"], "Cargo": row["cargo"],
                "Vacac. Total": t, "Consumidos": c, "Saldo": s, "Turnos": nt
            })
        df_full_df = pd.DataFrame(df_full)
        st.dataframe(df_full_df, use_container_width=True, hide_index=True)

        csv = df_full_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Exportar Reporte CSV",
            csv,
            f"reporte_rrhh_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            "text/csv"
        )

# =========================================================
# SIDEBAR FOOTER
# =========================================================

st.sidebar.markdown("""
<div style="height:1px; background:rgba(255,255,255,0.07); margin:16px 12px;"></div>
<div style="
    padding:14px 16px;
    background:rgba(255,255,255,0.04);
    border-radius:12px;
    border:1px solid rgba(255,255,255,0.06);
    text-align:center;
    margin:0 4px;
">
    <div style="font-size:13px; font-weight:700; color:rgba(255,255,255,0.7);">RRHH Executive Pro</div>
    <div style="font-size:10px; color:rgba(255,255,255,0.3); margin-top:3px; letter-spacing:0.5px;">
        v8.1 · Corporativo · Confidencial
    </div>
</div>
""", unsafe_allow_html=True)
