FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

# Install Python 3.12, pip, and venv
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y python3.12 python3-pip python3-venv \
    && apt-get install -y libjemalloc-dev \
    && apt-get install -y cron curl \
    && apt-get install -y logrotate

ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.2

WORKDIR /home

# Set up a virtual environment
RUN python3 -m venv /venv

# Make sure we use the virtual environment
ENV PATH="/venv/bin:$PATH"

# Copy requirements and install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./ .

# Expose the required port
EXPOSE 4000

ENTRYPOINT [ "python3", "run.py" ]