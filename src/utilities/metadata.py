# Standard 
from datetime import datetime

# Data management and processing
import pandas as pd
import geopandas as gpd

# Geospatial 
import rasterio

def get_metadata(file_path):
    '''
    extract metadata from a geospatial file 
    prompt the user for missing information
    
    Parameters
    ----------
    file_path : str
        path to the geospatial file (shapefile, GeoJSON, raster, etc.)
    
    Returns
    -------
    metadata_df : pandas.DataFrame
        dataframe containing the metadata for the geospatial file
        this includes manual inputs from user
    '''
    
    # Placeholder for metadata
    metadata = {
        "Title"                : file_path.split('/')[-1].split('.')[0],  # Use the file name without extension
        "Summary"              : None,
        "Description"          : None,
        "Tags"                 : None,
        "Category"             : None,
        "Credits"              : None,
        "Date of creation"     : datetime.now().strftime("%Y-%m-%d"),
        "Date of last update"  : datetime.now().strftime("%Y-%m-%d"),
        "Responsible party"    : None,
        "Coordinate system"    : None,
        "Geographic extent"    : None,
        "Lineage"              : None,
        "Attribute information": None,
        "Feature types"        : None,
        "Resolution"           : None,
        "Update frequency"     : None,
        "Usage information"    : None,
        "Metadata date"        : datetime.now().strftime("%Y-%m-%d"),
        "Metadata contact"     : None
    }
    
    # Extract metadata based on file type
    if file_path.endswith(('.shp', '.geojson')):
        # Handle vector data
        gdf = gpd.read_file(file_path)
        metadata["Coordinate system"]     = gdf.crs.to_string() if gdf.crs else "Unknown"
        metadata["Geographic extent"]     = f"Lat: {gdf.total_bounds[1]} to {gdf.total_bounds[3]}, Lon: {gdf.total_bounds[0]} to {gdf.total_bounds[2]}"
        metadata["Attribute information"] = ", ".join([f"{col}: {dtype}" for col, dtype in gdf.dtypes.items()])
        metadata["Feature types"]         = ", ".join(gdf.geometry.type.unique())
        
    elif file_path.endswith(('.tif', '.tiff', '.asc', '.nc')):
        # Handle raster data
        with rasterio.open(file_path) as src:
            metadata["Coordinate system"]     = src.crs.to_string() if src.crs else "Unknown"
            metadata["Geographic extent"]     = f"Lat: {src.bounds.bottom} to {src.bounds.top}, Lon: {src.bounds.left} to {src.bounds.right}"
            metadata["Resolution"]            = f"{src.res[0]} x {src.res[1]}"
            metadata["Attribute information"] = f"Bands: {src.count}, Data Type: {src.dtypes[0]}"
    
    # Prompt user for missing metadata
    descriptions = {
        "Summary"          : "Enter a one-line summary of the data layer: ",
        "Description"      : "Enter an in-depth description of the data layer: ",
        "Tags"             : "Enter relevant keywords for search, separated by commas: ",
        "Category"         : "Enter the category of the data layer: ",
        "Credits"          : "Enter the credits for the data providers: ",
        "Responsible party": "Enter the contact information of the responsible party: ",
        "Lineage"          : "Enter the origin of the data: ",
        "Update frequency" : "Enter the update frequency of the layer: ",
        "Usage information": "Enter information about layer format, accessibility, and usage constraints: ",
        "Metadata contact" : "Enter the contact information of the person responsible for the metadata: "
    }
    
    for key, prompt in descriptions.items():
        if metadata[key] is None:
            metadata[key] = input(prompt)

    # Create a DataFrame
    metadata_df = pd.DataFrame(list(metadata.items()), columns=["Element", "Value"])

    return metadata_df