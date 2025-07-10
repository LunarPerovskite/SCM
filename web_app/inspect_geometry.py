import geopandas as gpd

def inspect_geometry(shapefile_path):
    """Inspect the geometry of a shapefile."""
    try:
        # Read the shapefile
        gdf = gpd.read_file(shapefile_path)

        # Print the bounds and first few geometries
        print("Bounds:", gdf.total_bounds)
        print("Sample Geometries:", gdf.geometry.head())
    except Exception as e:
        print(f"Error inspecting shapefile geometry: {e}")

if __name__ == "__main__":
    shapefile_path = "c:\\Users\\juane\\OneDrive\\Desktop\\hackaton_cafetera\\web_app\\data\\shps\\Puntos\\Export_Output_WGS84.shp"
    inspect_geometry(shapefile_path)
