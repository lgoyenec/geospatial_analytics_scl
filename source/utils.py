"""
individual modules for geospatial analysis
includes multiple functions
TODO: 
    split based on topics and create classes when needed 
    update paths once AWS connection is fix

Author : Laura Goyeneche, Consultant SPH, lauragoy@iadb.org
Created: April 05, 2023 
"""

# Basics 
#-------------------------------------------------------------------------------#
# Libraries
import io
import os 
import re
import time
import fiona
import boto3
import dotenv
import requests
import numpy as np
import pandas as pd
import geopandas as gpd
from datetime import datetime
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from geopandas.tools import sjoin
from shapely.geometry import Polygon
from h3 import geo_to_h3, h3_to_geo_boundary

# Working environments
dotenv.load_dotenv("/home/ec2-user/SageMaker/.env")
sclbucket   = os.environ.get("sclbucket")
scldatalake = os.environ.get("scldatalake")

# Resources and buckets
s3        = boto3.client('s3')
s3_       = boto3.resource("s3")
s3_bucket = s3_.Bucket(sclbucket)

# IADB countries 
#-------------------------------------------------------------------------------#
def get_iadb():
    """
    process data to obtain the spanish and english country names for IADB countries
    TODO: dataset must be updated directly in the Data Lake to eliminate this step
    
    Parameters
    ----------
    None
    
    Returns
    ----------
    pandas.DataFrame
        dataframe with IADB country names (EN/SP) and isoalpha3 codes 
    """
    
    # Import country names
        # Define path and S3 object 
    file = "Manuals and Standards/IADB country and area codes for statistical use/IADB_country_codes_admin_0.xlsx"
    obj  = s3.get_object(Bucket = sclbucket, Key = file)
    
        # Load excel file from S3 into memory and create file-like object from the bytes read
    excel_data = obj['Body'].read()
    excel_file = io.BytesIO(excel_data)
    
        # Datafile
    data = pd.read_excel(excel_file, engine = 'openpyxl')
    
    #path = scldatalake + file
    #data = pd.read_excel(path, engine = 'openpyxl')

    # Select rows/columns of interest
    data = data[~data.iadb_region_code.isna()]
    data = data[['isoalpha3','country_name_es']]

    # Replace values
    data['country_name_en'] = data.country_name_es.str.normalize('NFKD')
    data.country_name_en    = data.country_name_en.str.encode('ascii', errors = 'ignore')
    data.country_name_en    = data.country_name_en.str.decode('utf-8')

    # Replace country names
    country_ = {"Belice"                              : "Belize",
                "Bolivia (Estado Plurinacional de)"   : "Bolivia",
                "Brasil"                              : "Brazil",
                "Venezuela (Republica Bolivariana de)": "Venezuela",
                "Republica Dominicana"                : "Dominican Republic",
                "Trinidad y Tabago"                   : "Trinidad and Tobago"}
    data.country_name_en = data.country_name_en.replace(country_)

    # Sort dataset
    data = data.sort_values(by = "isoalpha3")
    data = data.reset_index(drop = True)
    
    return data


# Administrative shapefiles
#-------------------------------------------------------------------------------#
def get_country_shp(code = "", level = 0):
    """
    gets the country's shapefile at the selected admin level 
    
    Parameters
    ----------
    code : str, optional
        country's isoalpha3 code
    level: int, optional 
        administrative level (default is 0)
    
    Returns
    ----------
    geopandas.GeoDataFrame
        geo pandas dataframe with geo data at determined admin level (default 0)
    """
    
    # Import data
    if code == "":
        file = f"Geospatial Basemaps/Cartographic Boundary Files/LAC-26/region/level-{level}/lac-level-{level}.shp"
    else:
        code = code.lower()
        file = f"Geospatial Basemaps/Cartographic Boundary Files/LAC-26/level-{level}/{code}-level-{level}.shp"
    
    # Import data
    path = scldatalake + file
    shp  = gpd.read_file(path) 
    
    # Adjust country codes 
    shp.ADM0_PCODE = shp.ADM0_PCODE.replace({'BZ':'BLZ','BO':'BOL','BR':'BRA','BB':'BRB',
                                             'CL':'CHL','CO':'COL','CR':'CRI','DO':'DOM',
                                             'EC':'ECU','GT':'GTM','GY':'GUY','HN':'HND',
                                             'HT':'HTI','MX':'MEX','NI':'NIC','PA':'PAN',
                                             'PE':'PER','PY':'PRY','SV':'SLV','SR':'SUR',
                                             'TT':'TTO','UY':'URY','VE':'VEN'})
    
    return shp

# Extract HTML code / information from HDX website
#-------------------------------------------------------------------------------#
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


# Get population data from META
#-------------------------------------------------------------------------------#
def get_population(data, code, group = "total_population"):
    """
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


# Get infrastructure from official records
#-------------------------------------------------------------------------------#
def get_amenity_official(amenity, official):
    """
    process official records by country
    each country's raw data is different, preprocessing is done individually
    
    Parameters
    ----------
    amenity : str
        string with amenity name, including:
            financial
            healthcare
    official : list
        list of countries with official data
    
    Returns
    ----------
    pandas.DataFrame
        dataframe amenity information per country and site, including:
            isoalpha3: country name
            source   : source name
            name     : amenity name
            lat      : latitude
            lon      : longitude
    """
    
    # Inputs
    path = f"Geospatial infrastructure/{amenity} Facilities"
    
    # Master table 
    infrastructure = []
    
    # Financial Facilities
    # No official records yet
    
    # Healthcare Facilities
    if amenity == "Healthcare":
        # Argentina
        #--------------------------------------------------------
        # Import data
        file  = [file for file in official if "ARG" in file][0]
        path_ = f"{scldatalake}{path}/{file}"
        file  = pd.read_csv(path_)
        
        # Filter amenities
        file = file[~file.tipologia_id.isin([53,80])]

        # Create variables
        file['isoalpha3'] = "ARG"
        file['source']    = "Ministry of Health"
        file['source_id'] = file.establecimiento_id
        file['amenity']   = file.tipologia_sigla
        file['name']      = file.establecimiento_nombre
        file['lat']       = file.y
        file['lon']       = file.x

        # Keep variables of interest
        file = file[file.columns[-7::]]

        # Add to master table
        infrastructure.append(file)
        
        # Brazil 
        #--------------------------------------------------------
        # Import data
        file  = [file for file in official if "BRA" in file][0]
        path_ = f"{scldatalake}{path}/{file}"
        file  = pd.read_csv(path_, sep = ";", encoding = "unicode_escape")
        
        # Filter amenities
        file = file[file.TP_UNIDADE.isin([1,2,4,5,7,15,21,36,61,62,67,69,70,76,80,81,82,85])]
        
        # Amenities name 
        UNID_NAME = {1 :"Posto de Saude",
                     2 :"Centro de Saude/Unidade Basica",
                     4 :"Policlinica",
                     5 :"Hospital Geral",
                     7 :"Hospital Especializado",
                     15:"Unidade Mista",
                     21:"Pronto Socorro Especializado",
                     36:"Clinica/Centro de Especialidade",
                     61:"Centro de Parto Normal - Isolado",
                     62:"Hospital/Dia - Isolado",
                     67:"Laboratorio Central de Saude Publica - Lacen",
                     69:"Centro de Atencao Hemoterapica E Ou Hematologica",
                     70:"Centro de Atencao Psicossocial",
                     76:"Central de Regulacao Medica Das Urgencias",
                     80:"Laboratorio de Saude Publica",
                     81:"Central de Regulacao Do Acesso",
                     82:"Central de Notificacao,Captacao E Distrib de Orgaos Estadual",
                     85:"Centro de Imunizacao"}
        
        # Replace codes with unit name
        file.TP_UNIDADE = file.TP_UNIDADE.replace(UNID_NAME)
        
        # Create variables
        file['isoalpha3'] = "BRA"
        file['source']    = "Ministry of Health"
        file['source_id'] = file.CO_CNES
        file['amenity']   = file.TP_UNIDADE
        file['name']      = file.NO_FANTASIA
        file['lat']       = file.NU_LATITUDE
        file['lon']       = file.NU_LONGITUDE

        # Keep variables of interest
        file = file[file.columns[-7::]]

        # Add to master table
        infrastructure.append(file)

        # Ecuador
        #--------------------------------------------------------
        # Import data
        file  = [file for file in official if "ECU" in file][0]
        path_ = f"{scldatalake}{path}/{file}"
        file  = pd.read_csv(path_)
        
        # Filter amenities
        file = file[file["nivel de atencion"].isin(["NIVEL 1","NIVEL 2","NIVEL 3"])]
        
        # Create variables
        file['isoalpha3'] = "ECU"
        file['source']    = "Ministry of Health"
        file['source_id'] = file.unicodigo
        file['amenity']   = file.tipologia
        file['name']      = file["nombre oficial"]
        file['lat']       = file.y
        file['lon']       = file.x

        # Keep variables of interest
        file = file[file.columns[-7::]]

        # Add to master table
        infrastructure.append(file)
        
        # Guatemala
        #--------------------------------------------------------
        # Import data 
        file  = [file for file in official if "GTM" in file][0]
        path_ = f"{scldatalake}{path}/{file}"
        file  = pd.read_csv(path_)
        
        # Filter amenities 
        tipo_serv = ["CENTRO CONVERGENCIA",
                     "PUESTO DE SALUD",
                     "CENTRO DE SALUD",
                     "HOSPITAL",
                     "CENTRO ATENCION PERMANEN*",
                     "UNIDAD TECNICA SALUD",
                     "CENTRO URGENCIAS MEDICAS",
                     "UNIDAD 24 HORAS"]
        file = file[file.tipo_serv.isin(tipo_serv)]
        
        # Create variables
        file['isoalpha3'] = "GTM"
        file['source']    = "Ministry of Health"
        file['source_id'] = file.gid
        file['amenity']   = file.tipo_serv
        file['name']      = file.servicio
        file['lat']       = file.lat
        file['lon']       = file.lon

        # Keep variables of interest
        file = file[file.columns[-7::]]

        # Add to master table
        infrastructure.append(file)
        
        # Guyana
        #--------------------------------------------------------
        # Import data
            # Define inputs
        file  = [file for file in official if "GUY" in file][0]
        path_ = f"{path}/{file}"
        obj   = s3.get_object(Bucket = sclbucket, Key = path_)

            # Read data
        excel_data = obj['Body'].read()
        excel_file = io.BytesIO(excel_data)
        file       = pd.read_excel(excel_file, engine = 'openpyxl')

        # Create variables
        file['isoalpha3'] = "GUY"
        file['source']    = "Ministry of Health"
        file['source_id'] = np.nan
        file['amenity']   = file["Facility Type"]
        file['name']      = file.Name
        file['lat']       = file[" latitude"]
        file['lon']       = file[" longitude"]

        # Keep variables of interest
        file = file[file.columns[-7::]]

        # Add to master table
        infrastructure.append(file)

        # Honduras
        #--------------------------------------------------------        
        # Import data 
        file       = [file for file in official if "HND" in file][0]
        path_      = f"{path}/{file}"
        obj        = s3.get_object(Bucket = sclbucket, Key = path_)
        excel_data = obj['Body'].read()
        excel_file = io.BytesIO(excel_data)
        file       = pd.read_excel(excel_file, engine = 'openpyxl', sheet_name = "coordenadas")
        
        # Create variables
        file['isoalpha3'] = "HND"
        file['source']    = "Ministry of Health"
        file['source_id'] = file.codigo
        file['amenity']   = np.nan
        file['name']      = file["Nombre US"]
        file['lat']       = file.lat
        file['lon']       = file.lon

        # Keep variables of interest
        file = file[file.columns[-7::]]

        # Add to master table
        infrastructure.append(file)
        
        # Jamaica 
        #--------------------------------------------------------
        # Import data
        file  = [file for file in official if "JAM" in file][0]
        path_ = f"{scldatalake}{path}/{file}"
        file  = pd.read_csv(path_)

        # Create variables
        file['isoalpha3'] = "JAM"
        file['source']    = "Ministry of Health"
        file['source_id'] = np.nan
        file['amenity']   = file.Type.str.lower()
        file['name']      = file[['H_Name','Parish']].apply(lambda x : '{} in {}'.format(x[0],x[1]), axis = 1)
        file['lat']       = file.GeoJSON.apply(lambda x: re.findall(r"\d+\.\d+", x)[1]).astype(float)
        file['lon']       = file.GeoJSON.apply(lambda x: re.findall(r"\d+\.\d+", x)[0]).astype(float) * -1

        # Keep variables of interest
        file = file[file.columns[-7::]]

        # Add to master table
        infrastructure.append(file)
        
        # Mexico 
        #--------------------------------------------------------
        # Import data
            # Define inputs
        file  = [file for file in official if "MEX" in file][0]
        path_ = f"{path}/{file}"
        obj   = s3.get_object(Bucket = sclbucket, Key = path_)

            # Read data
        excel_data = obj['Body'].read()
        excel_file = io.BytesIO(excel_data)
        file       = pd.read_excel(excel_file, engine = 'openpyxl')
        
        # Filter amenities 
        clave = ["CAF","99","W","F","OFI","ALM","BS","X","ANT","NES","UM","HM","OTR","UM TEMPORAL COVID","OTCE","BS","MR","NA","P","PERICIALES"]
        file  = file[~file["CLAVE DE TIPOLOGIA"].isin(clave)]

        # Create variables
        file['isoalpha3'] = "MEX"
        file['source']    = "Ministry of Health"
        file['source_id'] = file.ID
        file['amenity']   = file["NOMBRE TIPO ESTABLECIMIENTO"].str.replace("DE ","")
        file['name']      = file["NOMBRE DE LA UNIDAD"]
        file['lat']       = file["LATITUD"]
        file['lon']       = file["LONGITUD"]

        # Keep variables of interest
        file = file[file.columns[-7::]]

        # Add to master table
        infrastructure.append(file)
        
        # Peru 
        #--------------------------------------------------------
        # Import data
        file  = [file for file in official if "PER" in file][0]
        path_ = f"{scldatalake}{path}/{file}"
        file  = pd.read_csv(path_)

        # Dictionary with amenity names
        n_before  = ['I-1','I-2','I-3','I-4','II-1','II-2','II-E','III-1','III-2','III-E','SD'] 
        n_after   = ["Primary care"] * 4 + ["Secondary care"] * 3 + ["Tertiary care"] * 3 + [""]
        d_amenity = dict(zip(n_before,n_after))

        # Create variables
        file['isoalpha3'] = "PER"
        file['source']    = "Ministry of Health"
        file['source_id'] = file.codigo_renaes
        file['amenity']   = file.categoria.replace(d_amenity)
        file['name']      = file[['nombre','diresa']].apply(lambda x : '{} in {}'.format(x[0].title(),x[1].title()), axis = 1)
        file['lat']       = file.latitud
        file['lon']       = file.longitud

        # Keep variables of interest
        file = file[file.columns[-7::]]

        # Add to master table
        infrastructure.append(file)
        
        # El Salvador 
        #--------------------------------------------------------
        # Import data 
        file_ = [file for file in official if "SLV" in file]
        for file in file_:
            path_ = f"{scldatalake}{path}/{file}"
            file  = pd.read_csv(path_)

            # Create variables
            file['isoalpha3'] = "SLV"
            file['source']    = "Ministry of Health"
            file['source_id'] = np.nan
            file['amenity']   = file.ESPECIALIZACION.str.lower()
            file['name']      = file[['Name','MUNICIPIO','REGION']].apply(lambda x : '{}, {}, {}'.format(x[0], x[1], x[2]), axis = 1)
            file['lat']       = file.Y
            file['lon']       = file.X

            # Keep variables of interest
            file = file[file.columns[-7::]]

            # Add to master table
            infrastructure.append(file)
            
        # Master table 
        #--------------------------------------------------------
        # Generate master table 
        infrastructure = pd.concat(infrastructure)
        infrastructure = infrastructure.reset_index(drop = True)
        
        # Convert lat-lon to numeric
        infrastructure.lat = infrastructure.lat.apply(pd.to_numeric, errors = 'coerce', downcast = 'float')
        infrastructure.lon = infrastructure.lon.apply(pd.to_numeric, errors = 'coerce', downcast = 'float')
        
        # Remove NAs
        infrastructure = infrastructure[~infrastructure.lat.isna()] 
    
    return infrastructure


# Get infrastructure from official and public records
#-------------------------------------------------------------------------------#
def get_amenity(amenity, group):
    """
    gets the infrastructure data based on official and public records
    
    Parameters
    ----------
    amenity : str
        string with amenity name, including:
            financial
            healthcare
    group : str
        string wtth data group name, including:
            official
            public
    
    Returns
    ----------
    pandas.DataFrame
        dataframe amenity information per country and site, including:
            isoalpha3: country name
            source   : source name
            name     : amenity name
            lat      : latitude
            lon      : longitude
    """
    
    # Inputs
    data    = get_iadb()
    amenity = amenity.title()
    
    # Get files by bucket
    path  = f"Geospatial infrastructure/{amenity} Facilities"
    files = [file.key.split(path + "/")[1] for file in s3_bucket.objects.filter(Prefix = path).all()]
    
    # Identify records by categories
    official = [file for file in files if "official" in file]
    public   = [file for file in files if "healthsites" in file or "OSM" in file]
    
    # Create master table 
    infrastructure = []
    name           = []
    
    # Select group of interest 
    if group == "official":
        # Process official records 
        if len(official) > 0:
            infrastructure = get_amenity_official(amenity, official)
        else:
            print(f"No official records for {amenity} infrastructure")
            
    elif group == "public":    
        # Process public records
        # Records different from OSM
        file = [file for file in public if "OSM" not in file]
        if len(file) > 0:
            # Import data
            file  = file[0]
            path_ = f"{scldatalake}{path}/{file}"
            file  = pd.read_csv(path_)

            # Keep rows of interest
            file = file[~file.isoalpha3.isin(name)]
            file = file[~file.isoalpha3.isna()]

            # Keep variables of interest
            file = file.drop(columns = "geometry")

            # Add to master tables
            infrastructure.append(file)

            # Identify healthsites country names
            name =  pd.concat(infrastructure).isoalpha3.unique().tolist()
        
        # OSM records
        # Import data
        file_  = [file for file in public if "OSM" in file]
        for file in file_:
            path_ = f"{scldatalake}{path}/{file}"
            file  = pd.read_csv(path_, low_memory = False)

            # Keep IADB countries
            file = file[file.isoalpha3.isin(data.isoalpha3.unique())]

            # Keeps countries without healthsites.io records
            file = file[~file.isoalpha3.isin(name)]

            # Create variables
            file['source']    = "OSM"
            file['source_id'] = file.id

            # Keep variables of interest
            file = file[['isoalpha3','source','source_id','amenity','name','lat','lon']]

            # Add to master table
            infrastructure.append(file)

        # Generate master table 
        infrastructure = pd.concat(infrastructure)
        infrastructure = infrastructure.reset_index(drop = True)
    
    return infrastructure

# Get isochrone
#-------------------------------------------------------------------------------#
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


# Get multipolygon with isochrones by country
#-------------------------------------------------------------------------------#
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


# Get coverage by ADMIN-2 level and H3 cell
#-------------------------------------------------------------------------------#
def get_coverage(code, amenity, profile, minute, group, popgroup = "total_population"):
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


# Connectivity
# Code by Maria Reyes based on Ookla's Github repository tutorials
# Source: https://github.com/teamookla/ookla-open-data/blob/master/tutorials
#-------------------------------------------------------------------------------#

def quarter_start(year: int, q: int) -> datetime:
    """
    calculates the datetime representing the start of a quarter

    Parameters
    ----------
    year : int
        year
    q : int
        quarter

    Returns
    ----------
    datetime
        datetime object representing the start of a quarter
    """
    
    if not 1 <= q <= 4:
        raise ValueError("Quarter must be within [1, 2, 3, 4]")

    month = [1, 4, 7, 10]
    return datetime(year, month[q - 1], 1)


def get_tile_url(service: str, year: int, q: int) -> str:
    """
    returns the URL of a tile

    Parameters
    ----------
    service_type : ste
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

def calculate_stats(data, group_fields):
    """
    calculates weighted average of the download and upload speeds and total tests

    Parameters
    ----------
    data : GeoDataFrame) 
        geo pandas dataframe to analyze
    group_fields : list
        list of fields to group by

    Returns
    ----------
    geopandas.GeoDataFrame
        GeoDataFrame with the calculated stats
    """
    
    return (
        data.groupby(group_fields)
        .apply(
            lambda x: pd.Series(
                {"avg_d_mbps_wt": np.average(x["avg_d_mbps"], weights=x["tests"]),
                "avg_u_mbps_wt": np.average(x["avg_u_mbps"], weights=x["tests"])
                }
            )
        )
        .reset_index()
        .merge(
            data.groupby(group_fields)
            .agg(tests=("tests", "sum"))
            .reset_index(),
            on=group_fields,
        )
    )
