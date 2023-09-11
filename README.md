# Geospatial analysis in Latin America and the Caribbean 

## Index: 
- [Description](#description)
- [Structure](#structure)
- [Author(s)](#authors)

## Description 
This repository contains a comprehensive collection of code for preprocessing geospatial data in Latin America and the Caribbean (LAC). The repository aims to facilitate data analysis and exploration by providing code examples and modules (.py) for obtaining various datasets related to the region's population, administrative boundaries, social infrastructure, and more. This repository's **main objective** is to create a centralized and continuously updated resource for preprocessing and analyzing geospatial data in the region. By fostering collaboration and knowledge sharing, the repository aims to support research, analysts, and policymakers in conducting in-depth geospatial analysis and generating valuable insights for the region. 

This repository includes scripts and instructions for obtaining the following datasets: 

1. High-resolution population density map from [Meta](https://dataforgood.facebook.com/dfg/tools/high-resolution-population-density-maps)

2. Shapefiles at the administrative level 1 and 2 from Humanitarian Data Exchange [(HDX)](https://data.humdata.org/)

3. Social infrastructure, such as schools, hospitals, and other amenities is obtained from [OpenStreetMap](https://www.openstreetmap.org/).

4. Health infrastructure includes hospitals, clinics, and more from [healthsites.io](https://healthsites.io/). 

5. Official data on social infrastructure shared by the countries in the region. The structure of these datasets varies across countries. 

## Structure
The repository offers a range of code examples and modules to assist users in conducting data analysis on the 26 countries in the region. These examples demonstrate retrieving and preprocessing each required dataset, ensuring a seamless workflow for researchers. This repository workflow is (so far) divided into 4 steps:

- [0-population.ipynb](https://github.com/BID-DATA/geospatial_analytics_scl/blob/main/source/0-population.ipynb): this notebook shows the step-by-step to query and adjust the population high-resolution maps from Meta and CIESIN published in the [HDX](https://data.humdata.org/) data for good portal.

- [1-infrastructure.ipynb](https://github.com/BID-DATA/geospatial_analytics_scl/blob/main/source/1-infrastructure.ipynb) this notebook shows the step-by-step to create a dataset with social infrastructure in the region from official and public records. 

- [2-isochrones.ipynb](https://github.com/BID-DATA/geospatial_analytics_scl/blob/main/source/2-isochrones.ipynb): this notebook shows the step-by-step to calculate isochrones using the [mapbox API](https://docs.mapbox.com/playground/isochrone/). Please read for the [API](https://docs.mapbox.com/playground/isochrone/) works before running the code. 

- [3-coverage.ipynb](https://github.com/BID-DATA/geospatial_analytics_scl/blob/main/source/3-coverage.ipynb): this notebook shows the step-by-step to calculate of the population (un)covered by social infrastructure in the region at the administrative level 2 and H3 (resolution 6), including coverage to ATM, banks, bureau of change, hospitals, and other. 

The previous notebooks show examples of how to conduct the analysis described. However, a series of modules (.py functions) are provided in [utils.py](https://github.com/BID-DATA/geospatial_analytics_scl/blob/main/source/utils.py) to facilitate analysis for all countries in the region. These modules can process the collected data and generate output files in GeoJSON format, maps, and other relevant visualizations. Users can leverage these modules to perform a variety of analyses, including spatial aggregation, statistical calculations, and mapping. [run.ipynb](https://github.com/BID-DATA/geospatial_analytics_scl/blob/main/source/run.ipynb) presents a step-by-step to use these modules. 


## Author(s)
[Laura Goyeneche](https://github.com/lgoyenec), Social Data Consultant, Inter-American Development Bank

> Citation: Inter-American Development Bank (year of consultation), Geospatial analysis in Latin America and the Caribbean

> All rights concerning the public datasets used from Meta, HDX, OpenStreetMaps and healthsites.io belong to its owners. 