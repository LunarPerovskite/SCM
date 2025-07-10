import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def get_municipalities_data():
    """Get the municipalities data"""
    return {
        "Municipio": ["Manizales", "Chinchiná", "Villamaría", "Palestina", "Neira", "Aranzazu", "La Dorada", "Riosucio"],
        "Riesgo": [0.92, 0.75, 0.88, 0.65, 0.85, 0.78, 0.45, 0.58],
        "Población": [434000, 56000, 53000, 18000, 32000, 12000, 74000, 64000],
        "Área_Cafetera_km2": [85.2, 42.1, 38.7, 25.3, 55.8, 31.2, 12.5, 47.3]
    }

def create_risk_chart(df_municipalities):
    """Create the risk level bar chart"""
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    colors = ['#F44336' if risk > 0.8 else '#FF9800' if risk > 0.6 else '#FFC107' for risk in df_municipalities["Riesgo"]]
    bars = ax1.bar(df_municipalities["Municipio"], df_municipalities["Riesgo"], color=colors)
    ax1.set_title("Susceptibilidad a Deslizamientos por Municipio", fontsize=14, fontweight='bold')
    ax1.set_ylabel("Índice de Susceptibilidad (0-1)")
    ax1.set_ylim(0, 1)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Set dark background
    fig1.patch.set_facecolor('#181c1b')
    ax1.set_facecolor('#181c1b')
    ax1.tick_params(colors='white')
    ax1.xaxis.label.set_color('white')
    ax1.yaxis.label.set_color('white')
    ax1.title.set_color('white')
    ax1.spines['bottom'].set_color('white')
    ax1.spines['top'].set_color('white')
    ax1.spines['right'].set_color('white')
    ax1.spines['left'].set_color('white')
    
    return fig1

def create_scatter_chart(df_municipalities):
    """Create the coffee area vs risk scatter plot"""
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    colors = ['#F44336' if risk > 0.8 else '#FF9800' if risk > 0.6 else '#FFC107' for risk in df_municipalities["Riesgo"]]
    ax2.scatter(df_municipalities["Área_Cafetera_km2"], df_municipalities["Riesgo"], 
                s=df_municipalities["Población"]/1000, alpha=0.7, c=colors)
    ax2.set_xlabel("Área Cafetera (km²)")
    ax2.set_ylabel("Índice de Susceptibilidad")
    ax2.set_title("Relación: Área Cafetera vs Susceptibilidad", fontsize=14, fontweight='bold')
    
    # Add municipality labels
    for i, txt in enumerate(df_municipalities["Municipio"]):
        ax2.annotate(txt, (df_municipalities["Área_Cafetera_km2"][i], df_municipalities["Riesgo"][i]),
                    xytext=(5, 5), textcoords='offset points', fontsize=8, color='white')
    
    # Set dark background
    fig2.patch.set_facecolor('#181c1b')
    ax2.set_facecolor('#181c1b')
    ax2.tick_params(colors='white')
    ax2.xaxis.label.set_color('white')
    ax2.yaxis.label.set_color('white')
    ax2.title.set_color('white')
    ax2.spines['bottom'].set_color('white')
    ax2.spines['top'].set_color('white')
    ax2.spines['right'].set_color('white')
    ax2.spines['left'].set_color('white')
    
    plt.tight_layout()
    return fig2

def display_data_table(df_municipalities):
    """Display the municipalities data table"""
    df_display = df_municipalities.copy()
    df_display["Riesgo"] = df_display["Riesgo"].apply(lambda x: f"{x:.2f}")
    df_display["Población"] = df_display["Población"].apply(lambda x: f"{x:,}")
    df_display.columns = ["Municipio", "Susceptibilidad", "Población", "Área Cafetera (km²)"]
    st.dataframe(df_display, use_container_width=True)
