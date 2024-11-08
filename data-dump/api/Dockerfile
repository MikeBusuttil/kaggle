FROM python:alpine
RUN apk add --no-cache --update-cache gfortran build-base wget libpng-dev openblas-dev
RUN apk add --no-cache tzdata
ENV TZ America/Toronto
RUN pip3 install python-dateutil flask gunicorn pymongo sh scikit-learn numpy sigfig
