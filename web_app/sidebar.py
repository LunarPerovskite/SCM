import streamlit as st

def create_sidebar():
    """Create the sidebar with controls and legend"""
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
        
        # Shapefile layer controls
        st.markdown("### 🗺️ Capas de Datos")
        
        show_landslides = st.checkbox("Deslizamientos históricos", value=True, help="Mostrar eventos de deslizamientos registrados")
        show_faults = st.checkbox("Fallas geológicas", value=True, help="Mostrar fallas y fracturas geológicas")
        show_area = st.checkbox("Área de Estudio", value=True, help="Mostrar área de estudio")
        
        st.markdown("---")
        
        # Simplified Legend
        st.markdown("## 🎨 Leyenda del Mapa")
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
            <h5 style="color: #FFC107; margin-bottom: 0.8rem;">Susceptibilidad</h5>
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
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="width: 15px; height: 15px; background: #F44336; margin-right: 0.5rem; border-radius: 3px;"></div>
                <span style="color: white;">Muy Alto</span>
            </div>
            
            <h5 style="color: #FFC107; margin-bottom: 0.8rem;">Capas de Datos</h5>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div style="width: 15px; height: 15px; background: red; margin-right: 0.5rem; border-radius: 3px;"></div>
                <span style="color: white;">Deslizamientos</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 15px; height: 15px; background: purple; margin-right: 0.5rem; border-radius: 3px;"></div>
                <span style="color: white;">Fallas Geológicas</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        return {
            'risk_levels': risk_levels,
            'opacity': opacity,
            'show_slopes': show_slopes,
            'show_geology': show_geology,
            'show_coffee': show_coffee,
            'show_landslides': show_landslides,
            'show_faults': show_faults,
            'show_area': show_area
        }
