FROM debian:bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends libmagic1 gcc python3-dev python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV USER="jupyter"

RUN adduser --disabled-login --gecos "$USER user" $USER

WORKDIR /home/$USER
USER $USER

RUN python3 -m pip install --no-warn-script-location \
    jupyterlab matplotlib python-magic qrcode rgb-lib==0.1.2

COPY ./notebooks/rgb-lib.ipynb sample.png ./

CMD ["/home/jupyter/.local/bin/jupyter-lab", "--ip=0.0.0.0"]
