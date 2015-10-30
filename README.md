# Specifications Director

## Introduction

Specifications Director is a multi-user application that allows you to edit through a nice UI any Monolithe Specifications Set hosted on a GitHub repository. It will provide you with controls to defines your Specification Files, Attributes, APIs, and Monolithe Configuration File.

Never touch a json specification again!


## Installation

### Using Docker

> For now, you must have access to the internal Nuage Networks DockerHub for now.

The easiest way to get everything up and running to use the `docker-compose.yml` file provided in the repository.

    mkdir specsdirector
    cd specsdirector
    curl [url-of-the-docker-compose.yml] > docker-compose.yml
    docker-compose up

Once everything is started, you can simply point your browser to:

    http://your-ip-or-docker-machine-ip

The UI will ask you for a API URL, simply enter:

    https://your-ip-or-docker-machine-ip


### Manually

Too complex for now my friend :)