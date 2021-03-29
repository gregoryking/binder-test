FROM jupyter/datascience-notebook:r-4.0.3

USER root
RUN apt-get -qq update && \
    apt-get -qq install --yes openjdk-8-jdk
USER jovyan

RUN pip install ipython-cypher py2neo

# matplotlib
RUN jupyter labextension install jupyter-matplotlib

# plotly
RUN jupyter labextension install jupyterlab-plotly
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget

RUN jupyter lab build

RUN mkdir -p /home/jovyan/.resources/local
ADD resources/* /home/jovyan/.resources/

ENV NEO4J_VERSION=3.5.26
ENV NEO4J_HOME=/home/jovyan/.resources/local/neo4j-${NEO4J_VERSION}

USER root
WORKDIR  /home/jovyan/.resources/local
ADD https://neo4j.com/artifact.php?name=neo4j-community-${NEO4J_VERSION}-unix.tar.gz ./neo4j-community-${NEO4J_VERSION}.tar.gz
RUN tar -xvf neo4j-community-${NEO4J_VERSION}.tar.gz >/dev/null
RUN rm neo4j-community-${NEO4J_VERSION}.tar.gz
RUN mv neo4j-community-${NEO4J_VERSION} neo4j-${NEO4J_VERSION}

# Install APOC
ENV APOC_VERSION=3.5.0.11
ADD https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/${APOC_VERSION}/apoc-${APOC_VERSION}-all.jar ./
RUN mv apoc-${APOC_VERSION}-all.jar ${NEO4J_HOME}/plugins

# Instal GDS
ENV GDS_VERSION=1.1.6
ADD https://s3-eu-west-1.amazonaws.com/com.neo4j.graphalgorithms.dist/graph-data-science/neo4j-graph-data-science-${GDS_VERSION}-standalone.zip ./
RUN unzip neo4j-graph-data-science-${GDS_VERSION}-standalone.zip >/dev/null
RUN rm neo4j-graph-data-science-${GDS_VERSION}-standalone.zip
RUN mv neo4j-graph-data-science-${GDS_VERSION}-standalone.jar ${NEO4J_HOME}/plugins

ADD neo4j.conf ${NEO4J_HOME}/conf/neo4j.conf
RUN chown -R jovyan ${NEO4J_HOME}

USER jovyan
ENV PATH="$NEO4J_HOME/bin:${PATH}"

WORKDIR  /home/jovyan/
ADD MarvelDemo.ipynb ./work/
ADD notebook_setup.py ./work/
# RUN mkdir ./work/figure

# EXPOSE 7687
# EXPOSE 7474

USER root
COPY ./go.sh /
RUN chown jovyan /go.sh
RUN chmod +x /go.sh
USER jovyan
ENTRYPOINT ["/go.sh"]
