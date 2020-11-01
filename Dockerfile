FROM python:3.6

LABEL maintainer="info@manceps.com"

COPY requirements.txt /opt

RUN apt-get update && \
    python3 -m pip install --upgrade pip && \    
    pip3 install -r /opt/requirements.txt

WORKDIR /opt

COPY app/ /opt

CMD python3 routes.py


