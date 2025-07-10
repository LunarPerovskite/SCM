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
    page_icon="☕",
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
display_project_context()
display_educational_content()

# Risk comparison charts
st.markdown("---")
st.markdown("## 📊 Comparación de Niveles de Riesgo por Municipio")

# Get municipalities data
municipalities_data = get_municipalities_data()
df_municipalities = pd.DataFrame(municipalities_data)

# Create columns for charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎯 Nivel de Susceptibilidad")
    fig1 = create_risk_chart(df_municipalities)
    st.pyplot(fig1)

with col2:
    st.markdown("### ☕ Área Cafetera en Riesgo")
    fig2 = create_scatter_chart(df_municipalities)
    st.pyplot(fig2)

# Data table
st.markdown("### 📋 Tabla Detallada de Municipios")
display_data_table(df_municipalities)

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
        show_faults=sidebar_controls['show_faults']
    )
    map_data = st_folium(m, width=1000, height=700, returned_objects=["last_object_clicked"])
except Exception as e:
    st.error(f"Error al cargar el mapa: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# Display footer
display_footer()
