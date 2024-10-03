FROM python:3.10.15
RUN apt-get update -y && apt-get install -y gdal-bin
WORKDIR /python
COPY . ./
RUN pip install -e .[test]