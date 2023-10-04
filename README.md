# Geospatial analysis in Latin America and the Caribbean 

## Index: 
- [Description](#description)
- [Structure](#structure)
- [Data source](#data-source)
- [Author(s)](#authors)
- [Citation](#citation)

## Description 
This repository contains a comprehensive collection of code for preprocessing geospatial data in Latin America and the Caribbean (LAC). The repository aims to facilitate data analysis and exploration by providing code examples and modules (.py) for obtaining various datasets related to the region's population, administrative boundaries, social infrastructure, and more. This repository's **main objective** is to create a centralized and continuously updated resource for preprocessing and analyzing geospatial data in the region. By fostering collaboration and knowledge sharing, the repository aims to support research, analysts, and policymakers in conducting in-depth geospatial analysis and generating valuable insights for the region. 

This repository includes scripts and instructions for obtaining the following datasets: 

1. High-resolution population density map from [Meta](https://dataforgood.facebook.com/dfg/tools/high-resolution-population-density-maps)

2. Shapefiles at the administrative level 1 and 2 from Humanitarian Data Exchange [(HDX)](https://data.humdata.org/)

3. Social infrastructure, such as schools, hospitals, and other amenities is obtained from [OpenStreetMap](https://www.openstreetmap.org/).

4. Health infrastructure includes hospitals, clinics, and more from [healthsites.io](https://healthsites.io/). 

5. Official data on social infrastructure shared by the countries in the region. The structure of these datasets varies across countries. For more details on official data, visit SCL Data Lake, resource [Healthcare Facilities](https://scldata.iadb.org/app/folder/BF7AF50E-3BC0-479D-9B51-79A1F692F0F5).

6. Connectivty data from [Ookla's Open Data Initiative](https://github.com/teamookla/ookla-open-data)

## Structure
The repository offers a range of code examples and modules to assist users in conducting data analysis on the 26 countries in the region. These examples demonstrate retrieving and preprocessing each required dataset, ensuring a seamless workflow for researchers. This repository workflow is (so far) divided into 4 steps:

- [0-population.ipynb](https://github.com/BID-DATA/geospatial_analytics_scl/blob/main/source/0-population.ipynb): this notebook shows the step-by-step to query and adjust the population high-resolution maps from Meta and CIESIN published in the [HDX](https://data.humdata.org/) data for good portal.

- [1-infrastructure.ipynb](https://github.com/BID-DATA/geospatial_analytics_scl/blob/main/source/1-infrastructure.ipynb) this notebook shows the step-by-step to create a dataset with social infrastructure in the region from official and public records. 

- [2-isochrones.ipynb](https://github.com/BID-DATA/geospatial_analytics_scl/blob/main/source/2-isochrones.ipynb): this notebook shows the step-by-step to calculate isochrones using the [mapbox API](https://docs.mapbox.com/playground/isochrone/). Please read for the [API](https://docs.mapbox.com/playground/isochrone/) works before running the code. 

- [3-coverage.ipynb](https://github.com/BID-DATA/geospatial_analytics_scl/blob/main/source/3-coverage.ipynb): this notebook shows the step-by-step to calculate of the population (un)covered by social infrastructure in the region at the administrative level 2 and H3 (resolution 6), including coverage to ATM, banks, bureau of change, hospitals, and other.

- [4-connectivity.ipynb](https://github.com/BID-DATA/geospatial_analytics_scl/blob/main/source/4-connectivity.ipynb): this notebook shows the step-by-step to calculate the average download and upload connectivity speeds from Ookla's speedtest API based on [Ookla's Open Data Initiative](https://github.com/teamookla/ookla-open-data) GitHub repository. We used as reference the [tutorials](https://github.com/teamookla/ookla-open-data/blob/master/tutorials/aggregate_by_county_py.ipynb) to aggregate the data at the subnational levels. 

The previous notebooks show examples of how to conduct the analysis described. However, a series of modules (.py functions) are provided in [utils.py](https://github.com/BID-DATA/geospatial_analytics_scl/blob/main/source/utils.py) to facilitate analysis for all countries in the region. These modules can process the collected data and generate output files in GeoJSON format, maps, and other relevant visualizations. Users can leverage these modules to perform a variety of analyses, including spatial aggregation, statistical calculations, and mapping. [run.ipynb](https://github.com/BID-DATA/geospatial_analytics_scl/blob/main/source/run.ipynb) presents a step-by-step to use these modules. 

## Data source
> Population: [Development Data Partnership/Facebook - High resolution population density map](https://scldata.iadb.org/app/folder/A674F395-DAF5-4E98-B132-B6F7E07ADC64)

> Financial infrastructure: [Geospatial infrastructure/Financial Facilities](https://scldata.iadb.org/app/folder/C18ACCEE-04FC-4CA5-A034-4B9BA7FE2952)

> Healthcare infrastructure: [Geospatial infrastructure/Healthcare Facilities](https://scldata.iadb.org/app/folder/874B76A4-5B3C-467C-A31F-A0D9FA9B1F01)

> Isochrones: [Development Data Partnership/Mapbox](https://scldata.iadb.org/app/folder/9A16C68B-58F7-4260-B9E0-71AAC96AA523)

> Coverage: [Development Data Partnership/Mapbox](https://scldata.iadb.org/app/folder/0A0D8DD8-70B2-44AD-B75F-02E5B766C454)

## Author(s)
[Laura Goyeneche](https://github.com/lgoyenec), Social Data Consultant, Inter-American Development Bank

## Citation
> "Source: Inter-American Development Bank (year of consultation), Geospatial analysis in Latin America and the Caribbean". We suggest to reference the date on which the databases were consulted, as the information contained in them may change. Likewise, we appreciate a copy of the publications or reports that use the information contained in this database for our records.

> All rights concerning the public datasets used from Meta, HDX, OpenStreetMaps, Ookla, and healthsites.io belong to its owners.

## Limitation of responsibilities
The IDB is not responsible, under any circumstance, for damage or compensation, moral or patrimonial; direct or indirect; accessory or special; or by way of consequence, foreseen or unforeseen, that could arise: (i) under any concept of intellectual property, negligence or detriment of another part theory; (ii) following the use of the digital tool, including, but not limited to defects in the Digital Tool, or the loss or inaccuracy of data of any kind. The foregoing includes expenses or damages associated with communication failures and / or malfunctions of computers, linked to the use of the digital tool.
