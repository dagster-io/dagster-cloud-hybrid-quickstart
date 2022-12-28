FROM python:3.8-slim

COPY setup.py /
RUN pip install .

WORKDIR /opt/dagster/app

COPY . /opt/dagster/app

# Make sure dagster-cloud is installed. Fail early here if not.
RUN dagster-cloud --version
