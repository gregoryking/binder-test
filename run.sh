#!/usr/bin/env bash

# docker run -e GRANT_SUDO=yes --user root -p 8888:8888 -p 7687:7687 -p 7474:7474 -it --rm jupyter/my-datascience-notebook /bin/bash #jupyter lab --ip 0.0.0.0 --NotebookApp.token=''
# docker run -p 8888:8888 -p 7474:7474 -p 7687:7687 --rm -it jupyter/my-datascience-notebook
docker run -p 8888:8888 -p 7474:7474 -p 7687:7687 --volume=/Users/greg/Downloads/Notebooks:/home/jovyan/work  --rm -it jupyter/my-datascience-notebook jupyter lab --ip 0.0.0.0 --NotebookApp.token=''
