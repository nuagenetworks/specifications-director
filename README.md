# Specifications Director

## Introduction

Specifications Director is a client/server application that makes super easy to work on any Monolithe Specifications that are hosted on GitHub (private or public) using a cool user interface. It allows you work on various specifications, hosted on various repositories on different branches. All your work will be committed to the corresponding GitHub repository transparently. For each repository, you will be able to perform a synchronization of the specifications. If you have the right to write on the repository, it will merge back the master branch of the upstream repository (if any) into your working branch, and will pull the new changes.

Specification Director supports LDAP for the authentication of your users, and will work for public and private repositories hosted on GitHub.com as well have an internal GitHub Enterprise running in your own company.

As it is a Garuda based projects, the backend will scale well in a container environment, without any further configuration (other than having a cool Docker swarm). Specifications Director will enqueue all of the GitHub operations and smoothly balance the workload across all of the available workers.

Never touch a json specification again!


## Installation

You need Docker and Compose. Then simply run in your terminal:

    $ curl http://bit.ly/25npKrI > docker-compose.yml && docker-compose up

> The configuration is basic in that docker compose, and there will be no authentication. Plus it will use pregenerated certificates, that you **must** for any real production scenario. More informations on DockerHub for the [server](https://hub.docker.com/r/monolithe/specsdirector-server/) and for the [client](https://hub.docker.com/r/monolithe/specsdirector-client/).

## Accessing the Application

If you are using the default Docker Machine, get the IP by doing:

    $ docker-machine ip
    192.168.99.100

Then point your browser to `https://192.168.99.100`, and make it connect to the `Server` address in the login window to `https://192.168.99.100:1984` You can enter any login, and any password to access the application. It you use the same login later, your data will be retrieved.

More informations about how to secure everything on [DockerHub](https://hub.docker.com/r/monolithe/specsdirector-server/).

Peace!
