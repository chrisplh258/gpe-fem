FROM mambaorg/micromamba:1.5.10

#default
ARG ENV_FILE=environment-complex.yml

WORKDIR /app

COPY --chown=$MAMBA_USER:$MAMBA_USER ${ENV_FILE} /tmp/environment.yml

RUN micromamba create -y -f /tmp/environment.yml && \
    micromamba clean --all --yes

ENV PATH=/opt/conda/envs/fem-gpe/bin:$PATH

COPY --chown=$MAMBA_USER:$MAMBA_USER . /app

ENV PYTHONPATH=/app

CMD ["bash"]