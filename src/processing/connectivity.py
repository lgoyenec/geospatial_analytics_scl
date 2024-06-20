def get_tile_url(service: str, year: int, q: int) -> str:
    """
    returns the URL of a tile

    Parameters
    ----------
    service_type : str
        type of the service - fixed or mobile
    year : int
        year
    q : int
        quarter

    Returns
    ----------
    str
        URL of a tile
    """
   
    dt = quarter_start(year, q)

    base_url = "https://ookla-open-data.s3-us-west-2.amazonaws.com/shapefiles/performance"
    url      = f"{base_url}/type%3D{service}/year%3D{dt:%Y}/quarter%3D{q}/{dt:%Y-%m-%d}_performance_{service}_tiles.zip"
    
    return url 