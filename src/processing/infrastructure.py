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
        file['source_id'] = ['ARG' + str(i) for i in range(len(file))]
        file['amenity']   = file.tipologia_sigla
        file['name']      = file.establecimiento_nombre
        file['lat']       = file.y
        file['lon']       = file.x

        # Keep variables of interest
        file = file[file.columns[-7::]]

        # Add to master table
        infrastructure.append(file)
        
        # Bolivia
        #--------------------------------------------------------
        file_ = [file for file in official if ("BOL" in file) and (".shp" in file)]
        id_n = 0
        
        for file in file_:
            path_ = f"{scldatalake}{path}/{file}"
            file  = gpd.read_file(path_)

            # Create variables
            file['isoalpha3'] = "BOL"
            file['source']    = "Ministry of Health"
            file['source_id'] = ['BOL' + str(i) for i in range(id_n, id_n + len(file))]
            file['amenity']   = file.CLASE.str.lower()
            file['name']      = file[['Name','MUNICIPIO','PROVINCIA']].apply(lambda x : '{}, {}, {}'.format(x[0], x[1], x[2]), axis = 1)
            file['lat']       = file.LATITUD
            file['lon']       = file.LONGITUD

            # Keep variables of interest
            file = file[file.columns[-7::]]

            # Add to master table
            infrastructure.append(file)
            id_n += len(file)
        
        # Brazil 
        #--------------------------------------------------------
        # Import data
        file  = [file for file in official if "BRA" in file][0]
        path_ = f"{scldatalake}{path}/{file}"
        file  = pd.read_csv(path_, sep = ";", encoding = "unicode_escape")
        
        # Filter amenities
        file = file[file.TP_UNIDADE.isin([1,2,4,5,7,15,20,21,36,61,62,69,70,71,72,73,83,85])]
        
        # Amenities name 
        UNID_NAME = {1 :"Posto de Saude",
                     2 :"Centro de Saude/Unidade Basica",
                     4 :"Policlinica",
                     5 :"Hospital Geral",
                     7 :"Hospital Especializado",
                     15:"Unidade Mista",
                     20:"Pronto Socorro General",
                     21:"Pronto Socorro Especializado",
                     36:"Clinica/Centro de Especialidade",
                     61:"Centro de Parto Normal - Isolado",
                     62:"Hospital/Dia - Isolado",
                     69:"Centro de Atencao Hemoterapica E Ou Hematologica",
                     70:"Centro de Atencao Psicossocial",
                     71:"Centro de Apoio a Saude da Familia",
                     72:"Unidade de Atencao a Saude Indigena",
                     73:"Pronto Atendimento",
                     83:"Polo de Prevencao de Doencas e Agravos e Promocao da Saude",
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
        
        # Chile
        #--------------------------------------------------------
        file  = [file for file in official if ("CHL" in file) and (".shp" in file)][0]
        path_ = f"{scldatalake}{path}/{file}"
        file  = gpd.read_file(path_)
        
        # Create variables
        file['isoalpha3'] = "CHL"
        file['source']    = "Ministry of Health"
        file['source_id'] = file.C_VIG
        file['amenity']   = file.TIPO
        file['name']      = file.NOMBRE
        file['lat']       = file.LATITUD
        file['lon']       = file.LONGITUD

        # Keep variables of interest
        file = file[file.columns[-7::]]

        # Add to master table
        infrastructure.append(file)
        
        # Colombia 
        #--------------------------------------------------------
        file  = [file for file in official if "COL" in file][0]
        path_ = f"{scldatalake}{path}/{file}"
        file  = pd.read_csv(path_, encoding = "unicode_escape")
        
        # Filter amenities
        file = file[~file["latitute"].isna()]
        
        # Create variables
        file['isoalpha3'] = "COL"
        file['source']    = "Ministry of Health REPS"
        file['source_id'] = file.codigohabilitacionsede
        file['amenity']   = "IPS"
        file['name']      = file.nombresede
        file['lat']       = file.latitute
        file['lon']       = file.longitude

        # Keep variables of interest
        file = file[file.columns[-7::]]

        # Add to master table
        infrastructure.append(file)
        
        # Dominican Republic
        #--------------------------------------------------------
        file  = [file for file in official if "DOM" in file][0]
        path_ = f"{scldatalake}{path}/{file}"
        file  = pd.read_csv(path_, sep = ";", encoding = "latin1")
        
         # Create variables
        file['isoalpha3'] = "DOM"
        file['source']    = "Ministry of Health"
        file['source_id'] = ['DOM' + str(i) for i in range(len(file))]
        file['amenity']   = file["TIPO DE CENTRO"]
        file['name']      = file[['NOMBRE DEL ESTABLECIMIENTO','MUNICIPIO','PROVINCIA']].apply(lambda x : '{}, {}, {}'.format(x[0], x[1], x[2]), axis = 1)
        file['lat']       = file.COORDENADAS.str.split(',', expand = True)[0]
        file['lon']       = file.COORDENADAS.str.split(',', expand = True)[1]

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
        file['source_id'] = ['GUY' + str(i) for i in range(len(file))]
        file['amenity']   = file["Facility Type"]
        file['name']      = file.Name
        file['lat']       = file[" latitude"]
        file['lon']       = file[" longitude"]

        # Keep variables of interest
        file = file[file.columns[-7::]]

        # Add to master table
        infrastructure.append(file)
        
        # Haiti
        #--------------------------------------------------------
        file  = [file for file in official if "HTI" in file][0]
        path_ = f"{scldatalake}{path}/{file}"
        file  = pd.read_csv(path_)
        
        # Create variables
        file['isoalpha3'] = "HTI"
        file['source']    = file.SourceHosp
        file['source_id'] = file.HealthC_ID
        file['amenity']   = file.Categorie
        file['name']      = file[['NomInstitu','Commune','DistrictNo']].apply(lambda x : '{}, {}, {}'.format(x[0], x[1], x[2]), axis = 1)
        file['lat']       = file.X_DDS
        file['lon']       = file.Y_DDS

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
        file['source_id'] = ['JAM' + str(i) for i in range(len(file))]
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
        id_n = 0
 
        for file in file_:
            path_ = f"{scldatalake}{path}/{file}"
            file  = pd.read_csv(path_)

            # Create variables
            file['isoalpha3'] = "SLV"
            file['source']    = "Ministry of Health"
            file['source_id'] = ['SLV' + str(i) for i in range(id_n, id_n + len(file))]
            file['amenity']   = file.ESPECIALIZACION.str.lower()
            file['name']      = file[['Name','MUNICIPIO','REGION']].apply(lambda x : '{}, {}, {}'.format(x[0], x[1], x[2]), axis = 1)
            file['lat']       = file.Y
            file['lon']       = file.X

            # Keep variables of interest
            file = file[file.columns[-7::]]

            # Add to master table
            infrastructure.append(file)
            id_n += len(file)
        
        # Trinidad and Tobago
        #--------------------------------------------------------
        file_ = [file for file in official if ("TTO" in file) and (".shp" in file)]
        id_n = 0
        
        for file in file_:
            type_ = file.split("/")[-1].split(".")[0]
            path_ = f"{scldatalake}{path}/{file}"
            file  = gpd.read_file(path_)

            # Create variables
            file['isoalpha3'] = "TTO"
            file['source']    = "Ministry of Health"
            file['source_id'] = ['TTO' + str(i) for i in range(id_n, id_n + len(file))]
            file['amenity']   = type_
            file['name']      = file.Name
            file['lat']       = file['geometry'].y
            file['lon']       = file['geometry'].x

            # Keep variables of interest
            file = file[file.columns[-7::]]

            # Add to master table
            infrastructure.append(file)
            id_n += len(file)
        
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
        
        # Add country code to soure_id
        infrastructure['source_id'] = infrastructure.apply(
            lambda row: str(row['isoalpha3']) + str(int(row['source_id'])) if re.match(r'^\d', str(row['source_id'])) else row['source_id'], 
            axis = 1)
    
    return infrastructure

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