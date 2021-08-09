# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9.6-slim-buster

# Make sure working dir exists
RUN mkdir -p /usr/src/app
# set working directory
WORKDIR /usr/src/app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# install system dependencies
RUN apt-get update && apt-get -y install netcat gcc && apt-get clean

# Upgrade pip to latest
RUN pip install --upgrade pip
# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# add app
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
