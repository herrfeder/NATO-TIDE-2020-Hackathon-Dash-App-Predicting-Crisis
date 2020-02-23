Builds extended Dash environment for many usecases of creating a plotly dash web app:
RUN:

    `docker pull herrfeder/virtualenv_auto_webserver`
    
According to the included Dockerfile the name of the Dash folder has to be __webapp__:
    
    `docker run -it -p 8050:8050 -v /home/<location of dash app>:/home/user/src virtualenv_auto_webserver:latest`

