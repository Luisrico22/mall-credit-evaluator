import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import os

# =====================================================================
# CONFIGURACIÓN DE LA INTERFAZ BANCARIA / RETAIL
# =====================================================================
st.set_page_config(page_title="Mall Credit Evaluator", layout="wide", page_icon="💳")

st.title("💳 Sistema de Evaluación Crediticia e Inteligencia de Riesgos")
st.markdown("### `Módulo de Consulta Exclusivo para Asesores Financieros`")
st.markdown("Este portal evalúa en tiempo real las solicitudes de crédito utilizando el algoritmo K-Means sincronizado directamente con el comportamiento financiero del cliente.")

# =====================================================================
# 1. CARGA DE DATOS ORIGINALES (Sincronización Inteligente de Clústeres)
# =====================================================================
@st.cache_data
def cargar_y_procesar_datos():
    ruta = "Mall_Customers_wa.tab"
    
    if not os.path.exists(ruta):
        st.error(f"⚠️ ¡Archivo de datos no detectado! Por favor asegúrate de copiar el archivo 'Mall_Customers_wa.tab' dentro de la carpeta del proyecto: {os.getcwd()}")
        st.stop()
        
    df_local = pd.read_csv(ruta, sep='\t', skiprows=[1, 2])
    
    min_inc, max_inc = 15.0, 137.0
    min_exp, max_exp = 1.0, 99.0
    
    df_local['Ingresos_Reales'] = df_local['Annual Income (k$)'] * (max_inc - min_inc) + min_inc
    df_local['Gasto_Real'] = df_local['Spending Score (1-100)'] * (max_exp - min_exp) + min_exp
    
    X = df_local[['Annual Income (k$)', 'Spending Score (1-100)']]
    
    kmeans_model = KMeans(n_clusters=5, random_state=42, n_init=10)
    df_local['Cluster_Predicho'] = kmeans_model.fit_predict(X)
    
    centros = df_local.groupby('Cluster_Predicho')[['Ingresos_Reales', 'Gasto_Real']].mean()
    mapeo_inteligente = {}
    
    for idx, row in centros.iterrows():
        inc = row['Ingresos_Reales']
        exp = row['Gasto_Real']
        
        if inc < 50 and exp < 40:
            mapeo_inteligente[idx] = 'C1'
        elif inc > 65 and exp > 60:
            mapeo_inteligente[idx] = 'C3'
        elif inc > 65 and exp < 40:
            mapeo_inteligente[idx] = 'C4'
        elif inc < 50 and exp > 60:
            mapeo_inteligente[idx] = 'C5'
        else:
            mapeo_inteligente[idx] = 'C2'

    if len(set(mapeo_inteligente.values())) < 5:
        mapeo_inteligente = {0: 'C5', 1: 'C1', 2: 'C3', 3: 'C2', 4: 'C4'}
        
    df_local['Cluster_Final'] = df_local['Cluster_Predicho'].map(mapeo_inteligente)
    
    return df_local, kmeans_model, min_inc, max_inc, min_exp, max_exp, mapeo_inteligente

df, kmeans, min_inc, max_inc, min_exp, max_exp, mapa_clústeres = cargar_y_procesar_datos()

# =====================================================================
# COMPONENTE DE MÉTRICAS GLOBALES DEL DATASET
# =====================================================================
st.markdown("---")
col_g1, col_g2, col_g3 = st.columns(3)
with col_g1:
    st.metric(label="📊 Población Histórica Analizada", value=f"{len(df)} Clientes")
with col_g2:
    st.metric(label="💰 Ingreso Anual Promedio del Mall", value=f"${df['Ingresos_Reales'].mean():.1f} k$")
with col_g3:
    st.metric(label="🛍️ Índice de Gasto Promedio", value=f"{df['Gasto_Real'].mean():.1f} / 100 pts")
st.markdown("---")

# =====================================================================
# 2. PANEL LATERAL: ENTRADA DE DATOS CON CONTROL DE LÍMITES (MEJORA 1)
# =====================================================================
with st.sidebar:
    st.header("📋 Formulario de Evaluación")
    st.write("Complete los datos financieros del solicitante:")
    
    ingresos_input = st.number_input("Ingresos Anuales del Cliente (k$):", min_value=1, max_value=250, value=60)
    gasto_input = st.number_input("Puntaje de Gasto Estimado (1-100):", min_value=1, max_value=100, value=50)
    
    # Alerta visual si se exceden los umbrales de confianza del modelo matemático
    if ingresos_input < min_inc or ingresos_input > max_inc:
        st.sidebar.warning(f"⚠️ El ingreso seleccionado está fuera del rango histórico de entrenamiento del algoritmo ({int(min_inc)}-{int(max_inc)} k$). Proceda con cautela.")

# =====================================================================
# 3. CONVERSIÓN MATEMÁTICA Y REGLAS FINANCIERAS
# =====================================================================
ingresos_norm = (ingresos_input - min_inc) / (max_inc - min_inc)
gasto_norm = (gasto_input - min_exp) / (max_exp - min_exp)

nuevo_cliente_norm = pd.DataFrame([{
    'Annual Income (k$)': ingresos_norm,
    'Spending Score (1-100)': gasto_norm
}])

cluster_id_raw = kmeans.predict(nuevo_cliente_norm)[0]
nombre_cluster = mapa_clústeres[cluster_id_raw]

# MEJORA 2: Factor multiplicador para el cálculo de líneas de crédito dinámicas basado en ingresos
politica_credito = {
    'C1': {
        'Nombre': 'Ahorradores Cuidadosos (Bajos Ingresos / Bajo Gasto)',
        'Aprobado': False, 'Factor_Linea': 0.00, 'Tasa': 0,
        'Detalle': 'El solicitante pertenece al segmento de Bajos Ingresos y Bajo Consumo. No cumple el umbral financiero mínimo exigido.',
        'Accion': 'RECHAZADO AUTOMÁTICAMENTE. Estrategia alternativa comercial: Ofrecer apertura de Cuenta de Débito Cero Comisiones para bancarizar al perfil.'
    },
    'C2': {
        'Nombre': 'Clientes Promedio (Ingresos Medios / Gasto Medio)',
        'Aprobado': True, 'Factor_Linea': 0.07, 'Tasa': 25, # 7% de sus ingresos anuales
        'Detalle': 'Perfil financiero de estabilidad intermedia. Presenta un riesgo controlado y un patrón de consumo lineal.',
        'Accion': 'APROBADO ESTÁNDAR: Emitir Tarjeta Clásica comercial. Habilitar tasa base de mercado.'
    },
    'C3': {
        'Nombre': 'Clientes VIP (Altos Ingresos / Alto Gasto)',
        'Aprobado': True, 'Factor_Linea': 0.15, 'Tasa': 12, # 15% de sus ingresos anuales
        'Detalle': 'Máxima solvencia patrimonial combinada con un flujo de consumo muy elevado. Mínimo riesgo de impago.',
        'Accion': 'APROBADO PREMIUM: Asignar Tarjeta Black con tasa preferencial mínima y beneficios de lealtad inmediatos.'
    },
    'C4': {
        'Nombre': 'Oportunidad de Oro (Altos Ingresos / Bajo Gasto)',
        'Aprobado': True, 'Factor_Linea': 0.11, 'Tasa': 16, # 11% de sus ingresos anuales
        'Detalle': 'El cliente cuenta con excelente capacidad de pago pero baja interacción de consumo interna.',
        'Accion': 'APROBADO ESTRATÉGICO: Otorgar línea competitiva alta para incentivar la migración de consumos externos al ecosistema del mall.'
    },
    'C5': {
        'Nombre': 'Consumidores Impulsivos (Bajos Ingresos / Alto Gasto)',
        'Aprobado': True, 'Factor_Linea': 0.03, 'Tasa': 36, # 3% de sus ingresos anuales
        'Detalle': 'Perfil con alta tendencia al gasto pero con nivel de ingresos declarado bajo. Riesgo de sobreendeudamiento acelerado.',
        'Accion': 'APROBADO CON RESTRICCIÓN DE SEGURIDAD: Limitar la línea a un cupo bajo preventivo. Sugerir la colocación de un seguro de protección de pagos obligatorio.'
    }
}

resultado = politica_credito[nombre_cluster]

# Cálculo de la línea de crédito dinámica multiplicada por el ingreso del cliente (en dólares reales)
monto_calculado = int((ingresos_input * 1000) * resultado['Factor_Linea'])

# =====================================================================
# 4. MONITOR DE EMISIÓN DE DICTAMEN
# =====================================================================
st.subheader("🖥️ Dictamen de Riesgos Automatizado")

if resultado['Aprobado']:
    st.markdown("## 🟢 RESOLUCIÓN: **CRÉDITO APROBADO**")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric(label="Línea de Crédito Autorizada (Calculada Dinámicamente)", value=f"${monto_calculado:,} USD")
    with col_m2:
        st.metric(label="Tasa de Interés Asignada (TEA)", value=f"{resultado['Tasa']}%")
    with col_m3:
        st.metric(label="Segmento Predictivo Identificado", value=nombre_cluster)
        
    c_info1, c_info2 = st.columns(2)
    with c_info1:
        st.info(f"**Análisis de Riesgo Integrado:**\n\n{resultado['Detalle']}\n\n*Perfil detectado: {resultado['Nombre']}*")
    with c_info2:
        st.success(f"**Protocolo Comercial y Cross-Selling (Mejora 3):**\n\n{resultado['Accion']}")
else:
    st.markdown("## 🔴 RESOLUCIÓN: **CRÉDITO RECHAZADO**")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric(label="Línea de Crédito Autorizada", value="$0 USD")
    with col_m2:
        st.metric(label="Segmento Predictivo Identificado", value=nombre_cluster)
        
    st.error(f"**Motivo del Rechazo del Sistema:**\n\n{resultado['Detalle']}\n\n*Perfil detectado: {resultado['Nombre']}*")
    st.warning(f"**Estrategia Comercial de Recuperación (Mejora 3):**\n\n{resultado['Accion']}")

# Botón de Descarga de Certificado de Auditoría
resultado_evaluacion = pd.DataFrame([{
    "Ingresos_k$": ingresos_input,
    "Puntaje_Gasto": gasto_input,
    "Cluster_Asignado": nombre_cluster,
    "Nombre_Perfil": resultado['Nombre'],
    "Resolucion_Oficial": "APROBADO" if resultado['Aprobado'] else "RECHAZADO",
    "Monto_Linea_USD": monto_calculado,
    "Tasa_Asignada_TEA": f"{resultado['Tasa']}%"
}])

st.download_button(
    label="📥 Descargar Certificado de Dictamen Oficial (Auditoría)",
    data=resultado_evaluacion.to_csv(index=False).encode('utf-8'),
    file_name=f"Dictamen_Cliente_{nombre_cluster}.csv",
    mime="text/csv"
)

st.markdown("---")

# =====================================================================
# 5. COMPONENTE DE AUDITABLE GRÁFICO EXACTO (PALETA CORPORATIVA)
# =====================================================================
st.subheader("📊 Evidencia y Respaldo Gráfico (Escala Comercial Real)")
st.caption(f"Visualizando el universo completo de {len(df)} registros históricos analizados por el algoritmo.")

colores_riesgo = {'C1': '#95a5a6', 'C2': '#3498db', 'C3': '#f1c40f', 'C4': '#2ecc71', 'C5': '#e67e22'}

fig1, ax1 = plt.subplots(figsize=(11, 4.2))
sns.scatterplot(
    data=df, x='Ingresos_Reales', y='Gasto_Real', 
    hue='Cluster_Final', palette=colores_riesgo, hue_order=['C1', 'C2', 'C3', 'C4', 'C5'], s=75, ax=ax1
)

ax1.scatter(ingresos_input, gasto_input, color='red', s=300, marker='X', edgecolors='black', label='SOLICITANTE EN VENTANILLA')

ax1.set_title('Ubicación Exacta del Solicitante Frente a la Población Comercial del Mall')
ax1.set_xlabel('Ingresos Anuales del Cliente (en miles de $)')
ax1.set_ylabel('Puntuación de Gasto Estimada (1-100)')
ax1.grid(True, linestyle='--', alpha=0.4)
ax1.legend(loc='upper right')
st.pyplot(fig1)

st.markdown("---")

# =====================================================================
# 6. GLOSARIO DE SEGMENTACIÓN Y CRITERIOS
# =====================================================================
st.subheader("📖 Glosario de Segmentación y Criterios del Algoritmo")
st.write("Haga clic en cada sección para desplegar el análisis estratégico y comercial de cada clúster obtenido:")

with st.expander("📍 Clúster C1 — Ahorradores Cuidadosos (Bajos Ingresos / Bajo Gasto)"):
    st.markdown("""
    * **Ubicación en el Mapa:** Esquina inferior izquierda (Color Gris).
    * **Comportamiento Comercial:** Clientes que asisten al centro comercial de manera muy medida. Su nivel de ingresos es bajo y cuidan rigurosamente su capacidad de endeudamiento, evitando compras innecesarias.
    * **Política de Riesgo:** **No sujeto a crédito.** El otorgamiento de líneas financieras en este segmento incrementa críticamente el riesgo de impago (Default), ya que no cuentan con un colchón patrimonial de respaldo.
    """)

with st.expander("📍 Clúster C2 — Clientes Promedio (Ingresos Medios / Gasto Medio)"):
    st.markdown("""
    * **Ubicación en el Mapa:** Zona central del gráfico (Color Azul).
    * **Comportamiento Comercial:** Representa el grueso del mercado convencional. Tienen ingresos estables y gastan de acuerdo a su presupuesto medio para actividades comunes del mall (cine, comida, ropa casual).
    * **Política de Riesgo:** **Aprobación estándar.** Perfil sumamente balanceado y predecible. Se les otorga una línea de crédito moderada con tasas de interés estándar para incentivar consumos recurrentes controlados.
    """)

with st.expander("📍 Clúster C3 — Clientes VIP (Altos Ingresos / Alto Gasto)"):
    st.markdown("""
    * **Ubicación en el Mapa:** Esquina superior derecha (Color Dorado).
    * **Comportamiento Comercial:** El segmento de mayor valor para el negocio (Premium). Poseen una solvencia financiera muy holgada y consumen productos o marcas exclusivas de alta gama dentro del mall.
    * **Política de Riesgo:** **Aprobación prioritaria e inmediata.** Es el perfil con la menor tasa de morosidad. Se les asignan las líneas de crédito más altas de la institución junto con tasas preferenciales mínimas para fidelizarlos en el ecosistema bancario.
    """)

with st.expander("📍 Clúster C4 — Oportunidad de Oro (Altos Ingresos / Bajo Gasto)"):
    st.markdown("""
    * **Ubicación en el Mapa:** Esquina inferior derecha (Color Verde).
    * **Comportamiento Comercial:** Clientes con un excelente poder adquisitivo pero que prácticamente no consumen dentro del centro comercial (prefieren ahorrar o gastar en otros canales).
    * **Política de Riesgo:** **Aprobación estratégica de atracción.** Tienen capacidad de pago de sobra. El objetivo con ellos es engancharlos ofreciéndoles una tarjeta de alta categoría con beneficios agresivos, forzándolos a trasladar sus consumos habituales hacia nuestros establecimientos.
    """)

with st.expander("📍 Clúster C5 — Consumidores Impulsivos (Bajos Ingresos / Alto Gasto)"):
    st.markdown("""
    * **Ubicación en el Mapa:** Esquina superior izquierda (Color Naranja).
    * **Comportamiento Comercial:** Clientes con ingresos limitados pero con una actividad de compra y endeudamiento desproporcionada. Son propensos a seguir modas y ofertas de alto impacto visual.
    * **Política de Riesgo:** **Aprobación restringida y monitoreada.** Representan el perfil más volátil. Se aprueba un monto mínimo para capturar el negocio de sus compras impulsivas, pero aplicando una tasa de interés elevada para mitigar el alto peligro latente de sobreendeudamiento a corto plazo.
    """)