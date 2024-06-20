def get_access(code, amenity, profile, minute, group, popgroup = "total_population"):
    # TODO: Generalize function
    """
    calculates the coverage percentage per country by admin-2 level and H3 cell (resolution 3)
    
    Parameters
    ----------
    code : str
        country isoalpha3 code
    amenity : str
        string with amenity name, including:
            financial
            healthcare
    profile : str
        routing profile, including:
            walking
            cycling
            driving
     minute : int 
        distance in minutes from facility 
    popgroup: str
        population group (default is `total_population`), including:
            total_population
            women
            men
            children_under_five
            youth_15_24
            elderly_60_plus
            women_of_reproductive_age_15_49
    group : str
        string wtth data group name, including:
            official
            public
    
    Returns
    ----------
    geopandas.GeoDataFrame
        geo pandas dataframe with coverage at admin-2 and H3
    """
    
    # Inputs 
    #--------------------------------------------------------
        # Shapefile
    if code in ["BHS","BRB","BLZ","JAM","TTO"]:
        adm2_shp = get_country_shp(code, level = 1)
        adm2_shp["ADM2_PCODE"] = adm2_shp.ADM1_PCODE
    else: 
        adm2_shp = get_country_shp(code, level = 2)
    
        # Population and isochrones
    with fiona.Env(OGR_GEOJSON_MAX_OBJ_SIZE = 2000):  
        isochrone  = gpd.read_file(f"../data/1-isochrones/{amenity}/{group}/{minute}-min/{code}-{profile}-{minute}.geojson")
    population = pd.read_csv(f"../data/0-raw/population/{popgroup}/{code}_{popgroup}.csv.gz")
    geometry   = gpd.points_from_xy(population['longitude'], population['latitude'])
    population = gpd.GeoDataFrame(population.copy(), geometry = geometry, crs = 4326)
    
    # Population in isochrone 
    pop_iso = gpd.clip(population, isochrone)
    
    # Coverage at admin-2 level 
    #--------------------------------------------------------
        # Population in admin-2 level 
    pop_adm2 = gpd.sjoin(population, adm2_shp)
    pop_adm2 = pop_adm2[["ADM2_PCODE","population"]].groupby("ADM2_PCODE").sum().reset_index()
    pop_adm2 = pop_adm2.rename(columns = {"population":"pop_tot"})
    
        # Covered population in admin-2 level
    pop_adm2_cov = gpd.sjoin(pop_iso, adm2_shp)
    pop_adm2_cov = pop_adm2_cov[["ADM2_PCODE","population"]].groupby("ADM2_PCODE").sum().reset_index()
    pop_adm2_cov = pop_adm2_cov.rename(columns = {"population":"pop_cov"})
    
        # Coverage map 
    adm2_coverage = adm2_shp.copy()
    adm2_coverage = adm2_coverage.merge(pop_adm2    , on = "ADM2_PCODE", how = "left")
    adm2_coverage = adm2_coverage.merge(pop_adm2_cov, on = "ADM2_PCODE", how = "left")
    
        # Create coverage features
    adm2_coverage["pop_cov"]   = adm2_coverage.pop_cov.fillna(0)
    adm2_coverage["pop_uncov"] = adm2_coverage.pop_tot   - adm2_coverage.pop_cov
    adm2_coverage["per_cov"]   = adm2_coverage.pop_cov   * 100 / adm2_coverage.pop_tot
    adm2_coverage["per_uncov"] = adm2_coverage.pop_uncov * 100 / adm2_coverage.pop_tot
    
    # Coverage at H3 cell
    # Source: resolution table 
    # https://h3geo.org/docs/core-library/restable/
    #--------------------------------------------------------
        # Calculate H3 cells per population points
    population["hex_id"] = population.apply(lambda x: geo_to_h3(x["latitude"], x["longitude"], resolution = 6), axis = 1)
    
        # Collapse by H3
    h3_population             = population.groupby("hex_id").population.agg(sum).reset_index()
    h3_population["geometry"] = h3_population['hex_id'].apply(lambda x: h3_to_geo_boundary(x, geo_json = True))
    h3_population['hex_poly'] = h3_population['geometry'].apply(lambda x: Polygon(x))
    h3_population             = gpd.GeoDataFrame(h3_population, geometry = h3_population.hex_poly, crs = "EPSG:4326")
    
        # Covered population in H3 cells
    h3_pop_cov = gpd.sjoin(pop_iso, h3_population.drop(columns = "population"))
    h3_pop_cov = h3_pop_cov[["hex_id","population"]]
    h3_pop_cov = h3_pop_cov.rename(columns = {"population":"pop_cov"})
    h3_pop_cov = h3_pop_cov.groupby("hex_id").sum().reset_index()
    
        # H3 coverage map 
    h3_coverage = h3_population.merge(h3_pop_cov, on = "hex_id", how = "left")
    h3_coverage = h3_coverage.rename(columns = {"population":"pop_tot"})
    h3_coverage = h3_coverage.drop(columns = "geometry")
    h3_coverage = h3_coverage.rename(columns = {"hex_poly":"geometry"})
    
        # Create coverage features
    h3_coverage["pop_cov"]   = h3_coverage.pop_cov.fillna(0)
    h3_coverage["pop_uncov"] = h3_coverage.pop_tot   - h3_coverage.pop_cov
    h3_coverage["per_cov"]   = h3_coverage.pop_cov   * 100 / h3_coverage.pop_tot
    h3_coverage["per_uncov"] = h3_coverage.pop_uncov * 100 / h3_coverage.pop_tot
    
        # Set `geometry` as geometry in h3 level
    h3_coverage = h3_coverage.set_geometry(col = 'geometry')
    
    return adm2_coverage, h3_coverage  
