# =========================================================
# SISTEMA RRHH EMPRESARIAL v8.0 EXECUTIVE PRO
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
# CSS EJECUTIVO PRO
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
    background:
        radial-gradient(ellipse at 10% 10%, rgba(37,99,235,0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 90%, rgba(99,102,241,0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(16,185,129,0.03) 0%, transparent 60%),
        linear-gradient(160deg, #eef2ff 0%, #f8fafc 40%, #f0fdf4 100%);
    background-image:
        radial-gradient(ellipse at 10% 10%, rgba(37,99,235,0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 90%, rgba(99,102,241,0.06) 0%, transparent 50%),
        url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%232563eb' fill-opacity='0.025' fill-rule='evenodd'%3E%3Ccircle cx='20' cy='20' r='1'/%3E%3C/g%3E%3C/svg%3E"),
        linear-gradient(160deg, #eef2ff 0%, #f8fafc 40%, #f0fdf4 100%);
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg,
            #020617 0%,
            #0f172a 30%,
            #162040 65%,
            #1e293b 100%
        ) !important;
    border-right: 1px solid rgba(255,255,255,0.05);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

section[data-testid="stSidebar"] .stRadio label {
    border-radius: 12px !important;
    padding: 11px 16px !important;
    margin: 3px 0 !important;
    transition: all 0.2s ease !important;
    border: 1px solid transparent !important;
    font-weight: 500 !important;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.09) !important;
    border-color: rgba(255,255,255,0.12) !important;
    transform: translateX(2px);
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 11px 22px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    letter-spacing: 0.2px !important;
    box-shadow: 0 4px 15px rgba(37,99,235,0.30) !important;
    transition: all 0.25s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(37,99,235,0.42) !important;
}

.stButton > button[kind="secondary"] {
    background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
    box-shadow: 0 4px 15px rgba(220,38,38,0.28) !important;
}

/* ── METRICS ── */
div[data-testid="metric-container"] {
    background: white;
    border-radius: 20px;
    padding: 26px 24px;
    border: 1px solid rgba(226,232,240,0.9);
    box-shadow: 0 4px 20px rgba(15,23,42,0.06);
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}

div[data-testid="metric-container"]::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(15,23,42,0.10);
}

/* ── FORMS ── */
[data-testid="stForm"] {
    background: white;
    border-radius: 22px;
    padding: 32px 36px;
    border: 1px solid rgba(226,232,240,0.9);
    box-shadow: 0 4px 20px rgba(15,23,42,0.05);
}

/* ── INPUTS ── */
.stTextInput input,
.stNumberInput input,
.stDateInput input {
    border-radius: 12px !important;
    border: 1.5px solid #e2e8f0 !important;
    background: #fafbff !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
    transition: all 0.2s ease !important;
}

.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
    background: white !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    background: white;
    border-radius: 18px;
    border: 1px solid rgba(226,232,240,0.9);
    box-shadow: 0 4px 20px rgba(15,23,42,0.04);
    overflow: hidden;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(241,245,249,0.8);
    border-radius: 14px;
    padding: 4px;
    gap: 2px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}

.stTabs [aria-selected="true"] {
    background: white !important;
    box-shadow: 0 2px 8px rgba(15,23,42,0.08) !important;
    color: #2563eb !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background: white;
    border-radius: 16px !important;
    border: 1px solid rgba(226,232,240,0.9) !important;
    box-shadow: 0 2px 10px rgba(15,23,42,0.04);
}

/* ── HR ── */
hr {
    border: none;
    border-top: 1.5px solid #f1f5f9;
    margin: 28px 0;
}

/* ── MODULE BANNERS ── */
.module-banner {
    border-radius: 28px;
    padding: 56px 64px;
    margin-bottom: 36px;
    position: relative;
    overflow: hidden;
    color: white;
}

.module-banner .geo1 {
    position: absolute;
    width: 560px; height: 560px;
    border-radius: 50%;
    background: radial-gradient(rgba(255,255,255,0.11), transparent 70%);
    top: -250px; right: -120px;
    pointer-events: none;
}

.module-banner .geo2 {
    position: absolute;
    width: 320px; height: 320px;
    border-radius: 50%;
    background: radial-gradient(rgba(255,255,255,0.07), transparent 70%);
    bottom: -160px; left: -90px;
    pointer-events: none;
}

.module-banner .geo3 {
    position: absolute;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(rgba(255,255,255,0.05), transparent 70%);
    top: 50%; right: 15%;
    pointer-events: none;
}

.module-banner .pattern {
    position: absolute;
    inset: 0;
    background-image:
        repeating-linear-gradient(
            45deg,
            rgba(255,255,255,0.02) 0px,
            rgba(255,255,255,0.02) 1px,
            transparent 1px,
            transparent 55px
        );
    pointer-events: none;
}

.module-banner .banner-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 100px;
    padding: 6px 18px;
    font-size: 12px;
    font-weight: 700;
    color: rgba(255,255,255,0.9);
    margin-bottom: 18px;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    position: relative;
    z-index: 2;
}

.module-banner h1 {
    color: white !important;
    font-size: 46px !important;
    font-weight: 900 !important;
    letter-spacing: -1.5px !important;
    margin: 0 0 10px 0 !important;
    position: relative;
    z-index: 2;
    text-shadow: 0 2px 20px rgba(0,0,0,0.2);
    line-height: 1.05 !important;
}

.module-banner p {
    color: rgba(255,255,255,0.68) !important;
    font-size: 17px !important;
    font-weight: 400 !important;
    margin: 0 !important;
    position: relative;
    z-index: 2;
    letter-spacing: 0.1px;
    line-height: 1.5 !important;
}

/* BANNER COLORS */
.banner-dashboard {
    background:
        url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.03' fill-rule='evenodd'%3E%3Cpath d='M0 0h40v40H0V0zm40 40h40v40H40V40z'/%3E%3C/g%3E%3C/svg%3E"),
        linear-gradient(135deg, #06091a 0%, #0c1a47 35%, #1a3480 65%, #2563eb 100%);
}

.banner-empleados {
    background:
        url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.03' fill-rule='evenodd'%3E%3Cpath d='M0 0h40v40H0V0zm40 40h40v40H40V40z'/%3E%3C/g%3E%3C/svg%3E"),
        linear-gradient(135deg, #060f2a 0%, #0c2060 35%, #14408a 65%, #1a6ecf 100%);
}

.banner-vacaciones {
    background:
        url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.03' fill-rule='evenodd'%3E%3Cpath d='M0 0h40v40H0V0zm40 40h40v40H40V40z'/%3E%3C/g%3E%3C/svg%3E"),
        linear-gradient(135deg, #011c12 0%, #043d28 35%, #065f46 65%, #059669 100%);
}

.banner-turnos {
    background:
        url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.03' fill-rule='evenodd'%3E%3Cpath d='M0 0h40v40H0V0zm40 40h40v40H40V40z'/%3E%3C/g%3E%3C/svg%3E"),
        linear-gradient(135deg, #14032a 0%, #2a0a5e 35%, #4c1d95 65%, #6d28d9 100%);
}

.banner-reportes {
    background:
        url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.03' fill-rule='evenodd'%3E%3Cpath d='M0 0h40v40H0V0zm40 40h40v40H40V40z'/%3E%3C/g%3E%3C/svg%3E"),
        linear-gradient(135deg, #180700 0%, #431407 35%, #7c2d12 65%, #c2410c 100%);
}

/* ── CARD ── */
.card {
    background: white;
    border-radius: 20px;
    padding: 28px;
    border: 1px solid rgba(226,232,240,0.9);
    box-shadow: 0 4px 20px rgba(15,23,42,0.05);
    margin-bottom: 20px;
    transition: all 0.25s ease;
}

.card:hover {
    box-shadow: 0 8px 32px rgba(15,23,42,0.09);
}

/* ── FEATURE LIST ── */
.feature-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 11px 0;
    border-bottom: 1px solid #f8fafc;
    color: #374151;
    font-size: 15px;
}

/* ── MODULE LIST ── */
.module-row {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 18px;
    background: #f8fafc;
    border-radius: 14px;
    margin-bottom: 10px;
    border: 1px solid rgba(226,232,240,0.6);
    transition: all 0.2s;
}

.module-row:hover {
    background: #eff6ff;
    border-color: #bfdbfe;
}

/* ── LOGIN ── */
.login-card {
    background: white;
    border-radius: 32px;
    padding: 56px 48px;
    box-shadow:
        0 30px 80px rgba(15,23,42,0.14),
        0 0 0 1px rgba(226,232,240,0.5);
    max-width: 440px;
    margin: 60px auto 0;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGIN
# =========================================================

if not st.session_state.login_correcto:

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        st.markdown("""
        <div class="login-card">
        <div style="text-align:center; margin-bottom:36px;">
            <div style="
                width:72px; height:72px;
                background:linear-gradient(135deg,#2563eb,#1d4ed8);
                border-radius:20px;
                display:flex; align-items:center; justify-content:center;
                font-size:32px; margin:0 auto 20px;
                box-shadow:0 8px 24px rgba(37,99,235,0.30);
            ">🏢</div>
            <h2 style="color:#0f172a; margin:0 0 6px; font-weight:800; font-size:26px; letter-spacing:-0.5px;">
                RRHH Executive Pro
            </h2>
            <p style="color:#64748b; margin:0; font-size:15px;">
                Plataforma Corporativa Empresarial
            </p>
        </div>
        </div>
        """, unsafe_allow_html=True)

        usuario = st.text_input("Usuario", placeholder="Ingrese su usuario")
        clave   = st.text_input("Contraseña", type="password", placeholder="••••••••")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Ingresar al Sistema", use_container_width=True):
            if usuario == USUARIO_ADMIN and clave == CLAVE_ADMIN:
                st.session_state.login_correcto = True
                st.rerun()
            else:
                st.error("⚠️ Credenciales incorrectas. Verifique usuario y contraseña.")

        st.markdown("""
        <div style="text-align:center; margin-top:24px; color:#94a3b8; font-size:13px;">
            Sistema protegido · Acceso solo personal autorizado
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# =========================================================
# BASE DE DATOS
# =========================================================

DB_NAME = "gestion_personal.db"

conn   = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()

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
# FUNCIONES AUXILIARES
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
        if (
            fecha_actual.weekday() < 5
            and fecha_actual not in chile_holidays
        ):
            dias += 1
        if dias < dias_solicitados:
            fecha_actual += timedelta(days=1)
    return fecha_actual

def obtener_resumen_vacaciones(empleado_id):
    cursor.execute(
        "SELECT dias_vacaciones FROM empleados WHERE id = ?",
        (empleado_id,)
    )
    resultado = cursor.fetchone()
    if resultado is None:
        return 0, 0, 0
    total = resultado[0]
    cursor.execute(
        "SELECT COALESCE(SUM(dias_consumidos), 0) FROM vacaciones WHERE empleado_id = ?",
        (empleado_id,)
    )
    consumidos = cursor.fetchone()[0]
    return total, consumidos, total - consumidos

def render_banner(css_class, icon, title, subtitle, badge=""):
    badge_html = (
        f'<div class="banner-badge">{badge}</div>'
        if badge else ""
    )
    st.markdown(f"""
    <div class="module-banner {css_class}">
        <div class="geo1"></div>
        <div class="geo2"></div>
        <div class="geo3"></div>
        <div class="pattern"></div>
        {badge_html}
        <h1>{icon} {title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("""
<div style="padding:22px 10px 14px;">
    <div style="
        display:flex; align-items:center; gap:12px; margin-bottom:6px;
    ">
        <div style="
            width:44px; height:44px;
            background:linear-gradient(135deg,#2563eb,#1d4ed8);
            border-radius:13px;
            display:flex; align-items:center; justify-content:center;
            font-size:20px;
            box-shadow:0 4px 14px rgba(37,99,235,0.4);
        ">🏢</div>
        <div>
            <div style="font-size:17px; font-weight:800; letter-spacing:-0.3px;">RRHH Pro</div>
            <div style="font-size:11px; color:rgba(255,255,255,0.45); letter-spacing:0.8px; text-transform:uppercase; margin-top:1px;">Executive Suite</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.divider()

menu = st.sidebar.radio(
    "Navegación",
    [
        "🏠 Dashboard",
        "👤 Empleados",
        "🏖️ Vacaciones",
        "🕒 Turnos",
        "📊 Reportes"
    ],
    label_visibility="collapsed"
)

# =========================================================
# DASHBOARD
# =========================================================

if menu == "🏠 Dashboard":

    render_banner(
        "banner-dashboard", "🏢",
        "Sistema de Gestión RRHH",
        "Plataforma Ejecutiva de Recursos Humanos · Turnos Operacionales · Prevención Laboral",
        "Executive Suite v8.0"
    )

    # ── Reloj en tiempo real (componente iframe) ──
    components.html("""
    <div style="
        background:white;
        border-radius:20px;
        padding:22px 32px;
        border:1px solid #e2e8f0;
        box-shadow:0 4px 20px rgba(15,23,42,0.06);
        margin-bottom:4px;
        display:flex;
        align-items:center;
        gap:28px;
    ">
        <div style="border-left:4px solid #2563eb; padding-left:20px;">
            <div id="hora" style="
                font-size:44px;
                font-weight:900;
                color:#2563eb;
                font-family:'Inter',system-ui;
                letter-spacing:-2px;
                line-height:1;
            ">00:00:00</div>
            <div id="fecha" style="
                font-size:15px;
                color:#64748b;
                margin-top:7px;
                font-family:'Inter',system-ui;
                font-weight:500;
            ">—</div>
        </div>
        <div style="height:70px; width:1px; background:#e2e8f0; flex-shrink:0;"></div>
        <div style="font-family:'Inter',system-ui;">
            <div style="font-weight:800; color:#0f172a; font-size:17px;">Sistema Activo</div>
            <div style="font-size:13px; color:#64748b; margin-top:4px;">RRHH Executive Pro · Plataforma Corporativa</div>
            <div style="margin-top:10px; display:flex; gap:8px;">
                <span style="
                    background:#dcfce7; color:#15803d;
                    padding:3px 12px; border-radius:100px;
                    font-size:12px; font-weight:700;
                ">● EN LÍNEA</span>
            </div>
        </div>
    </div>
    <script>
    const DIAS  = ["Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado"];
    const MESES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                   "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"];
    function tick() {
        const n = new Date();
        document.getElementById("hora").textContent =
            String(n.getHours()).padStart(2,"0") + ":" +
            String(n.getMinutes()).padStart(2,"0") + ":" +
            String(n.getSeconds()).padStart(2,"0");
        document.getElementById("fecha").textContent =
            DIAS[n.getDay()] + " " + n.getDate() +
            " de " + MESES[n.getMonth()] + " de " + n.getFullYear();
    }
    tick();
    setInterval(tick, 1000);
    </script>
    """, height=130)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Métricas reales ──
    df_emp = obtener_empleados()
    n_emp  = len(df_emp)

    cursor.execute("SELECT COALESCE(SUM(dias_consumidos),0) FROM vacaciones")
    total_vac = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM turnos")
    n_turnos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT empleado_id) FROM vacaciones")
    emp_vac = cursor.fetchone()[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👤 Empleados", n_emp, "Activos")
    col2.metric("📅 Días Vacaciones", total_vac, "Consumidos")
    col3.metric("🕒 Turnos", n_turnos, "Registrados")
    col4.metric("✈️ Con Vacaciones", emp_vac, "Empleados")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Módulos del Sistema")
        modulos = [
            ("🏠", "Dashboard",   "Centro de control y monitoreo ejecutivo"),
            ("👤", "Empleados",   "Registro y administración del personal"),
            ("🏖️", "Vacaciones",  "Control legal de descanso con festivos"),
            ("🕒", "Turnos",      "Gestión operacional 24H de turnos"),
            ("📊", "Reportes",    "Analytics, gráficos y exportación CSV"),
        ]
        for icon, nombre, desc in modulos:
            st.markdown(f"""
            <div class="module-row">
                <span style="font-size:22px; width:32px; text-align:center;">{icon}</span>
                <div>
                    <div style="font-weight:700; color:#0f172a; font-size:15px;">{nombre}</div>
                    <div style="font-size:13px; color:#64748b; margin-top:2px;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("### Características del Sistema")
        features = [
            ("✅", "Gestión integral de Recursos Humanos"),
            ("✅", "Cálculo automático días hábiles y festivos"),
            ("✅", "Control legal de descanso (Código del Trabajo)"),
            ("✅", "Turnos operacionales configurables 24H"),
            ("✅", "Base de datos SQLite robusta y local"),
            ("✅", "Analytics en tiempo real con gráficos"),
            ("✅", "Exportación de reportes en CSV"),
            ("✅", "Acceso seguro con autenticación"),
            ("✅", "Prevención de fatiga laboral"),
        ]
        feat_html = "".join([
            f'<div class="feature-row">'
            f'<span style="color:#10b981; font-size:18px;">{icon}</span>'
            f'<span>{texto}</span></div>'
            for icon, texto in features
        ])
        st.markdown(f'<div class="card" style="padding:22px 26px;">{feat_html}</div>', unsafe_allow_html=True)

# =========================================================
# EMPLEADOS
# =========================================================

elif menu == "👤 Empleados":

    render_banner(
        "banner-empleados", "👤",
        "Gestión de Empleados",
        "Registro, consulta y administración integral del personal de la empresa",
        "RRHH · Directorio de Personal"
    )

    tab1, tab2 = st.tabs(["➕  Nuevo Empleado", "📋  Directorio y Administración"])

    with tab1:
        with st.form("form_empleado"):
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input(
                    "Nombre completo *",
                    placeholder="Ej: Juan Pérez González"
                )
            with col2:
                cargo = st.text_input(
                    "Cargo / Función",
                    placeholder="Ej: Jefe de Operaciones"
                )

            dias = st.number_input(
                "Días de vacaciones legales asignados",
                min_value=0, max_value=60, step=1, value=15
            )

            st.markdown("<br>", unsafe_allow_html=True)

            guardar = st.form_submit_button(
                "💾 Registrar Empleado",
                use_container_width=True
            )

            if guardar:
                if not nombre.strip():
                    st.error("⚠️ El nombre del empleado es obligatorio.")
                else:
                    cursor.execute(
                        "INSERT INTO empleados (nombre, cargo, dias_vacaciones) VALUES (?, ?, ?)",
                        (nombre.strip(), cargo.strip(), dias)
                    )
                    conn.commit()
                    st.success(f"✅ Empleado **{nombre.strip()}** registrado correctamente.")
                    st.rerun()

    with tab2:
        df = obtener_empleados()

        if df.empty:
            st.info("📋 No hay empleados registrados aún. Use la pestaña **Nuevo Empleado** para agregar.")
        else:
            resumen = []
            for _, row in df.iterrows():
                total, consumidos, saldo = obtener_resumen_vacaciones(row["id"])
                resumen.append({
                    "ID":             row["id"],
                    "Nombre":         row["nombre"],
                    "Cargo":          row["cargo"],
                    "Vacac. Total":   total,
                    "Consumidos":     consumidos,
                    "Saldo":          saldo,
                })
            df_resumen = pd.DataFrame(resumen)

            st.markdown(
                f"<div style='color:#64748b; font-size:14px; margin-bottom:12px;'>"
                f"<strong>{len(df_resumen)}</strong> empleado(s) registrado(s)</div>",
                unsafe_allow_html=True
            )
            st.dataframe(df_resumen, use_container_width=True, hide_index=True)

            st.divider()
            st.markdown("### 🗑️ Eliminar Empleado")
            st.caption("Al eliminar un empleado se eliminarán también sus registros de vacaciones y turnos.")

            col1, col2 = st.columns([3, 1])
            with col1:
                opciones = {
                    f"{r['Nombre']}  —  {r['Cargo']}": r["ID"]
                    for _, r in df_resumen.iterrows()
                }
                sel = st.selectbox(
                    "Seleccionar empleado",
                    list(opciones.keys()),
                    label_visibility="collapsed"
                )
            with col2:
                if st.button("🗑️ Eliminar", type="secondary", use_container_width=True):
                    eid = opciones[sel]
                    cursor.execute("DELETE FROM empleados  WHERE id = ?",           (eid,))
                    cursor.execute("DELETE FROM vacaciones WHERE empleado_id = ?",  (eid,))
                    cursor.execute("DELETE FROM turnos     WHERE empleado_id = ?",  (eid,))
                    conn.commit()
                    st.success("✅ Empleado y todos sus registros eliminados.")
                    st.rerun()

# =========================================================
# VACACIONES
# =========================================================

elif menu == "🏖️ Vacaciones":

    render_banner(
        "banner-vacaciones", "🏖️",
        "Control de Vacaciones",
        "Administración legal de descanso · Cálculo automático con días hábiles y festivos nacionales",
        "Conforme Código del Trabajo"
    )

    df_emp = obtener_empleados()

    if df_emp.empty:
        st.warning("⚠️ No hay empleados registrados. Agregue empleados en el módulo Empleados.")
    else:
        empleado_nombre = st.selectbox(
            "Seleccionar trabajador",
            df_emp["nombre"],
            key="vac_emp_select"
        )
        empleado    = df_emp[df_emp["nombre"] == empleado_nombre].iloc[0]
        empleado_id = int(empleado["id"])

        total, consumidos, saldo = obtener_resumen_vacaciones(empleado_id)

        col1, col2, col3 = st.columns(3)
        col1.metric("📅 Días Totales",    total)
        col2.metric("✈️ Consumidos",      consumidos)
        col3.metric(
            "💚 Saldo Disponible", saldo,
            "Disponible" if saldo > 0 else "Sin saldo",
            delta_color="normal" if saldo > 0 else "inverse"
        )

        st.divider()

        tab1, tab2 = st.tabs(["➕  Solicitar Vacaciones", "📋  Historial"])

        with tab1:
            if saldo <= 0:
                st.error("❌ Este empleado no tiene saldo de vacaciones disponible.")
            else:
                with st.form("form_vacaciones"):
                    col1, col2 = st.columns(2)
                    with col1:
                        fecha_inicio = st.date_input("Fecha de inicio")
                    with col2:
                        dias_sol = st.number_input(
                            "Días hábiles solicitados",
                            min_value=1,
                            max_value=int(saldo),
                            step=1,
                            value=1
                        )

                    fecha_fin = calcular_fecha_fin(fecha_inicio, dias_sol)
                    st.info(
                        f"📅 Fecha de término calculada: **{fecha_fin.strftime('%d de %B de %Y')}**  "
                        f"·  {dias_sol} días hábiles  ·  Excluye sábados, domingos y festivos de Chile"
                    )

                    guardar = st.form_submit_button(
                        "💾 Registrar Vacaciones",
                        use_container_width=True
                    )

                    if guardar:
                        if dias_sol > saldo:
                            st.error(f"❌ Saldo insuficiente. Disponible: {saldo} días.")
                        else:
                            cursor.execute(
                                """INSERT INTO vacaciones
                                   (empleado_id, fecha_inicio, fecha_fin, dias_consumidos)
                                   VALUES (?, ?, ?, ?)""",
                                (empleado_id, str(fecha_inicio), str(fecha_fin), dias_sol)
                            )
                            conn.commit()
                            st.success(
                                f"✅ Vacaciones registradas correctamente.\n\n"
                                f"**{empleado_nombre}** · {fecha_inicio} → {fecha_fin} · {dias_sol} días"
                            )
                            st.rerun()

        with tab2:
            df_hist = pd.read_sql_query(
                """SELECT id, fecha_inicio, fecha_fin, dias_consumidos
                   FROM vacaciones
                   WHERE empleado_id = ?
                   ORDER BY fecha_inicio DESC""",
                conn, params=(empleado_id,)
            )

            if df_hist.empty:
                st.info("📋 Sin historial de vacaciones para este empleado.")
            else:
                df_hist.columns = ["ID", "Inicio", "Término", "Días"]
                st.dataframe(df_hist, use_container_width=True, hide_index=True)

                with st.expander("🗑️ Eliminar registro de vacaciones"):
                    id_el = st.number_input(
                        "ID del registro a eliminar (ver columna ID en la tabla)",
                        min_value=1, step=1
                    )
                    if st.button("Eliminar registro", key="btn_del_vac"):
                        cursor.execute(
                            "DELETE FROM vacaciones WHERE id = ? AND empleado_id = ?",
                            (id_el, empleado_id)
                        )
                        conn.commit()
                        st.success("✅ Registro eliminado.")
                        st.rerun()

# =========================================================
# TURNOS
# =========================================================

elif menu == "🕒 Turnos":

    render_banner(
        "banner-turnos", "🕒",
        "Gestión de Turnos 24H",
        "Asignación y control de turnos operacionales · Prevención de fatiga laboral conforme normativa",
        "Módulo Operacional"
    )

    TIPOS_TURNO = {
        "☀️  Turno Día  (07:00 – 19:00)":     "Turno Día",
        "🌙  Turno Noche  (19:00 – 07:00)":   "Turno Noche",
        "🛡️  Guardia 24H  (00:00 – 24:00)":   "Guardia 24H",
        "🌿  Día Libre / Descanso":            "Día Libre",
    }

    COLORES_TURNO = {
        "Turno Día":   "#dbeafe|#1d4ed8",
        "Turno Noche": "#ede9fe|#5b21b6",
        "Guardia 24H": "#fce7f3|#9d174d",
        "Día Libre":   "#dcfce7|#15803d",
    }

    df_emp = obtener_empleados()

    if df_emp.empty:
        st.warning("⚠️ No hay empleados registrados.")
    else:
        tab1, tab2 = st.tabs(["➕  Asignar Turno", "📋  Turnos Registrados"])

        with tab1:
            with st.form("form_turno"):
                col1, col2 = st.columns(2)
                with col1:
                    emp_sel    = st.selectbox("Empleado", df_emp["nombre"])
                    tipo_label = st.selectbox("Tipo de turno", list(TIPOS_TURNO.keys()))
                with col2:
                    f_inicio = st.date_input("Fecha inicio", key="t_inicio")
                    f_fin    = st.date_input("Fecha fin",    key="t_fin")

                tipo_val = TIPOS_TURNO[tipo_label]
                bg, fg = COLORES_TURNO[tipo_val].split("|")
                st.markdown(
                    f'<div style="display:inline-flex; align-items:center; gap:8px; '
                    f'background:{bg}; color:{fg}; padding:7px 18px; border-radius:100px; '
                    f'font-size:14px; font-weight:700; margin-top:6px;">'
                    f'Turno seleccionado: {tipo_val}</div>',
                    unsafe_allow_html=True
                )
                st.markdown("<br>", unsafe_allow_html=True)

                guardar = st.form_submit_button("💾 Asignar Turno", use_container_width=True)

                if guardar:
                    if f_fin < f_inicio:
                        st.error("❌ La fecha de fin no puede ser anterior a la fecha de inicio.")
                    else:
                        emp_row = df_emp[df_emp["nombre"] == emp_sel].iloc[0]
                        emp_id  = int(emp_row["id"])
                        cursor.execute(
                            """INSERT INTO turnos
                               (empleado_id, fecha_inicio, fecha_fin, tipo_turno)
                               VALUES (?, ?, ?, ?)""",
                            (emp_id, str(f_inicio), str(f_fin), tipo_val)
                        )
                        conn.commit()
                        duracion = (f_fin - f_inicio).days + 1
                        st.success(
                            f"✅ Turno **{tipo_val}** asignado a **{emp_sel}**.\n\n"
                            f"Período: {f_inicio} → {f_fin}  ·  {duracion} día(s)"
                        )
                        st.rerun()

        with tab2:
            df_turnos = pd.read_sql_query(
                """SELECT t.id, e.nombre AS Empleado, t.tipo_turno AS Turno,
                          t.fecha_inicio AS Inicio, t.fecha_fin AS Fin
                   FROM turnos t
                   JOIN empleados e ON t.empleado_id = e.id
                   ORDER BY t.fecha_inicio DESC""",
                conn
            )

            if df_turnos.empty:
                st.info("📋 No hay turnos registrados. Use la pestaña **Asignar Turno**.")
            else:
                col1, col2 = st.columns([2, 1])
                with col1:
                    opciones_fil = ["Todos"] + df_emp["nombre"].tolist()
                    filtro = st.selectbox("Filtrar por empleado", opciones_fil, key="turno_filtro")
                with col2:
                    tipos_fil = ["Todos"] + list(TIPOS_TURNO.values())
                    filtro_tipo = st.selectbox("Filtrar por turno", tipos_fil, key="turno_tipo_filtro")

                df_vis = df_turnos.copy()
                if filtro != "Todos":
                    df_vis = df_vis[df_vis["Empleado"] == filtro]
                if filtro_tipo != "Todos":
                    df_vis = df_vis[df_vis["Turno"] == filtro_tipo]

                st.markdown(
                    f"<div style='color:#64748b; font-size:14px; margin-bottom:10px;'>"
                    f"<strong>{len(df_vis)}</strong> turno(s) encontrado(s)</div>",
                    unsafe_allow_html=True
                )
                st.dataframe(df_vis, use_container_width=True, hide_index=True)

                with st.expander("🗑️ Eliminar turno"):
                    id_t = st.number_input(
                        "ID del turno a eliminar (ver columna ID en la tabla)",
                        min_value=1, step=1, key="del_turno_id"
                    )
                    if st.button("Eliminar turno", key="btn_del_turno"):
                        cursor.execute("DELETE FROM turnos WHERE id = ?", (id_t,))
                        conn.commit()
                        st.success("✅ Turno eliminado.")
                        st.rerun()

# =========================================================
# REPORTES
# =========================================================

elif menu == "📊 Reportes":

    render_banner(
        "banner-reportes", "📊",
        "Reportes y Analytics",
        "Visualización ejecutiva · Vacaciones · Turnos · Personal · Exportación de datos",
        "Business Intelligence"
    )

    df_emp = obtener_empleados()

    if df_emp.empty:
        st.warning("⚠️ Sin datos para reportar. Registre empleados primero.")
    else:
        # ── Métricas de resumen ──
        cursor.execute("SELECT COUNT(*) FROM empleados")
        n_emp = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(dias_consumidos),0) FROM vacaciones")
        total_vac = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM turnos")
        n_turnos = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT empleado_id) FROM vacaciones")
        emp_con_vac = cursor.fetchone()[0]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👤 Total Empleados",      n_emp)
        col2.metric("📅 Días Vacac. Usados",   total_vac)
        col3.metric("🕒 Total Turnos",         n_turnos)
        col4.metric("✈️ Empl. c/Vacaciones",  emp_con_vac)

        st.divider()

        # ── Gráficos ──
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📅 Vacaciones por Empleado")

            datos_vac = []
            for _, row in df_emp.iterrows():
                total, consumidos, saldo = obtener_resumen_vacaciones(row["id"])
                datos_vac.append({
                    "Empleado":  row["nombre"],
                    "Consumidos": consumidos,
                    "Saldo":      saldo,
                })
            df_vac_chart = pd.DataFrame(datos_vac)

            if PLOTLY:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    name="Consumidos",
                    x=df_vac_chart["Empleado"],
                    y=df_vac_chart["Consumidos"],
                    marker_color="#2563eb",
                    marker_line_width=0,
                ))
                fig.add_trace(go.Bar(
                    name="Saldo",
                    x=df_vac_chart["Empleado"],
                    y=df_vac_chart["Saldo"],
                    marker_color="#10b981",
                    marker_line_width=0,
                ))
                fig.update_layout(
                    barmode="stack",
                    height=360,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=0, r=0, t=10, b=0),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom", y=1.02,
                        xanchor="right",  x=1
                    ),
                    font=dict(family="Inter, system-ui", size=13),
                )
                fig.update_xaxes(showgrid=False, tickfont=dict(size=12))
                fig.update_yaxes(showgrid=True, gridcolor="#f1f5f9", tickfont=dict(size=12))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.bar_chart(df_vac_chart.set_index("Empleado"))

        with col2:
            st.markdown("### 🕒 Distribución de Turnos")

            cursor.execute(
                "SELECT tipo_turno, COUNT(*) AS total FROM turnos GROUP BY tipo_turno"
            )
            rows_t = cursor.fetchall()

            if rows_t:
                df_pie = pd.DataFrame(rows_t, columns=["Tipo", "Total"])
                if PLOTLY:
                    fig2 = px.pie(
                        df_pie, values="Total", names="Tipo",
                        hole=0.48,
                        color_discrete_sequence=["#2563eb","#7c3aed","#dc2626","#10b981"],
                    )
                    fig2.update_traces(
                        textposition="inside",
                        textinfo="percent+label",
                        textfont_size=13,
                        marker=dict(line=dict(color="white", width=3))
                    )
                    fig2.update_layout(
                        height=360,
                        paper_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=0, r=0, t=10, b=0),
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom", y=-0.15,
                            xanchor="center", x=0.5
                        ),
                        font=dict(family="Inter, system-ui", size=13),
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.dataframe(df_pie, use_container_width=True, hide_index=True)
            else:
                st.info("📋 Sin turnos registrados para graficar.")

        st.divider()

        # ── Tabla completa ──
        st.markdown("### 📋 Resumen Ejecutivo Completo")

        df_full = []
        for _, row in df_emp.iterrows():
            total, consumidos, saldo = obtener_resumen_vacaciones(row["id"])
            cursor.execute(
                "SELECT COUNT(*) FROM turnos WHERE empleado_id = ?",
                (row["id"],)
            )
            n_t = cursor.fetchone()[0]
            df_full.append({
                "Nombre":             row["nombre"],
                "Cargo":              row["cargo"],
                "Vacac. Total":       total,
                "Consumidos":         consumidos,
                "Saldo Disponible":   saldo,
                "Turnos Asignados":   n_t,
            })

        df_full_df = pd.DataFrame(df_full)
        st.dataframe(df_full_df, use_container_width=True, hide_index=True)

        # ── Exportar ──
        csv_data = df_full_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Exportar Reporte CSV",
            data=csv_data,
            file_name=f"reporte_rrhh_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )

# =========================================================
# SIDEBAR FOOTER
# =========================================================

st.sidebar.markdown("---")

st.sidebar.markdown("""
<div style="
    padding:18px;
    background:rgba(255,255,255,0.04);
    border-radius:16px;
    border:1px solid rgba(255,255,255,0.07);
    text-align:center;
">
    <div style="font-size:14px; font-weight:700; margin-bottom:4px;">RRHH Executive Pro</div>
    <div style="font-size:11px; color:rgba(255,255,255,0.38); letter-spacing:0.5px;">
        v8.0 · Sistema Corporativo · Confidencial
    </div>
</div>
""", unsafe_allow_html=True)
