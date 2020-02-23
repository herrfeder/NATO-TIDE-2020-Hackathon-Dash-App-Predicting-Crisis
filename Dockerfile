FROM ubuntu:18.04
RUN apt-get update && apt-get install \
  -y --no-install-recommends python3 python3-dev python3-virtualenv \
  git-core curl build-essential openssl libssl-dev default-libmysqlclient-dev

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash
RUN apt-get install -y --no-install-recommends nodejs vim tmux
RUN node -v
RUN npm -v

RUN addgroup --gid 1000 dash && adduser --disabled-password --disabled-login --gecos "" --uid 1000 --gid 1000 user
USER user

WORKDIR /home/user
RUN mkdir install && cd install
RUN git clone https://github.com/plotly/react-chart-editor.git &&\ 
    cd react-chart-editor/examples/demo &&\
    npm install

WORKDIR /home/user
RUN npm install react-plotly.js plotly.js plotly.js-dist
RUN npm install react-cytoscapejs
RUN npm install cytoscape@3.2.19

RUN mkdir /home/user/venv
RUN python3 -m virtualenv --python=/usr/bin/python3 /home/user/venv

# Install dependencies:
RUN /bin/bash -c "source /home/user/venv/bin/activate" && /home/user/venv/bin/pip install \
 asn1crypto==0.24.0\
 atomicwrites==1.3.0 attrs==19.1.0 backcall==0.1.0 biopython==1.74\
 bleach==3.1.0 blinker==1.4 certifi==2019.6.16 cffi==1.12.3\
 chardet==3.0.4 Click==7.0 cloudpickle==1.2.1 colorama==0.4.1\
 colorcet==2.0.1 colorlover==0.3.0 coverage==4.5.4 cryptography==2.7\
 cufflinks cycler==0.10.0 dash dash-auth dash-bio\ 
 dash-canvas dash-colorscales dash-core-components\
 dash-cytoscape dash-html-components dash-renderer\
 dash-table dask datashader==0.7.0 datashape==0.5.2\
 decorator==4.4.0 defusedxml==0.6.0 distributed==2.2.0 dominate==2.4.0\
 elasticsearch==7.0.2 entrypoints==0.3 flake8==3.7.8 Flask\
 Flask-Bootstrap Flask-Compress Flask-DebugToolbar\
 Flask-Login Flask-SeaSurf Flask-Session Flask-WTF\
 fsspec==0.4.1 gunicorn HeapDict==1.0.0 idna==2.8 imageio==2.5.0\
 importlib-metadata==0.19 ipykernel==5.1.2 ipython ipython-genutils==0.2.0\
 ipywidgets==7.5.1 itsdangerous==1.1.0 jedi==0.15.1 Jinja2==2.10.1 joblib==0.13.2\
 jsonschema==3.0.2 jupyter-client==5.3.1 jupyter-core==4.5.0 kiwisolver==1.1.0\
 llvmlite==0.29.0 locket==0.2.0 lorem==0.1.1 MarkupSafe==1.1.1 matplotlib==3.0.3\
 mccabe==0.6.1 mistune==0.8.4 more-itertools==7.2.0 msgpack==0.6.1\
 multipledispatch==0.6.0 mysqlclient==1.4.4 nbconvert==5.6.0 nbformat==4.4.0\
 neobolt==1.7.13 neotime==1.7.4 networkx==2.3 notebook==6.0.0 numba==0.45.1\
 numpy==1.17.0 packaging==19.1 pandas==1.0.0 pandocfilters==1.4.2 param==1.9.1\
 parso==0.5.1 partd==1.0.0 pathlib==1.0.1 pathlib2==2.3.4 pexpect==4.7.0\
 pickleshare==0.7.5 Pillow==6.1.0 pkg-resources==0.0.0 plotly==4.5.0\
 pluggy==0.12.0 prometheus-client==0.7.1 prompt-toolkit==2.0.9 psutil==5.6.3\
 ptyprocess==0.6.0 py==1.8.0 py2neo==4.3.0 pycodestyle==2.5.0 pycparser==2.19\
 pyct==0.4.6 pyflakes==2.1.1 Pygments==2.3.1 pyOpenSSL==19.0.0 pyparsing==2.4.2\
 pyrsistent==0.15.4 pytest==5.0.1 pytest-cov==2.7.1 python-dateutil==2.8.0\
 pytz==2019.2 PyWavelets==1.0.3 PyYAML==5.1.2 pyzmq==18.1.0 requests==2.22.0\
 retrying==1.3.3 scikit-image==0.15.0 scikit-learn==0.21.3 scipy==1.3.1\
 Send2Trash==1.5.0 simple-salesforce==0.74.3 six==1.12.0 sortedcontainers==2.1.0\
 SQLAlchemy==1.3.6 stats==0.1.2a0 tblib==1.4.0 terminado==0.8.2 testpath==0.3.1\
 toolz==0.10.0 tornado==6.0.3 traitlets==4.3.2 ua-parser==0.8.0 urllib3==1.24.3\
 visitor==0.1.3 wcwidth==0.1.7 webencodings==0.5.1 Werkzeug==0.15.5\
 widgetsnbextension==3.5.1 WTForms==2.2.1 xarray==0.12.3 zict==1.0.0 zipp==0.5.2

RUN echo '#!/bin/bash' > entrypoint.sh
RUN echo 'source venv/bin/activate' >> entrypoint.sh
RUN echo 'gunicorn --bind 0.0.0.0:8050 src.webapp.app:server' >> entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ["/home/user/entrypoint.sh"]
