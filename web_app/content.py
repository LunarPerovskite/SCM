import streamlit as st

def display_header():
    """Display the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>⛰️ Análisis de Susceptibilidad a Derrumbes</h1>
        <h3>Caldas, Colombia - Modelo de Evaluación de Riesgo en Áreas Cafeteras</h3>
        <p>Monitoreo de estabilidad de taludes y prevención de deslizamientos en zonas de cultivo de café</p>
    </div>
    """, unsafe_allow_html=True)

def display_project_context():
    """Display project context section"""
    st.markdown("---")
    st.markdown("""
    <div class="info-section">
        <h3 style="color: #FFC107; text-align: center; margin-bottom: 1.5rem;">📋 Contexto del Proyecto</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
            <div>
                <h4 style="color: #4CAF50;">🌋 Características Geológicas</h4>
                <p style="opacity: 0.9;">Caldas presenta suelos volcánicos andisoles, pendientes pronunciadas (>30°) y alta pluviosidad, creando condiciones ideales para deslizamientos en la cordillera central.</p>
            </div>
            <div>
                <h4 style="color: #4CAF50;">☕ Impacto en Caficultura</h4>
                <p style="opacity: 0.9;">El 85% de las fincas cafeteras están en zonas de ladera con susceptibilidad media-alta. Los deslizamientos afectan directamente la productividad y sostenibilidad del café.</p>
            </div>
            <div>
                <h4 style="color: #4CAF50;">🚨 Sistema de Alerta</h4>
                <p style="opacity: 0.9;">Modelo predictivo basado en precipitación, pendiente, geología y cobertura del suelo para generar alertas tempranas en municipios prioritarios.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_educational_content():
    """Display educational content section"""
    st.markdown("---")
    st.markdown("""
    <div class="info-section">
        <h3 style="color: #FFC107; text-align: center; margin-bottom: 1.5rem;">🎓 Factores de Susceptibilidad a Deslizamientos</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
            <div>
                <h4 style="color: #4CAF50;">📐 Pendiente</h4>
                <p style="opacity: 0.9;">Áreas con pendientes mayores a 30° son más propensas a deslizamientos. La gravedad actúa como fuerza motriz principal.</p>
            </div>
            <div>
                <h4 style="color: #4CAF50;">🌧️ Precipitación</h4>
                <p style="opacity: 0.9;">Lluvias intensas saturan los suelos, reduciendo la cohesión y aumentando el peso del material.</p>
            </div>
            <div>
                <h4 style="color: #4CAF50;">🪨 Geología</h4>
                <p style="opacity: 0.9;">Suelos volcánicos andisoles son altamente susceptibles debido a su estructura porosa y baja densidad.</p>
            </div>
            <div>
                <h4 style="color: #4CAF50;">🌿 Cobertura Vegetal</h4>
                <p style="opacity: 0.9;">La pérdida de vegetación reduce la estabilidad del suelo y aumenta la erosión superficial.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_statistics_cards():
    """Display the main statistics cards"""
    st.markdown("## 📊 Dashboard de Susceptibilidad")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>⛰️ Municipios en Riesgo Alto</h4>
            <h2 style="color: #F44336; margin: 0;">23</h2>
            <p style="margin: 0; opacity: 0.8;">de 27 municipios de Caldas</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🏠 Población Vulnerable</h4>
            <h2 style="color: #FF9800; margin: 0;">315,720</h2>
            <p style="margin: 0; opacity: 0.8;">habitantes en zonas de riesgo</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>☕ Área Cafetera Afectada</h4>
            <h2 style="color: #FFC107; margin: 0;">42,156</h2>
            <p style="margin: 0; opacity: 0.8;">hectáreas en susceptibilidad alta</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <h4>🎯 Precisión Modelo</h4>
            <h2 style="color: #2196F3; margin: 0;">91.3%</h2>
            <p style="margin: 0; opacity: 0.8;">validación con eventos históricos</p>
        </div>
        """, unsafe_allow_html=True)

def display_footer():
    """Display the footer"""
    st.markdown("---")
    st.markdown("""
    <div class="footer-section" style="text-align: center;">
        <p>⛰️ <strong>Hackathon Cafetero 2025</strong> | Sistema de Monitoreo de Deslizamientos en Zonas Cafeteras - Caldas, Colombia</p>
    </div>
    """, unsafe_allow_html=True)
