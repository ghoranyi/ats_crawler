FROM python:2.7

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y --force-yes qt5-default libqt5webkit5-dev build-essential python-lxml python-pip xvfb xorg openbox

RUN mkdir -p /opt/ghoranyi/ats_crawler

WORKDIR /opt/ghoranyi/ats_crawler

ADD requirements.txt ./
RUN virtualenv virtualenv
RUN virtualenv/bin/pip install -r requirements.txt

ADD *.py ./
ADD analyzers ./analyzers/
ADD utils ./utils/
ADD input.txt ./

CMD ["virtualenv/bin/python","main.py"]