FROM python:3.8-slim

# Installing dependencies first enables better Docker caching
COPY *setup.py /
RUN if [ -f "setup.py" ]; then \
        pip install .; \
    fi

WORKDIR /opt/dagster/app
COPY . /opt/dagster/app
