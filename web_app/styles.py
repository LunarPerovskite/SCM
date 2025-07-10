import streamlit as st

def load_css():
    """Load custom CSS for the application"""
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
