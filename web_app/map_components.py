import folium
import geopandas as gpd
import os
import streamlit as st

def create_map(show_landslides=True, show_faults=True, show_area=True, show_points=True):
    """Create the main folium map with shapefiles"""
    
    # Create the base map centered on Caldas
    m = folium.Map(
        location=[5.3, -75.4],  # Better center for Caldas
        zoom_start=8,
        tiles='OpenStreetMap'
    )
    
    # Add shapefiles to the map
    try:
        # Path to shapefiles
        base_path = "data/shps"
        
        # 1. Add landslides (Deslizamientos)
        if show_landslides:
            landslides_path = os.path.join(base_path, "Deslizamientos", "DESLIZAMIENTOS.shp")
            if os.path.exists(landslides_path):
                landslides = gpd.read_file(landslides_path)
                folium.GeoJson(
                    landslides,
                    style_function=lambda x: {
                        'fillColor': 'red',
                        'color': 'darkred',
                        'weight': 2,
                        'fillOpacity': 0.7
                    },
                    popup=folium.Popup("Deslizamiento Histórico", parse_html=True),
                    tooltip="Deslizamiento"
                ).add_to(m)
        
        # 2. Add faults (Fallas)
        if show_faults:
            faults_path = os.path.join(base_path, "FALLAS", "fallas_clip.shp")
            if os.path.exists(faults_path):
                faults = gpd.read_file(faults_path)
                folium.GeoJson(
                    faults,
                    style_function=lambda x: {
                        'color': 'purple',
                        'weight': 3,
                        'opacity': 0.8
                    },
                    popup=folium.Popup("Falla Geológica", parse_html=True),
                    tooltip="Falla Geológica"
                ).add_to(m)
                    
        # 3. Add area of study (AREA DE ESTUDIO)
        if show_area:
            area_path = os.path.join(base_path, "AREA DE ESTUDIO", "Polygons.shp")
            if os.path.exists(area_path):
                area = gpd.read_file(area_path)
                folium.GeoJson(
                    area,
                    style_function=lambda x: {
                        'fillColor': 'blue',
                        'color': 'darkblue',
                        'weight': 2,
                        'fillOpacity': 0.5
                    },
                    popup=folium.Popup("Área de Estudio", parse_html=True),
                    tooltip="Área de Estudio"
                ).add_to(m)

        # 4. Add points (Puntos)
        if show_points:
            points_path = os.path.join(base_path, "Puntos", "Export_Output_WGS84.shp")
            if os.path.exists(points_path):
                points = gpd.read_file(points_path)
                folium.GeoJson(
                    points,
                    style_function=lambda x: {
                        'color': 'orange',
                        'weight': 3,
                        'opacity': 0.8
                    },
                    popup=folium.Popup("Puntos Relevantes", parse_html=True),
                    tooltip="Puntos Relevantes"
                ).add_to(m)

    except Exception as e:
        st.error(f"Error al cargar shapefiles: {e}")

    return m
