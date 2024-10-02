FROM python:3.10.15
WORKDIR /python
COPY . ./
RUN pip install -e .[test]