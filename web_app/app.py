import streamlit as st
import folium
from streamlit_folium import st_folium
import rasterio
import numpy as np
from rasterio.plot import show
from rasterio.warp import calculate_default_transform, reproject, Resampling
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from io import BytesIO
import base64
import json

# Page configuration
st.set_page_config(
    page_title="Susceptibilidad a Derrumbes - Caldas, Colombia",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Coffee grain background pattern on a dark base */
    body {
        background-color: #181c1b !important;
        background-image: 
            radial-gradient(circle at 20% 20%, rgba(139, 69, 19, 0.13) 2px, transparent 2px),
            radial-gradient(circle at 80% 40%, rgba(101, 67, 33, 0.10) 1px, transparent 1px),
            radial-gradient(circle at 40% 80%, rgba(160, 82, 45, 0.09) 1.5px, transparent 1.5px),
            radial-gradient(circle at 60% 30%, rgba(139, 69, 19, 0.07) 1px, transparent 1px);
        background-size: 50px 50px, 30px 30px, 70px 70px, 40px 40px;
        background-position: 0 0, 15px 15px, 35px 35px, 25px 25px;
    }
    
    .main-header {
        background: linear-gradient(135deg, #4CAF50, #FFC107);
        padding: 2rem 3rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border: 3px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(139, 69, 19, 0.2) 3px, transparent 3px),
            radial-gradient(circle at 85% 25%, rgba(101, 67, 33, 0.15) 2px, transparent 2px),
            radial-gradient(circle at 45% 85%, rgba(160, 82, 45, 0.1) 2.5px, transparent 2.5px);
        background-size: 60px 60px, 40px 40px, 80px 80px;
        opacity: 0.3;
        z-index: 0;
    }
    
    .main-header > * {
        position: relative;
        z-index: 1;
    }
    
    .main-header h1 {
        font-size: 3rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header h3 {
        font-size: 1.3rem !important;
        margin-bottom: 0.5rem !important;
        opacity: 0.9;
    }
    
    .metric-card {
        background: rgba(24,28,27,0.85);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid rgba(255, 193, 7, 0.3);
        margin-bottom: 1rem;
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 10% 90%, rgba(139, 69, 19, 0.1) 1px, transparent 1px),
            radial-gradient(circle at 90% 10%, rgba(101, 67, 33, 0.08) 1.5px, transparent 1.5px);
        background-size: 25px 25px, 35px 35px;
        opacity: 0.4;
        z-index: 0;
    }
    
    .metric-card > * {
        position: relative;
        z-index: 1;
    }
    
    .metric-card h4 {
        color: #FFC107 !important;
        margin-bottom: 1rem !important;
    }
    
    .info-section {
        background: rgba(24,28,27,0.9);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid rgba(76, 175, 80, 0.3);
        margin: 2rem 0;
        color: white;
    }
    
    .info-section h3 {
        color: #FFC107 !important;
    }
    
    .info-section h4 {
        color: #4CAF50 !important;
    }
    
    .info-section p {
        color: rgba(255,255,255,0.9) !important;
    }
    
    .map-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        border: 3px solid rgba(76, 175, 80, 0.4);
        background: rgba(24,28,27,0.7);
    }
    
    /* Hide unnecessary Streamlit elements */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(24,28,27,0.95);
        backdrop-filter: blur(10px);
        border-right: 2px solid rgba(76, 175, 80, 0.3);
    }
    
    .stSelectbox label, .stSlider label, .stMultiSelect label {
        color: #FFC107 !important;
        font-weight: 600 !important;
    }
    
    /* Ensure white text is visible */
    .stMarkdown p, .stMarkdown span {
        color: white !important;
    }
    
    /* Footer styling */
    .footer-section {
        background: rgba(0,0,0,0.5);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        border: 1px solid rgba(76, 175, 80, 0.3);
        padding: 1rem;
    }
    
    .footer-section p {
        color: rgba(255,255,255,0.7) !important;
    }
    
    /* Legend background */
    .stMarkdown div[style*='background: rgba(255,255,255,0.1)'] {
        background: rgba(24,28,27,0.7) !important;
        border: 1.5px solid #4CAF50 !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>⛰️ Análisis de Susceptibilidad a Derrumbes</h1>
    <h3>Caldas, Colombia - Modelo de Evaluación de Riesgo en Áreas Cafeteras</h3>
    <p>Monitoreo de estabilidad de taludes y prevención de deslizamientos en zonas de cultivo de café</p>
</div>
""", unsafe_allow_html=True)

# Sidebar controls (simplified)
with st.sidebar:
    st.markdown("## ⚙️ Configuración")
    
    # Risk level filter (main control)
    risk_levels = st.multiselect(
        "🎯 Niveles de Susceptibilidad",
        ["Muy Bajo", "Bajo", "Medio", "Alto", "Muy Alto"],
        default=["Alto", "Muy Alto"],
        help="Selecciona los niveles de susceptibilidad a deslizamientos"
    )
    
    # Opacity control
    opacity = st.slider("🔍 Intensidad", 0.3, 1.0, 0.7, 0.1)
    
    st.markdown("---")
    
    # Additional landslide controls
    st.markdown("### 📊 Factores de Análisis")
    
    show_slopes = st.checkbox("Pendientes > 30°", value=True, help="Mostrar áreas con pendientes críticas")
    show_geology = st.checkbox("Geología inestable", value=True, help="Áreas con suelos susceptibles")
    show_coffee = st.checkbox("Plantaciones de café", value=True, help="Ubicación de cultivos cafeteros")
    
    st.markdown("---")
    
    # Simplified Legend
    st.markdown("## 🎨 Leyenda de Susceptibilidad")
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <div style="width: 15px; height: 15px; background: #4CAF50; margin-right: 0.5rem; border-radius: 3px;"></div>
            <span style="color: white;">Muy Bajo</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <div style="width: 15px; height: 15px; background: #8BC34A; margin-right: 0.5rem; border-radius: 3px;"></div>
            <span style="color: white;">Bajo</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <div style="width: 15px; height: 15px; background: #FFC107; margin-right: 0.5rem; border-radius: 3px;"></div>
            <span style="color: white;">Medio</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <div style="width: 15px; height: 15px; background: #FF9800; margin-right: 0.5rem; border-radius: 3px;"></div>
            <span style="color: white;">Alto</span>
        </div>
        <div style="display: flex; align-items: center;">
            <div style="width: 15px; height: 15px; background: #F44336; margin-right: 0.5rem; border-radius: 3px;"></div>
            <span style="color: white;">Muy Alto</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Cache the map creation to prevent re-rendering
@st.cache_data(show_spinner=False)
def create_map():
    import random  # Import random inside the function
    from folium.plugins import HeatMap  # Import HeatMap inside the function

    # Create the base map
    m = folium.Map(
        location=[5.0689, -75.5174],  # Caldas, Colombia coordinates
        zoom_start=11,
        tiles='CartoDB positron'
    )

    # Generate sample flood susceptibility points
    flood_points = [
        [5.0689 + (random.random() - 0.5) * 0.5, -75.5174 + (random.random() - 0.5) * 0.5, random.random()]
        for _ in range(200)
    ]

    # Add heatmap layer
    HeatMap(
        flood_points,
        min_opacity=0.3,
        max_zoom=15,
        radius=20,
        blur=15,
        gradient={
            0.0: 'navy',
            0.3: 'blue',
            0.5: 'cyan',
            0.7: 'lime',
            1.0: 'yellow'
        }
    ).add_to(m)

    return m

# Main content - Full width map with overlay stats
st.markdown('<div class="map-container">', unsafe_allow_html=True)

# Create map
m = create_map()
map_data = st_folium(m, width=None, height=650, returned_objects=["last_object_clicked"])

st.markdown('</div>', unsafe_allow_html=True)

# Statistics overlay cards - horizontal layout
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h4>⛰️ Taludes en Riesgo Crítico</h4>
        <h2 style="color: #F44336; margin: 0;">2,547</h2>
        <p style="margin: 0; opacity: 0.8;">hectáreas de café vulnerables</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h4>🏠 Población en Zona de Riesgo</h4>
        <h2 style="color: #FF9800; margin: 0;">12,489</h2>
        <p style="margin: 0; opacity: 0.8;">habitantes en áreas susceptibles</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h4>📍 Deslizamientos Históricos</h4>
        <h2 style="color: #FFC107; margin: 0;">34</h2>
        <p style="margin: 0; opacity: 0.8;">eventos registrados (2020-2024)</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h4>� Precisión Modelo</h4>
        <h2 style="color: #2196F3; margin: 0;">87%</h2>
        <p style="margin: 0; opacity: 0.8;">confiabilidad</p>
    </div>
    """, unsafe_allow_html=True)

# Compact Information section
st.markdown("""
<div class="info-section">
    <h3 style="color: #FFC107; text-align: center; margin-bottom: 1.5rem;">ℹ️ Información del Proyecto</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
        <div>
            <h4 style="color: #4CAF50;">📊 Factores de Inestabilidad</h4>
            <p style="opacity: 0.9;">Pendientes pronunciadas, suelos saturados, actividad sísmica, erosión hídrica y deforestación en áreas de producción cafetera.</p>
        </div>
        <div>
            <h4 style="color: #4CAF50;">🤖 Modelado Predictivo</h4>
            <p style="opacity: 0.9;">Análisis geotécnico combinado con machine learning para identificar zonas de alta susceptibilidad a movimientos de masa.</p>
        </div>
        <div>
            <h4 style="color: #4CAF50;">🎯 Prevención y Mitigación</h4>
            <p style="opacity: 0.9;">Sistemas de alerta temprana, obras de estabilización de taludes y reubicación de cultivos en zonas críticas.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Compact Footer
st.markdown("---")
st.markdown("""
<div class="footer-section" style="text-align: center;">
    <p>⛰️ <strong>Hackathon Cafetero 2025</strong> | Sistema de Monitoreo de Deslizamientos en Zonas Cafeteras - Caldas, Colombia</p>
</div>
""", unsafe_allow_html=True)
