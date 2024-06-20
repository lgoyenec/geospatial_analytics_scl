def get_meta_url(data, code):
    """
    gets the HTML content from the high density population datasets in HDX
    https://data.humdata.org/organization/facebook?q=high%20resolution%20population%20density
    
    Parameters
    ----------
    data : pandas.DataFrame
        dataframe with IADB country names (EN/SP) and isoalpha3 codes
    code : str
        country's isoalpha3 code
    
    Returns
    ----------
    dict
        dictionary with file name and URL to download data by groups
        groups includes:
            total_population
            women
            men
            children_under_five
            youth_15_24
            elderly_60_plus
            women_of_reproductive_age_15_49
    """
    
    # Get latest population density maps name files 
    # Request HTML content
    geo      = data[data.isoalpha3 == code].country_name_en.values[0].lower().replace(" ","-")
    url      = f"https://data.humdata.org/dataset/{geo}-high-resolution-population-density-maps-demographic-estimates"
    response = requests.get(url)
    
    # Omit countries without population daya
    if response.status_code == 200:
    
        # Format HTML code
        html = response.content
        soup = BeautifulSoup(html, "html5lib")

        # Find file names
        soup = soup.find_all('ul', attrs = {"class":"hdx-bs3 resource-list"})
        soup = soup[0].find_all('li', attrs = {"class":"resource-item"})
        url  = [item.find_all('div', attrs = {"class":"hdx-btn-group hdx-btn-group-fixed"})[0].find('a')['href'] for item in soup]

        # Processing URL
        url = [item for item in url if "csv" in item]
        url = [f"https://data.humdata.org{item}" for item in url]

        # Processing file names
        files = []
        for item in url: 
            item_ = item.split("/")[-1]
            item_ = item_.replace("_csv",".csv")
            item_ = item_.replace(".zip",".gz")
            item_ = re.sub("(_|-)\d+", "", item_)
            item_ = item_.replace("population","total_population")
            item_ = item_.replace("general","total_population")
            item_ = f"{code}_{item_}"
            item_ = item_.replace(f"{code.lower()}_","")
            item_ = item_.replace(f"_{code.lower()}","")
            item_ = item_.replace("elderly_plus","elderly_60_plus")
            item_ = item_.replace("youth","youth_15_24")
            item_ = item_.replace("women_of_reproductive_age","women_of_reproductive_age_15_49")

            files.append(item_)

        # Create dictionary 
        keys_ = [x.replace(f"{code.upper()}_","").replace(".csv.gz","") for x in files]
        vals_ = [[x,y] for x,y in zip(files,url)]
        dict_ = dict(zip(keys_,vals_))
        
    else: 
        dict_ = dict(zip([],[]))
    
    return dict_

def get_population(data, code, group = "total_population"):
    """
    META population estimations
    gets the high density population datasets in HDX
    https://data.humdata.org/organization/facebook?q=high%20resolution%20population%20density
    
    Parameters
    ----------
    data : pandas.DataFrame
        dataframe with IADB country names (EN/SP) and isoalpha3 codes
    code : str
        country's isoalpha3 code
    group: str
        population group (default is `total_population`), including:
            total_population
            women
            men
            children_under_five
            youth_15_24
            elderly_60_plus
            women_of_reproductive_age_15_49
    
    Returns
    ----------
    pandas.DataFrame
        dataframe with adjusted population by admin-0 shapefile (country's admin border)
    """
    # Import data
    data = get_iadb()
    meta = get_meta_url(data, code)
    
    # Group of interest 
    groups = [name for name in meta.keys() if group in name]
    
    # Individuals shapefiles 
    files_ = []
    for group_ in groups:
        # Select group of interest
        item = meta[group_]
        name = item[0]
        path = item[1]
        pop  = pd.read_csv(path)

        # Keep variables of interest
        # Keep most recent population estimation 
        temp = [name for name in pop.columns if "latit" not in name and "long" not in name]
        if len(temp) > 1: 
            if temp[len(temp)-1] > temp[len(temp)-2]:
                var_ = temp[len(temp)-1]
            else: 
                var_ = temp[len(temp)-2]
        else: 
            var_ = temp[0]

        # Select variables of interest
        vars_ = ["latitude","longitude",var_]
        pop   = pop[vars_]
        pop   = pop.rename(columns = {var_:"population"})

        # Rename variables
        pop.columns = [re.sub("_\d+", "", name) for name in pop.columns]

        # Convert population .csv to .gpd
        geometry = gpd.points_from_xy(pop['longitude'], pop['latitude'])
        pop_geo  = gpd.GeoDataFrame(pop.copy(), geometry = geometry, crs = 4326)

        # Keep points inside country/region of interets
        # get_country_shp() default admin-level-0
        shp_        = get_country_shp(code)
        pop_geo_adj = gpd.clip(pop_geo, shp_)
        
        # Append to list of shapefiles
        files_.append(pop_geo_adj)
    
    # Create master data
    pop_geo_adj_ = gpd.pd.concat(files_).pipe(gpd.GeoDataFrame)
    
    # Export to Data Lake as .csv.gz 
    file = pop_geo_adj_.copy()
    file = file.drop(columns = "geometry")
    path = "Development Data Partnership/Facebook - High resolution population density map/public-fb-data/csv"
    path = scldatalake + f"{path}/{code.upper()}/{name}"
    file.to_csv(path, compression = 'gzip')
    
    return file