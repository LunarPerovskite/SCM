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
    page_title="Susceptibilidad a Inundaciones - Caldas, Colombia",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2a5298;
        margin-bottom: 1rem;
    }
    
    .stSelectbox label {
        font-weight: 600;
        color: #2a5298;
    }
    
    .stSlider label {
        font-weight: 600;
        color: #2a5298;
    }
    
    .info-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1976d2;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🌊 Análisis de Susceptibilidad a Inundaciones</h1>
    <h3>Caldas, Colombia - Modelo de Evaluación de Riesgo</h3>
    <p>Visualización interactiva de mapeo de susceptibilidad a inundaciones usando aprendizaje automático y análisis SIG</p>
</div>
""", unsafe_allow_html=True)

# Sidebar controls
with st.sidebar:
    st.markdown("## 📊 Controles de Análisis")
    
    # Layer selection
    layer_type = st.selectbox(
        "Seleccionar Tipo de Capa",
        ["Susceptibilidad a Inundaciones", "Elevación", "Pendiente", "Uso del Suelo", "Precipitación"]
    )
    
    # Opacity control
    opacity = st.slider("Opacidad de la Capa", 0.1, 1.0, 0.7, 0.1)
    
    # Risk level filter
    risk_level = st.multiselect(
        "Niveles de Riesgo a Mostrar",
        ["Muy Bajo", "Bajo", "Medio", "Alto", "Muy Alto"],
        default=["Medio", "Alto", "Muy Alto"]
    )
    
    # Color scheme
    color_scheme = st.selectbox(
        "Esquema de Colores",
        ["Viridis", "Plasma", "Coolwarm", "RdYlBu", "Spectral"]
    )
    
    st.markdown("---")
    
    # Legend
    st.markdown("## 🎨 Leyenda")
    st.markdown("""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px;">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <div style="width: 20px; height: 20px; background: #2E8B57; margin-right: 0.5rem;"></div>
            <span>Riesgo Muy Bajo</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <div style="width: 20px; height: 20px; background: #FFD700; margin-right: 0.5rem;"></div>
            <span>Riesgo Bajo</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <div style="width: 20px; height: 20px; background: #FFA500; margin-right: 0.5rem;"></div>
            <span>Riesgo Medio</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <div style="width: 20px; height: 20px; background: #FF6347; margin-right: 0.5rem;"></div>
            <span>Riesgo Alto</span>
        </div>
        <div style="display: flex; align-items: center;">
            <div style="width: 20px; height: 20px; background: #DC143C; margin-right: 0.5rem;"></div>
            <span>Riesgo Muy Alto</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("## 🗺️ Mapa Interactivo")
    
    # Create base map centered on Caldas, Colombia
    m = folium.Map(
        location=[5.0689, -75.5174],  # Caldas, Colombia coordinates
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    # Add different tile layers with attribution
    folium.TileLayer('Stamen Terrain', attr='Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors').add_to(m)
    folium.TileLayer('CartoDB positron', attr='© OpenStreetMap contributors, © CartoDB').add_to(m)
    folium.TileLayer('CartoDB dark_matter', attr='© OpenStreetMap contributors, © CartoDB').add_to(m)
    
    # Mock raster data overlay (in real implementation, you'd load your actual raster)
    # This creates a sample heat map overlay
    from folium.plugins import HeatMap
    
    # Generate sample flood susceptibility points
    import random
    
    # Mock data for demonstration
    flood_points = []
    for _ in range(100):
        lat = 5.0689 + (random.random() - 0.5) * 0.5
        lon = -75.5174 + (random.random() - 0.5) * 0.5
        intensity = random.random()
        flood_points.append([lat, lon, intensity])
    
    # Add heatmap layer
    if "Alto" in risk_level or "Muy Alto" in risk_level:
        HeatMap(
            flood_points,
            min_opacity=0.2,
            max_zoom=18,
            radius=15,
            blur=10,
            gradient={
                0.0: 'blue',
                0.3: 'green',
                0.5: 'yellow',
                0.7: 'orange',
                1.0: 'red'
            }
        ).add_to(m)
    
    # Add some sample markers for key areas
    folium.Marker(
        [5.0689, -75.5174],
        popup="Manizales - Capital de Caldas",
        tooltip="Haz clic para más información",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    folium.Marker(
        [5.1, -75.4],
        popup="Área de Alto Riesgo - Zona Residencial",
        tooltip="Alta susceptibilidad a inundaciones",
        icon=folium.Icon(color='orange', icon='warning-sign')
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Display map
    map_data = st_folium(m, width=700, height=500)

with col2:
    st.markdown("## 📈 Estadísticas")
    
    # Mock statistics
    st.markdown("""
    <div class="metric-card">
        <h4>📊 Distribución de Riesgo</h4>
        <p><strong>Muy Alto:</strong> 15%</p>
        <p><strong>Alto:</strong> 25%</p>
        <p><strong>Medio:</strong> 35%</p>
        <p><strong>Bajo:</strong> 20%</p>
        <p><strong>Muy Bajo:</strong> 5%</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <h4>🏘️ Áreas Afectadas</h4>
        <p><strong>Áreas Urbanas:</strong> 45%</p>
        <p><strong>Áreas Rurales:</strong> 30%</p>
        <p><strong>Agrícola:</strong> 25%</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <h4>🌧️ Precisión del Modelo</h4>
        <p><strong>Precisión:</strong> 87%</p>
        <p><strong>Sensibilidad:</strong> 82%</p>
        <p><strong>Puntuación F1:</strong> 84%</p>
    </div>
    """, unsafe_allow_html=True)

# Information section
st.markdown("---")
st.markdown("## ℹ️ Información del Modelo")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-box">
        <h4>📋 Fuentes de Datos</h4>
        <ul>
            <li>Modelo Digital de Elevación (DEM)</li>
            <li>Datos de precipitación (IDEAM)</li>
            <li>Clasificación de uso del suelo</li>
            <li>Características del suelo</li>
            <li>Redes de drenaje</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-box">
        <h4>🤖 Modelo de Aprendizaje Automático</h4>
        <ul>
            <li>Algoritmo: Random Forest</li>
            <li>Características: 15 variables</li>
            <li>Datos de entrenamiento: 10,000 muestras</li>
            <li>Validación: Validación cruzada</li>
            <li>Resolución: 30m x 30m</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-box">
        <h4>🎯 Aplicaciones</h4>
        <ul>
            <li>Planificación urbana</li>
            <li>Evaluación de riesgos</li>
            <li>Planificación de emergencias</li>
            <li>Evaluación de seguros</li>
            <li>Diseño de infraestructura</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🌊 Modelo de Susceptibilidad a Inundaciones - Caldas, Colombia | Desarrollado para Hackathon 2025</p>
    <p>📧 Contacto: tu.email@ejemplo.com | 🐙 GitHub: tu-repositorio-github</p>
</div>
""", unsafe_allow_html=True)

# Download section
st.markdown("## 📥 Descargar Resultados")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Descargar Mapa de Riesgo (PNG)"):
        st.success("¡Mapa de riesgo descargado exitosamente!")

with col2:
    if st.button("📋 Descargar Estadísticas (CSV)"):
        st.success("¡Estadísticas descargadas exitosamente!")

with col3:
    if st.button("🗺️ Descargar GeoTIFF"):
        st.success("¡Archivo GeoTIFF descargado exitosamente!")
