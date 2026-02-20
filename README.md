# Geospatial Analytics SCL

Welcome to the Geospatial Analytics SCL repository. This project focuses on preprocessing and analyzing geospatial data in Latin America and the Caribbean (LAC), providing tools and resources to facilitate data analysis and exploration.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Repository structure](#repository-structure)
- [Author](#author)
- [Citation](#citation)
- [Limitations](#limitations)

## Introduction

This repository provides a set of tools and methodologies for geospatial data analysis in the context of social sector projects within the Inter-American Development Bank (IDB). The tools are designed to facilitate the analysis and visualization of spatial data to support decision-making in areas such as health, education, and social protection.

The codebase is organized into reusable core modules (in `src/`) and sector-specific workflows and examples (in `sector/`), making it easier to apply common geospatial processing steps across multiple projects and sectors.


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

- `sector/`  
  Sector-specific projects, workflows, and examples that build on the core geospatial modules. Each subfolder typically corresponds to a sector (e.g., health, education, social protection) or a specific analytical use case, and may include scripts and/or Jupyter notebooks illustrating end-to-end pipelines.

- `src/`  
  Main Python package containing reusable modules for geospatial data processing, analysis, and supporting utilities. These modules are intended to be imported and reused across different sector projects in `sector/`.

- `metadata-sample.csv`  
  A sample metadata file that serves as an example or template for organizing metadata related to the datasets used in the repository.

- `requirements.txt`  
  Lists all the Python dependencies required to run the scripts and notebooks in the repository.

- `setup.py`  
  Packaging script that makes it possible to install the repository as a Python package (e.g., `pip install -e .`), so that the modules in `src/` can be imported in a consistent way.

## Author 

This repository is maintained by **[Laura Goyeneche](https://github.com/lgoyenec)**, Social Data Consultant at the Inter-American Development Bank (IDB). 

## Citation 

> "Source: Inter-American Development Bank (year of consultation), Geospatial analysis in Latin America and the Caribbean". We suggest referencing the date on which the databases were consulted, as the information contained in them may change. Likewise, we appreciate a copy of the publications or reports that use the information contained in this database for our records.

> All rights concerning the public datasets used from Meta, HDX, OpenStreetMaps, and healthsites.io belong to their respective owners.

## Limitations of responsibilities 

The IDB is not responsible, under any circumstance, for damage or compensation, moral or patrimonial; direct or indirect; accessory or special; or by way of consequence, foreseen or unforeseen, that could arise: (i) under any concept of intellectual property, negligence, or detriment of another party theory; (ii) following the use of the digital tool, including, but not limited to defects in the Digital Tool, or the loss or inaccuracy of data of any kind. The foregoing includes expenses or damages associated with communication failures and/or malfunctions of computers linked to the use of the digital tool.

## Contributing 

We welcome contributions from the community! If you have suggestions for new features, improvements, or bug fixes, please feel free to submit a pull request. When contributing, please ensure that your code is well-documented and follows the project's coding standards.
