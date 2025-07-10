import geopandas as gpd
from pyproj import CRS

def reproject_shapefile(input_path, output_path, target_crs):
    """Reproject a shapefile to the target CRS."""
    try:
        # Read the shapefile
        gdf = gpd.read_file(input_path)

        # Reproject to the target CRS
        gdf = gdf.to_crs(target_crs)

        # Save the reprojected shapefile
        gdf.to_file(output_path)
        print(f"Shapefile reprojected and saved to {output_path}")
    except Exception as e:
        print(f"Error reprojecting shapefile: {e}")

if __name__ == "__main__":
    input_path = "c:\\Users\\juane\\OneDrive\\Desktop\\hackaton_cafetera\\web_app\\data\\shps\\Puntos\\Export_Output.shp"
    output_path = "c:\\Users\\juane\\OneDrive\\Desktop\\hackaton_cafetera\\web_app\\data\\shps\\Puntos\\Export_Output_WGS84.shp"
    target_crs = CRS.from_epsg(4326)  # WGS84

    reproject_shapefile(input_path, output_path, target_crs)
