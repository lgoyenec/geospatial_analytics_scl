def get_isochrone(lon, lat, minute, profile, generalize = 500):
    """
    calculates the individual isochrones based on lat-lon
    for more detail on the API options, refer to the following link:
        https://docs.mapbox.com/playground/isochrone/
    
    Parameters
    ----------
    lat,lon : float
        latitude, longitude
    minute : int 
        distance in minutes from facility 
    profile : str
        routing profile, including:
            walking
            cycling
            driving
    generalize : int, optional
        tolerance for Douglas-Peucker generalization in meters (default is 500)
        
    Returns
    ----------
    geopandas.GeoDataFrame
        geo pandas dataframe with isochrone for each latitude and longitude points
    """
    
    # Define url 
    token = os.environ.get("access_token_dp")
    url   = "https://api.mapbox.com/isochrone/v1/mapbox/"
    url   = f'{url}{profile}/{lon},{lat}?contours_minutes={minute}&generalize={generalize}&polygons=true&access_token={token}'
    
    # Request isochrones
    response = requests.get(url).json()
    
    # Create GeoDataframe and append results 
    try: 
        features  = response['features']
        isochrone = gpd.GeoDataFrame.from_features(features)
    except:
        isochrone = gpd.GeoDataFrame()
    
    return isochrone

def get_isochrones_country(code, amenity, minute, profile, group):
    """
    calculates the isochrones per country based on mapbox API
    for more detail on the API options, refer to the following link:
        https://docs.mapbox.com/playground/isochrone/
    
    Parameters
    ----------
    code : str
        country isoalpha3 code
    amenity : str
        string with amenity name, including:
            financial
            healthcare
    minute : int 
        distance in minutes from facility 
    profile : str
        routing profile, including:
            walking
            cycling
            driving
    group : str
        string wtth data group name, including:
            official
            public
            
    Returns
    ----------
    geopandas.GeoDataFrame
        geo pandas dataframe with multipolygon with covered area 
    """
    
    # Infrastructure data
    # TODO: path must be updated with Data Lake path
    path = f"../data/0-raw/infrastructure/{amenity}_facilities_{group}.csv"
    data = pd.read_csv(path, low_memory = False)
    data = data[data.isoalpha3 == code]
    data = data[~data.lat.isna()]
    
    # Get list of isochrones 
    isochrones = []
    for x,y,name in zip(data.lon, data.lat, data.amenity):
        # Calculate isochrone 
        shp_            = get_isochrone(x, y, minute, profile)
        shp_['amenity'] = name
        isochrones.append(shp_)
            
    # Master table 
    isochrones = pd.concat(isochrones)
    
    return isochrones