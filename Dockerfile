FROM python:3.8-slim
# Add any steps to install project system dependencies like java

WORKDIR /opt/dagster/app

COPY . /opt/dagster/app

# Add steps to install the Python dependencies for your Dagster project
# into the default Python on PATH
# For example, this project uses setup.py and we install all dependencies into the Docker container
# using `pip`. 

RUN pip install -e .
