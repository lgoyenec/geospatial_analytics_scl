"""
Import libraries
    Standard
    Thrid-party 
    Local modules
        Initialize the `src` package
"""

# Standard 
import io
import os
import re
import time
from datetime import datetime
import urllib

# AWS and environment
import boto3
import dotenv

# Data management and processing
import numpy as np
import pandas as pd
import geopandas as gpd
from sodapy import Socrata

# Web scraping and requests
import requests
from bs4 import BeautifulSoup

# Geospatial 
import fiona
from geopandas.tools import sjoin
from shapely.geometry import Polygon
from h3 import geo_to_h3, h3_to_geo_boundary

# Visualization
import matplotlib.pyplot as plt

# Local Application/Library Imports
from .processing import get_meta_url, get_population, get_amenity_official, get_amenity, get_tile_url
from .geospatial import get_coordinates, get_isochrone, get_isochrones_country, get_access
from .utilities  import get_iadb, get_country_shp, quarter_start
from .statistics import calculate_stats

# Working environments
dotenv.load_dotenv()
sclbucket   = os.environ.get("sclbucket")
scldatalake = os.environ.get("scldatalake")

# Resources and buckets
s3  = boto3.client('s3')
s3_ = boto3.resource("s3")
s3_bucket = s3_.Bucket(sclbucket)

# Define funcionts accessible via 'from src import *'
__all__ = [
    'get_iadb',
    'get_country_shp',
    'get_meta_url',
    'get_population',
    'get_coordinates',
    'get_isochrone',
    'get_isochrones_country',
    'get_tile_url',
    'get_amenity_official',
    'get_amenity',
    'get_access',
    'quarter_start',
    'calculate_stats'
]
