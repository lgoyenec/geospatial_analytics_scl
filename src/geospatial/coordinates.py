def get_coordinates(address, code):
    """
    gets the coordinates for address
    
    Parameters
    ----------
    address : str
        address, including, if possible, admin1, admin2 and country name
    
    Returns
    ----------
    list
        list of possible coordinates [longitude,latitude]
    """    
    # Inputs
    token   = os.environ.get("access_token_dp")
    country = get_iadb()
    country = country[country.isoalpha3 == code].country_name_es.tolist()[0]
    address = address if country in address else f"{address} {country}"
    address = urllib.parse.quote(address.encode('utf-8')) 
    url     = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json?access_token={token}'
    
    # Request
    try: 
        response = requests.get(url).json()
        response = response['features']
        response = [j for j in response if country in j["place_name"]]
    except: 
        response = []
        
    return response

def get_coordinates(address, country):
   
    # Inputs
    token   = os.environ.get("access_token_dp")
    address = urllib.parse.quote(address.encode('utf-8')) 
    url     = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json?access_token={token}'
    
    # Request
    try: 
        response = requests.get(url).json()
        response = response['features']
        response = [j for j in response if country in j["place_name"]]
    except: 
        response = []
        
    return response
