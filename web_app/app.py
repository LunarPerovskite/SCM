import streamlit as st
from streamlit_folium import st_folium
import pandas as pd

# Import custom modules
from styles import load_css
from sidebar import create_sidebar
from content import (
    display_header, 
    display_project_context, 
    display_educational_content,
    display_statistics_cards,
    display_footer
)
from charts import (
    get_municipalities_data,
    create_risk_chart,
    create_scatter_chart,
    display_data_table
)
from map_components import create_map

# Page configuration
st.set_page_config(
    page_title="Susceptibilidad a Derrumbes - Caldas, Colombia",
    page_icon="⛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_css()

# Display header
display_header()

# Create sidebar and get controls
sidebar_controls = create_sidebar()

# Display project context and educational content
st.markdown("## Tecnologías Usadas")

# Create columns for cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background-color: #333; padding: 15px; border-radius: 10px; color: #fff;">
        <h3 style="color: #007BFF;">Satélites y fuentes de datos</h3>
        <ul style="list-style-type: none; padding-left: 0;">
            <li><b>CHIRPS</b>: Precipitación máxima promedio histórica (resolución 5 km, reprocesado a 30 m)</li>
            <li><b>MODIS</b>: NDVI promedio 2009–presente</li>
            <li><b>SRTM</b>: Elevación, pendiente, TRI y TWI</li>
            <li><b>SGC</b>: Geología y fallas geológicas</li>
            <li><b>SIMMA</b>: Inventario de deslizamientos desde 2009</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: #333; padding: 15px; border-radius: 10px; color: #fff;">
        <h3 style="color: #28A745;">Procesamiento y modelado</h3>
        <ul style="list-style-type: none; padding-left: 0;">
            <li><b>Google Earth Engine (GEE)</b>: Extracción y preprocesamiento de variables</li>
            <li><b>Python</b>: Librerías como rasterio, numpy, scikit-learn y TensorFlow/Keras</li>
            <li><b>Modelos ML</b>: Random Forest, XGBoost y Red Neuronal Convolucional (CNN)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background-color: #333; padding: 15px; border-radius: 10px; color: #fff;">
        <h3 style="color: #FFC107;">Visualización</h3>
        <ul style="list-style-type: none; padding-left: 0;">
            <li>Página web desarrollada con React + Leaflet para mapas interactivos</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# Statistics cards
display_statistics_cards()

# Main Map Section
st.markdown("---")
st.markdown("## 🗺️ Mapa de Susceptibilidad - Departamento de Caldas")

# Full width map
st.markdown('<div class="map-container">', unsafe_allow_html=True)

# Create and display map
try:
    m = create_map(
        show_landslides=sidebar_controls['show_landslides'],
        show_faults=sidebar_controls['show_faults'],
        show_area=sidebar_controls['show_area']
    )
    # Display the map using st_folium
    st_folium(m, width=700, height=600)
except Exception as e:
    st.error(f"Error al cargar el mapa: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# Display footer
display_footer()
