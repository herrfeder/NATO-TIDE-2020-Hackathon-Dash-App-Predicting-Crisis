# NATO TIDE 2020 Hackathon Dash App Predicting Crisis

## Screenshots

|  Landing Page with first Plotly Visualisation | Second Graph Visualisation on Landing Page |  Zoom into Second Graph Visualisation | Classification of Example Message "Help me. I need water." |
|--------------------------------------|--------------------------------------|--------------------------------------|--------------------------------------|
| ![](https://imgur.com/xTMDsW5.jpg) | ![](https://imgur.com/paJIsXT.jpg) | ![](https://imgur.com/bS8uYnF.jpg) | ![](https://imgur.com/95ZeX3K.jpg) |


## Data Sources

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


