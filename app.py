import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import os
import datetime

# =====================================================================
# CONFIGURACIÓN DE LA INTERFAZ PREMIUM (BRANDING RE-DESIGN)
# =====================================================================
st.set_page_config(
    page_title="Mall Credit Evaluator Pro", 
    layout="wide", 
    page_icon="💳",
    initial_sidebar_state="expanded"
)

# ESTILOS CSS AVANZADOS (DISEÑO GRÁFICO CORPORATIVO Y GRADIENTES)
st.markdown("""
<style>
    /* Estética General Premium - Fondo Gradiente Suave y Elegante */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1f2937 100%);
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Personalización Avanzada de la Barra Lateral */
    div[data-testid="stSidebarUserContent"] {
        background-color: #0b0f19 !important;
        padding-top: 2rem;
    }

    /* Contenedor Hero de Ancho Completo (Corrige el espacio vacío a la derecha) */
    .hero-container {
        background: linear-gradient(90deg, rgba(17,24,39,0.8) 0%, rgba(31,41,55,0.4) 100%), 
                    url('https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        border-radius: 16px;
        padding: 40px;
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Tarjeta de Crédito Virtual en Sidebar */
    .credit-card-widget {
        background: linear-gradient(135deg, #2e66ff 0%, #8e2de2 100%);
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 10px 20px rgba(46, 102, 255, 0.2);
        color: white;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }
    .credit-card-widget::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 80%);
    }

    /* Mosaicos de Métricas de Alta Gama (Glassmorphism + Neo-Glow) */
    .stMetric {
        background: rgba(17, 24, 39, 0.5) !important;
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2) !important;
    }
    .stMetric:hover {
        transform: translateY(-4px);
        border-color: rgba(46, 102, 255, 0.4) !important;
        box-shadow: 0 12px 24px rgba(46, 102, 255, 0.15) !important;
    }
    
    /* Insignias de la cabecera */
    .badge-premium {
        background: linear-gradient(90deg, #fca311, #ffcd3c);
        color: #0b0f19;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .badge-sync {
        background: rgba(0, 184, 148, 0.15);
        color: #00b894;
        border: 1px solid #00b894;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }

    /* Bloques de Dictamen con Degradados Dinámicos */
    .decision-card-approved {
        background: linear-gradient(135deg, rgba(39, 174, 96, 0.12) 0%, rgba(39, 174, 96, 0.02) 100%);
        border-left: 6px solid #27ae60;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        margin-bottom: 25px;
    }
    .decision-card-rejected {
        background: linear-gradient(135deg, rgba(192, 41, 43, 0.12) 0%, rgba(192, 41, 43, 0.02) 100%);
        border-left: 6px solid #c0392b;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        margin-bottom: 25px;
    }

    /* Sub-paneles Oscuros Estilizados */
    .glass-panel {
        background: rgba(17, 24, 39, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.04);
        padding: 20px;
        border-radius: 12px;
        height: 100%;
        box-shadow: inset 0 1px 1px rgba(255,255,255,0.05);
    }

    /* Botón de descarga de marca premium */
    .stDownloadButton button {
        background: linear-gradient(90deg, #fca311 0%, #ff8c00 100%) !important;
        color: #0b0f19 !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        border: none !important;
        border-radius: 8px !important;
        padding: 14px 28px !important;
        box-shadow: 0 4px 20px rgba(252, 163, 17, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton button:hover {
        transform: scale(1.01);
        box-shadow: 0 6px 25px rgba(252, 163, 17, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# BANNER HERO DE ANCHO COMPLETO CON MARCA INTEGRADA
# =====================================================================
st.markdown("""
<div class="hero-container">
    <div style="max-width: 600px; background: rgba(11, 15, 25, 0.85); padding: 30px; border-radius: 12px; backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.05);">
        <span class='badge-premium' style='font-size: 0.75rem; padding: 4px 10px;'>ALGORITHMIC CORE v3.14</span>
        <h2 style='margin: 10px 0 5px 0; font-weight: 800; color: #ffffff;'>Ecosistema de Scoring de Inteligencia Financiera</h2>
        <p style='margin: 0; color: #94a3b8; font-size: 0.95rem; line-height: 1.4;'>Modelado analítico avanzado para la segmentación automatizada de perfiles crediticios en tiempo real.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Barra de herramientas superior e insignias
col_header1, col_header2 = st.columns([1, 2])
with col_header1:
    today_str = datetime.date.today().strftime("%d de %B, %Y")
    st.markdown(f"<p style='color: #94a3b8; font-weight: 500; margin-top: 5px;'>📅 Auditoría del Sistema: {today_str}</p>", unsafe_allow_html=True)

with col_header2:
    st.markdown("""
    <div style='text-align: right; margin-bottom: 15px;'>
        <span class='badge-premium'>🔒 ADVISOR PREMIUM INTERFACE</span>
        <span class='badge-sync'>🟢 ALGORITMO SYNC: LIVE</span>
    </div>
    """, unsafe_allow_html=True)

st.title("💳 Sistema Inteligente de Evaluación de Créditos")

# =====================================================================
# 1. MOTOR DE DATOS (PROCESAMIENTO BACKEND)
# =====================================================================
@st.cache_data
def cargar_y_procesar_datos():
    ruta = "Mall_Customers_wa.tab"
    if not os.path.exists(ruta):
        st.error(f"⚠️ ¡Archivo de datos no detectado! Asegúrate de tener 'Mall_Customers_wa.tab' en la carpeta: {os.getcwd()}")
        st.stop()
        
    df_local = pd.read_csv(ruta, sep='\t', skiprows=[1, 2])
    min_inc, max_inc = 15.0, 137.0
    min_exp, max_exp = 1.0, 99.0
    
    df_local['Ingresos_Reales'] = df_local['Annual Income (k$)'] * (max_inc - min_inc) + min_inc
    df_local['Gasto_Real'] = df_local['Spending Score (1-100)'] * (max_exp - min_exp) + min_exp
    
    X = df_local[['Ingresos_Reales', 'Gasto_Real']]
    kmeans_model = KMeans(n_clusters=5, random_state=42, n_init=10)
    df_local['Cluster_Predicho'] = kmeans_model.fit_predict(X)
    
    centros = df_local.groupby('Cluster_Predicho')[['Ingresos_Reales', 'Gasto_Real']].mean()
    mapeo_inteligente = {}
    for idx, row in centros.iterrows():
        inc = row['Ingresos_Reales']
        exp = row['Gasto_Real']
        if inc < 50 and exp < 40: mapeo_inteligente[idx] = 'C1'
        elif inc > 65 and exp > 60: mapeo_inteligente[idx] = 'C3'
        elif inc > 65 and exp < 40: mapeo_inteligente[idx] = 'C4'
        elif inc < 50 and exp > 60: mapeo_inteligente[idx] = 'C5'
        else: mapeo_inteligente[idx] = 'C2'

    if len(set(mapeo_inteligente.values())) < 5:
        mapeo_inteligente = {0: 'C5', 1: 'C1', 2: 'C3', 3: 'C2', 4: 'C4'}
        
    df_local['Cluster_Final'] = df_local['Cluster_Predicho'].map(mapeo_inteligente)
    return df_local, kmeans_model, min_inc, max_inc, min_exp, max_exp, mapeo_inteligente

df, kmeans, min_inc, max_inc, min_exp, max_exp, mapa_clústeres = cargar_y_procesar_datos()

# =====================================================================
# 2. SIDEBAR SENSORIAL (CON TARJETA DE CRÉDITO DESIGN)
# =====================================================================
with st.sidebar:
    st.markdown("""
    <div class='credit-card-widget'>
        <p style='font-family: monospace; letter-spacing: 2px; font-size: 0.8rem; margin:0;'>CREDIT SCORING ENGINE</p>
        <h3 style='margin: 10px 0; color: white; font-weight:800;'>MALL PRO SYSTEM</h3>
        <p style='font-family: monospace; font-size: 1.1rem; margin-top:15px;'>**** **** **** 2026</p>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 10px;'>
            <span style='font-size:0.7rem; color: #e0e6ed;'>VALID ADVISOR USE ONLY</span>
            <span style='font-weight: bold; font-style: italic;'>VISA</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📋 Captura de Datos")
    st.write("Modifique los indicadores clave del cliente en ventanilla:")
    
    ingresos_input = st.number_input("Ingresos Anuales del Perfil (k$):", min_value=1, max_value=250, value=60)
    gasto_input = st.number_input("Score de Intención de Gasto (1-100):", min_value=1, max_value=100, value=50)
    
    st.markdown("---")
    if ingresos_input < min_inc or ingresos_input > max_inc:
        st.sidebar.warning(f"⚠️ Alerta: El ingreso ingresado difiere de los límites base optimizados ({int(min_inc)}-{int(max_inc)} k$).")

    st.markdown("### 🏷️ Matriz Comercial de Riesgo")
    st.markdown("<div style='background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; font-size:0.9rem; border: 1px solid rgba(255,255,255,0.05);'>"
                "⚪ <b style='color:#95a5a6;'>C1 Gris:</b> Ahorro Pasivo<br>"
                "🔵 <b style='color:#3498db;'>C2 Azul:</b> Consumo Convencional<br>"
                "🟡 <b style='color:#fca311;'>C3 Oro:</b> Cuenta VIP Elite<br>"
                "🟢 <b style='color:#2ecc71;'>C4 Verde:</b> Valor Patrimonial<br>"
                "🟠 <b style='color:#e67e22;'>C5 Naranja:</b> Consumo Volátil</div>", unsafe_allow_html=True)

# =====================================================================
# 3. LÓGICA DE PROCESAMIENTO
# =====================================================================
nuevo_cliente = pd.DataFrame([{'Ingresos_Reales': float(ingresos_input), 'Gasto_Real': float(gasto_input)}])
cluster_id_raw = kmeans.predict(nuevo_cliente)[0]
nombre_cluster = mapa_clústeres[cluster_id_raw]

politica_credito = {
    'C1': { 'Nombre': 'Ahorradores Cuidadosos', 'Aprobado': False, 'Factor_Linea': 0.00, 'Tasa': 0, 'TEA': '0%',
            'Detalle': 'Capacidad patrimonial e interacción de flujo por debajo del umbral mínimo exigido institucionalmente.', 'Accion': 'Rechazo Automático. Migrar flujo comercial hacia apertura de Cuentas de Ahorro Programado sin comisión.' },
    'C2': { 'Nombre': 'Clientes Promedio', 'Aprobado': True, 'Factor_Linea': 0.07, 'Tasa': 25, 'TEA': '25.0%',
            'Detalle': 'Comportamiento financiero regular y lineal. Riesgo de default controlado bajo estándares históricos.', 'Accion': 'Aprobación Estándar. Proceder con el embozo de Tarjeta Clásica con beneficios de retail integrados.' },
    'C3': { 'Nombre': 'Clientes VIP', 'Aprobado': True, 'Factor_Linea': 0.15, 'Tasa': 12, 'TEA': '12.5%',
            'Detalle': 'Máximo escalafón de ingresos y tracción comercial interna muy alta. Excelente liquidez demostrada.', 'Accion': 'Asignación Black Inmediata. Ofrecer tasa preferencial corporativa y acceso exclusivo a salas VIP.' },
    'C4': { 'Nombre': 'Oportunidad de Oro', 'Aprobado': True, 'Factor_Linea': 0.11, 'Tasa': 16, 'TEA': '16.0%',
            'Detalle': 'Excelente respaldo económico pero baja interacción en el ecosistema actual. Alta capacidad de pago ociosa.', 'Accion': 'Estrategia de Captación. Brindar una línea extendida agresiva para incentivar la compra corporativa.' },
    'C5': { 'Nombre': 'Consumidores Impulsivos', 'Aprobado': True, 'Factor_Linea': 0.03, 'Tasa': 36, 'TEA': '36.0%',
            'Detalle': 'Flujo de gasto agresivo no respaldado por ingresos recurrentes consolidados. Riesgo de sobreendeudamiento.', 'Accion': 'Aprobación Controlada. Forzar línea preventiva acotada y vinculación de póliza de protección de desempleo.' }
}
resultado = politica_credito[nombre_cluster]
monto_calculado = int((ingresos_input * 1000) * resultado['Factor_Linea'])

# =====================================================================
# 4. CUADRO DE MANDO PRINCIPAL (DASHBOARD VISUAL INTERACTIVO)
# =====================================================================
st.markdown("### 📊 Analítica General del Mercado")
col_g1, col_g2, col_g3 = st.columns(3)
with col_g1:
    st.metric(label="👥 Historial Clientes Evaluados", value=f"{len(df):,} Perfiles", delta="Estable")
with col_g2:
    st.metric(label="💰 Liquidez Promedio de Clientes", value=f"${df['Ingresos_Reales'].mean():.1f} k$", delta="Mercado Alto")
with col_g3:
    st.metric(label="🛍️ Ticket de Gasto del Mall", value=f"{df['Gasto_Real'].mean():.1f} / 100 pts", delta="Estacionalidad")

st.markdown("---")

col_dec1, col_dec2 = st.columns([1.1, 1])

with col_dec1:
    st.markdown("### ⚡ Motor Predictivo Automático")
    
    if resultado['Aprobado']:
        st.markdown(f"""
        <div class='decision-card-approved'>
            <h3 style='margin:0; color:#27ae60;'>🟢 SOLICITUD EVALUADA: CRÉDITO AUTORIZADO</h3>
            <p style='margin: 5px 0 0 0; font-size:1rem; color:#cbd5e1;'>Asignación de Riesgo exitosa para el segmento: <b>{nombre_cluster} - {resultado['Nombre']}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric(label="Línea Máxima Autorizada", value=f"${monto_calculado:,} USD")
        with col_res2:
            st.metric(label="Tasa de Interés Equivalente (TEA)", value=resultado['TEA'])
    else:
        st.markdown(f"""
        <div class='decision-card-rejected'>
            <h3 style='margin:0; color:#c0392b;'>🔴 SOLICITUD EVALUADA: CRÉDITO RECHAZADO</h3>
            <p style='margin: 5px 0 0 0; font-size:1rem; color:#cbd5e1;'>El perfil analizado pertenece al clúster restrictivo: <b>{nombre_cluster} - {resultado['Nombre']}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric(label="Línea Máxima Autorizada", value="$0 USD")
        with col_res2:
            st.metric(label="Tasa de Interés Equivalente (TEA)", value="0.0%")

    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        st.markdown(f"""<div class='glass-panel'>
            <h5 style='color:#3498db; margin-top:0;'>🔍 Dictamen Técnico de Riesgos</h5>
            <p style='font-size:0.9rem; color:#cbd5e1; line-height:1.4;'>{resultado['Detalle']}</p>
        </div>""", unsafe_allow_html=True)
    with col_sub2:
        st.markdown(f"""<div class='glass-panel'>
            <h5 style='color:#fca311; margin-top:0;'>🚀 Estrategia de Cross-Selling</h5>
            <p style='font-size:0.9rem; color:#cbd5e1; line-height:1.4;'>{resultado['Accion']}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    resultado_evaluacion = pd.DataFrame([{
        "Ingresos_k$": ingresos_input, "Puntaje_Gasto": gasto_input, "Cluster": nombre_cluster,
        "Resolucion": "APROBADO" if resultado['Aprobado'] else "RECHAZADO", "Linea_USD": monto_calculado, "TEA": resultado['TEA']
    }])
    st.download_button(
        label="📥 Descargar Certificado de Auditoría Oficial",
        data=resultado_evaluacion.to_csv(index=False).encode('utf-8'),
        file_name=f"Dictamen_{nombre_cluster}.csv", mime="text/csv"
    )

with col_dec2:
    st.markdown("### 🎯 Respaldo Gráfico y Auditoría Visual")
    st.caption("Ubicación del solicitante actual frente a toda la población bajo el modelo matemático.")

    colores_riesgo = {'C1': '#95a5a6', 'C2': '#3498db', 'C3': '#fca311', 'C4': '#2ecc71', 'C5': '#e67e22'}
    fig1, ax1 = plt.subplots(figsize=(10, 5.2))
    
    # Ajuste armónico con el fondo refinado
    fig1.patch.set_facecolor('#111827')
    ax1.set_facecolor('#0b0f19')
    
    sns.scatterplot(
        data=df, x='Ingresos_Reales', y='Gasto_Real', 
        hue='Cluster_Final', palette=colores_riesgo, hue_order=['C1', 'C2', 'C3', 'C4', 'C5'], s=85, ax=ax1, alpha=0.75
    )
    
    ax1.scatter(ingresos_input, gasto_input, color='#e74c3c', s=350, marker='X', edgecolors='#ffffff', linewidths=2, label='CLIENTE EN VENTANILLA')
    
    ax1.set_title('Distribución Geométrica de Clientes por Inteligencia Artificial', color='#ffffff', fontsize=11, fontweight='bold')
    ax1.set_xlabel('Capacidad de Ingresos Anuales (miles de USD)', color='#94a3b8')
    ax1.set_ylabel('Ratio de Gasto Interno (1-100)', color='#94a3b8')
    ax1.tick_params(colors='#94a3b8')
    ax1.grid(True, linestyle=':', alpha=0.15, color='#ffffff')
    
    ax1.legend(loc='upper right', facecolor='#111827', edgecolor='#34495e', labelcolor='white')
    st.pyplot(fig1)

# =====================================================================
# 5. SECCIÓN INFORMATIVA DE MÁRKETING (GLOSARIO)
# =====================================================================
st.markdown("---")
st.markdown("### 📖 Manual de Segmentación de Clientes y Criterios Comerciales")

col_info_img1, col_info_img2 = st.columns([2, 1])
with col_info_img1:
    with st.expander("📌 Clúster C1 — Ahorradores Cuidadosos (Bajos Ingresos / Bajo Gasto)"):
        st.markdown("**Ubicación:** Esquina inferior izquierda. Perfil conservador con flujo controlado. No apto para colocación de líneas abiertas, priorizar captación pasiva.")
    with st.expander("📌 Clúster C2 — Clientes Promedio (Ingresos Medios / Gasto Medio)"):
        st.markdown("**Ubicación:** Núcleo central de población. Perfil ideal para productos clásicos masivos de alta retención.")
    with st.expander("📌 Clúster C3 — Clientes VIP (Altos Ingresos / Alto Gasto)"):
        st.markdown("**Ubicación:** Esquina superior derecha. Máxima rentabilidad institucional, requiere atención preferencial inmediata y cross-selling premium.")
    with st.expander("📌 Clúster C4 — Oportunidad de Oro (Altos Ingresos / Bajo Gasto)"):
        st.markdown("**Ubicación:** Esquina inferior derecha. Alta capacidad de pago subutilizada. Objetivo clave para campañas de fidelización.")
    with st.expander("📌 Clúster C5 — Consumidores Impulsivos (Bajos Ingresos / Alto Gasto)"):
        st.markdown("**Ubicación:** Esquina superior izquierda. Alta tracción de consumo pero perfil volátil, requiere topes estrictos.")

with col_info_img2:
    st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=500&q=80", caption="Análisis Avanzado de Datos")