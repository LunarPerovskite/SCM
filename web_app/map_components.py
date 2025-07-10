import geopandas as gpd
import os
import streamlit as st
import folium
from streamlit_folium import st_folium
import glob

def ensure_wgs84(gdf):
    """Ensure the GeoDataFrame is in WGS84 CRS."""
    if gdf.crs is not None and gdf.crs.to_string() != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    return gdf

def load_and_validate_shapefile(shapefile_path, layer_name):
    """Load and validate a shapefile, return None if fails."""
    try:
        print(f"Debug: Attempting to load {layer_name} from: {shapefile_path}")
        
        # Diagnostic information
        print(f"Debug: File path length: {len(shapefile_path)}")
        print(f"Debug: File path repr: {repr(shapefile_path)}")
        print(f"Debug: Directory exists: {os.path.exists(os.path.dirname(shapefile_path))}")
        print(f"Debug: Directory contents: {os.listdir(os.path.dirname(shapefile_path)) if os.path.exists(os.path.dirname(shapefile_path)) else 'DIR_NOT_FOUND'}")
        
        # Try different approaches to check file existence
        import pathlib
        path_obj = pathlib.Path(shapefile_path)
        print(f"Debug: Pathlib exists: {path_obj.exists()}")
        print(f"Debug: Pathlib is_file: {path_obj.is_file()}")
        
        # Try to access the file directly
        try:
            with open(shapefile_path, 'rb') as f:
                print(f"Debug: File can be opened directly (first 10 bytes): {f.read(10)}")
        except Exception as file_error:
            print(f"Debug: Cannot open file directly: {file_error}")
        
        # Check if main shapefile exists
        if not os.path.exists(shapefile_path):
            print(f"Debug: {layer_name} shapefile not found at: {shapefile_path}")
            return None
        
        # Check for associated files
        base_path = shapefile_path[:-4]  # Remove .shp extension
        required_files = ['.shp', '.shx', '.dbf']
        missing_files = []
        
        for ext in required_files:
            file_path = base_path + ext
            if not os.path.exists(file_path):
                missing_files.append(ext)
        
        if missing_files:
            print(f"Debug: {layer_name} missing required files: {missing_files}")
            return None
        
        # List all associated files
        all_files = glob.glob(base_path + ".*")
        print(f"Debug: {layer_name} associated files: {[os.path.basename(f) for f in all_files]}")
        
        # Try to read the shapefile
        print(f"Debug: Reading {layer_name} shapefile...")
        gdf = gpd.read_file(shapefile_path)
        
        if gdf.empty:
            print(f"Debug: {layer_name} shapefile is empty!")
            return None
        
        # Ensure WGS84
        gdf = ensure_wgs84(gdf)
        
        print(f"Debug: {layer_name} loaded successfully!")
        print(f"Debug: {layer_name} CRS: {gdf.crs}")
        print(f"Debug: {layer_name} shape: {gdf.shape}")
        print(f"Debug: {layer_name} bounds: {gdf.total_bounds}")
        print(f"Debug: {layer_name} geometry types: {gdf.geometry.geom_type.unique()}")
        print(f"Debug: {layer_name} column dtypes: {gdf.dtypes.to_dict()}")
        
        return gdf
        
    except Exception as e:
        print(f"Debug: Error loading {layer_name}: {e}")
        return None

def create_map(show_landslides=True, show_faults=True, show_area=True, show_points=True):
    """Create the main map with shapefiles using folium."""
    # Create the base map centered on Caldas
    m = folium.Map(location=[5.3, -75.4], zoom_start=8)

    try:
        print("Debug: Starting map creation...")
        print(f"Debug: Current working directory: {os.getcwd()}")
        
        # Define shapefile paths using absolute paths for reliability
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "shps"))
        print(f"Debug: Base shapefile directory: {base_dir}")
        
        shapefiles = {
            'landslides': {
                'path': os.path.join(base_dir, "Deslizamientos", "DESLIZAMIENTOS.shp"),
                'name': 'Deslizamientos',
                'color': 'red',
                'show': show_landslides
            },
            'faults': {
                'path': os.path.join(base_dir, "FALLAS", "fallas_clip.shp"),
                'name': 'Fallas',
                'color': 'purple',
                'show': show_faults
            },
            'area': {
                'path': os.path.join(base_dir, "AREA DE ESTUDIO", "Polygons.shp"),
                'name': 'Área de Estudio',
                'color': 'blue',
                'show': show_area
            },
            'points': {
                'path': os.path.join(base_dir, "Puntos", "Export_Output_WGS84.shp"),
                'name': 'Puntos',
                'color': 'orange',
                'show': show_points
            }
        }
        
        # Process each shapefile
        for key, config in shapefiles.items():
            if not config['show']:
                print(f"Debug: Skipping {config['name']} (disabled)")
                continue
            if key == 'points':
                print(f"Debug: Skipping {config['name']} (removed by user request)")
                continue
            print(f"\nDebug: Processing {config['name']}...")
            gdf = load_and_validate_shapefile(config['path'], config['name'])
            if gdf is None:
                print(f"Debug: Failed to load {config['name']}, skipping...")
                continue
            # Mostrar todos los deslizamientos sin filtros
            if key == 'landslides':
                print(f"Debug: Mostrando todos los deslizamientos sin filtros. Total: {len(gdf)} registros.")
            
            # Fix timestamp/datetime serialization issues
            gdf_clean = gdf.copy()
            for col in gdf_clean.columns:
                if gdf_clean[col].dtype == 'datetime64[ns]' or 'datetime' in str(gdf_clean[col].dtype).lower():
                    print(f"Debug: Converting datetime column '{col}' to string for {config['name']}")
                    gdf_clean[col] = gdf_clean[col].astype(str)
                elif gdf_clean[col].dtype == 'object':
                    # Check if any values are Timestamp objects
                    sample_vals = gdf_clean[col].dropna().head()
                    if len(sample_vals) > 0 and any(hasattr(val, 'strftime') for val in sample_vals):
                        print(f"Debug: Converting timestamp objects in column '{col}' to string for {config['name']}")
                        gdf_clean[col] = gdf_clean[col].astype(str)
            
            # Add to map based on geometry type
            print(f"Debug: Adding {config['name']} as red points...")
            try:
                if key == 'landslides' and gdf_clean.geometry.geom_type.isin(['Point', 'MultiPoint']).any():
                    for _, row in gdf_clean.iterrows():
                        folium.CircleMarker(
                            location=[row.geometry.y, row.geometry.x],
                            radius=5,
                            color=config['color'],
                            fill=True,
                            fill_color=config['color'],
                            fill_opacity=0.7
                        ).add_to(m)
                else:
                    folium.GeoJson(
                        gdf_clean.to_json(),
                        name=config['name'],
                        style_function=lambda x, color=config['color'], key=key: {
                            'fillColor': color if key != 'area' else '#00000000',
                            'color': color,
                            'weight': 2 if key != 'faults' else 3,
                            'fillOpacity': 0.3 if key == 'area' else 0.7,
                            'opacity': 0.8
                        }
                    ).add_to(m)
                print(f"Debug: Successfully added {config['name']} to map")
            except Exception as e:
                print(f"Debug: Error adding {config['name']} to map: {e}")
                # Additional debugging for serialization issues
                print(f"Debug: Column dtypes for {config['name']}: {gdf_clean.dtypes.to_dict()}")
                import traceback
                traceback.print_exc()

        # Add layer control
        folium.LayerControl().add_to(m)
        print("Debug: Map creation completed successfully!")

    except Exception as e:
        st.error(f"Error al cargar shapefiles: {e}")
        print(f"Debug: General error in map creation: {e}")
        import traceback
        traceback.print_exc()

    return m
