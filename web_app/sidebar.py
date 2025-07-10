import streamlit as st

def create_sidebar():
    """Create the sidebar with controls and legend"""
    with st.sidebar:
        # Removed "Configuración" and "Leyenda del Mapa" sections
        
        # Shapefile layer controls
        st.markdown("### 🗺️ Capas de Datos")
        
        show_landslides = st.checkbox("Deslizamientos históricos", value=True, help="Mostrar eventos de deslizamientos registrados")
        show_faults = st.checkbox("Fallas geológicas", value=True, help="Mostrar fallas y fracturas geológicas")
        show_area = st.checkbox("Área de Estudio", value=True, help="Mostrar área de estudio")
        
        st.markdown("---")
        
        return {
            'show_landslides': show_landslides,
            'show_faults': show_faults,
            'show_area': show_area
        }
