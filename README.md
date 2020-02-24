# NATO TIDE 2020 Hackathon Dash App Predicting Crisis
## Purpose

This Dash based Web App was our Deliverable for the NATO TIDE 2020 Hackathon with the Challenge Topic __Predicting Crisis__.
The app includes a analytical dashboard for deeper examination of the source data and the future predictions from our best performing ML-Models (XGBoost and RandomForestClassifier).

### TODO/Ideas:

  * Include Probability based predictions on a monthly base for more exact predictions
  * Add Time Series Analysis Predictions
  * Spatial Clustering based on Subnational areas

## Screenshots

|  Analytical Dashboard with Geospatial, Plotview and Predictions | Correlation Matrix for all Features filtered by Country |  Confusion Matrices for used ML Models |
|--------------------------------------|--------------------------------------|--------------------------------------|
| ![](https://raw.githubusercontent.com/herrfeder/herrfeder.github.io/master/tide_01.JPG) | ![](https://raw.githubusercontent.com/herrfeder/herrfeder.github.io/master/tide_02.JPG) | ![](https://raw.githubusercontent.com/herrfeder/herrfeder.github.io/master/tide_03.JPG) |

## Contributors

  * [Fabian Köhlinger](https://github.com/fkoehlin)
  * Oliver Bornschlegl

## Data Sources

### ACLED Data for Africa between 1997-2020
https://www.acleddata.com/download/16865/

### AFDB Social Economic Data 1960-2019
https://data.humdata.org/dataset/afdb-socio-economic-database-1960-2019

## Build and Run

Builds extended Dash environment for many usecases of creating a plotly dash web app:


  * Clone Repository and move into it

```
git clone https://github.com/herrfeder/NATO-TIDE-2020-Hackathon-Dash-App-Predicting-Crisis.git
cd NATO-TIDE-2020-Hackathon-Dash-App-Predicting-Crisis
```

  * Build the Docker Environment (it's multipurpose for a big variety of Dash Use-Cases):

`docker build . -t dash_container`
    
  * After successfully building the container run it (the folder with the Dash environment has to be called __webapp__):
    
`docker run -p 8050:8050 -v $PWD/:/home/user/src dash_container:latest`


