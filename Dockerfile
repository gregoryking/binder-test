FROM jupyter/datascience-notebook:r-4.0.3

USER root
RUN apt-get -qq update && \
    apt-get -qq install --yes openjdk-8-jdk
USER jovyan

# matplotlib
RUN jupyter labextension install jupyter-matplotlib

# plotly
RUN jupyter labextension install jupyterlab-plotly
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget

RUN jupyter lab build

RUN mkdir -p ~/resources/local \
    && cd  ~/resources/local

ENV NEO4J_VERSION=3.5.8
ENV NEO4J_HOME=./neo4j-${NEO4J_VERSION}

ADD https://neo4j.com/artifact.php?name=neo4j-community-${NEO4J_VERSION}-unix.tar.gz ./neo4j-${NEO4J_VERSION}.tar.gz

USER root
RUN tar -xvf neo4j-${NEO4J_VERSION}.tar.gz >/dev/null
RUN rm neo4j-${NEO4J_VERSION}.tar.gz
RUN mv neo4j-community-${NEO4J_VERSION} neo4j-${NEO4J_VERSION}
ADD https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/3.5.0.15/apoc-3.5.0.15-all.jar ./
RUN mv apoc-3.5.0.15-all.jar ${NEO4J_HOME}/plugins
ADD neo4j.conf ${NEO4J_HOME}/conf/neo4j.conf
RUN chown -R jovyan ${NEO4J_HOME}

USER jovyan
ENV PATH="$NEO4J_HOME/bin:${PATH}"
EXPOSE 7687
EXPOSE 7474

USER root
COPY ./go.sh /
RUN chown jovyan /go.sh
RUN chmod +x /go.sh
USER jovyan
ENTRYPOINT ["/go.sh"]
