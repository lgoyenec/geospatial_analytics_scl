# Geospatial Analytics SCL

Welcome to the Geospatial Analytics SCL repository. This project focuses on preprocessing and analyzing geospatial data in Latin America and the Caribbean (LAC), providing tools and resources to facilitate data analysis and exploration.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Repository structure](#repository-structure)
- [Data sources](#data-sources)
- [Author](#author)
- [Citation](#citation)
- [Limitations](#limitations)
- [Contributing](#contributing)

## Introduction

This repository provides a set of tools and methodologies for geospatial data analysis in the context of social sector projects within the Inter-American Development Bank (IDB). The tools are designed to facilitate the analysis and visualization of spatial data to support decision-making in areas such as health, education, and social protection. The repository includes Python scripts, Jupyter notebooks, and links to various datasets in the SCL Data Lake that can be used to perform comprehensive geospatial analysis.

## Installation

To get started with Geospatial Analytics SCL, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/BID-DATA/geospatial_analytics_scl.git
    ```

2. Navigate to the repository directory:
    ```bash
    cd geospatial_analytics_scl
    ```

3. Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

4. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Repository structure

The repository is organized to facilitate both learning and practical application of geospatial data processing and analysis in the social sector. Below is an overview of the structure:

- **/docs/**: [MISSING]

- **/notebooks/**: A collection of Jupyter notebooks that provide step-by-step tutorials on how to create and process spatial datasets.
    - `0-population.ipynb`: Demonstrates processing population data.
    - `1-infrastructure.ipynb`: Covers processing social and health infrastructure data.
    - `2-isochrones.ipynb`: Explains isochrone estimation.
    - `3-coverage.ipynb`: Estimates accesibility based on isochrone estimation.
    - `4-connectivity.ipynb`: Covers processing connectivity data.

- **/exercises/**: Contains Jupyter notebooks designed as exercises to apply the modules developed in the **/src/** directory. These exercises build on the concepts and steps outlined in the **/notebooks/**, providing users with hands-on practice in using the code modules.

- **/src/**: The main directory containing all Python modules and scripts used for geospatial data processing, analysis, and utility functions.
    - **/geospatial/**: Modules related to geospatial operations and analysis, such as accessibility and isochrone calculations.
    - **/processing/**: Contains modules for processing various types of geospatial data, including connectivity, infrastructure, ecosystems, natural disasters, and population data.
    - **/statistics/**: Modules for statistical analysis of geospatial datasets, supporting the extraction of insights from the data.
    - **/utilities/**: Utility scripts that support the main modules, providing additional tools and functionalities.

- **metadata-sample.csv**: A sample metadata file that serves as an example or template for organizing metadata related to the datasets used in the repository.

- **requirements.txt**: Lists all the Python dependencies required to run the scripts and notebooks in the repository.

- **setup.py**: A script used for packaging the repository, making it easier to distribute and install the repository as a Python package.

## Data sources

The following datasets are included in or linked to this repository:

1. **High-Resolution Population Density Map**: Provides detailed population density maps and demographic estimates from [Meta](https://dataforgood.facebook.com/dfg/tools/high-resolution-population-density-maps-demographic-estimates)

2. **Administrative Boundaries**: Shapefiles at the administrative level 1 and 2 from [Humanitarian Data Exchange (HDX)](https://data.humdata.org/).

3. **Social Infrastructure**: Data on social infrastructure such as schools, hospitals, and other amenities, collected from [OpenStreetMap (OSM)](https://www.openstreetmap.org/).

4. **Health Infrastructure**: Data on health infrastructure including hospitals, clinics, and other health-related facilities from [healthsites.io](https://healthsites.io/).

5. **Official Social Infrastructure**: Data on social infrastructure provided by countries such as Argentina, Brazil, Ecuador, El Salvador, Guatemala, Guyana, Honduras, Jamaica, Mexico, and Peru. The structure of these datasets varies across countries. For further details, refer to the [IDB documentation](https://scldata.iadb.org/app/folder/874B76A4-5B3C-467C-A31F-A0D9FA9B1F01#tab-documentation).

6. **Connectivity Data**: Data on internet connectivity, including speed and coverage from [Ookla's Open Data Initiative](https://github.com/teamookla/ookla-open-data).

Note: Ensure you comply with the terms of use of these data sources when using them for your projects.

## Author 

This repository is maintained by **[Laura Goyeneche](https://github.com/lgoyenec)**, Social Data Consultant at the Inter-American Development Bank (IDB). 

## Citation 

> "Source: Inter-American Development Bank (year of consultation), Geospatial analysis in Latin America and the Caribbean". We suggest referencing the date on which the databases were consulted, as the information contained in them may change. Likewise, we appreciate a copy of the publications or reports that use the information contained in this database for our records.

> All rights concerning the public datasets used from Meta, HDX, OpenStreetMaps, and healthsites.io belong to their respective owners.

## Limitations of responsibilities 

The IDB is not responsible, under any circumstance, for damage or compensation, moral or patrimonial; direct or indirect; accessory or special; or by way of consequence, foreseen or unforeseen, that could arise: (i) under any concept of intellectual property, negligence, or detriment of another party theory; (ii) following the use of the digital tool, including, but not limited to defects in the Digital Tool, or the loss or inaccuracy of data of any kind. The foregoing includes expenses or damages associated with communication failures and/or malfunctions of computers linked to the use of the digital tool.

## Contributing 

We welcome contributions from the community! If you have suggestions for new features, improvements, or bug fixes, please feel free to submit a pull request. When contributing, please ensure that your code is well-documented and follows the project's coding standards.

### Guidelines for Contributing:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:
    ```bash
    git checkout -b feature-name
    ```
3. Make your changes and commit them with a descriptive message:
    ```bash
    git commit -m "Added new feature: feature description"
    ```
4. Push your branch to your forked repository:
    ```bash
    git push origin feature-name
    ```
5. Open a pull request against the main branch of this repository.
