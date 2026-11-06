FROM quay.io/jupyter/datascience-notebook:latest

USER root
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

USER ${NB_UID}
WORKDIR /home/jovyan/work
COPY --chown=${NB_UID}:${NB_GID} . /home/jovyan/work

EXPOSE 8888

# Hanya untuk penggunaan lokal; akses JupyterLab tanpa password atau token.
CMD ["start-notebook.py", "--ServerApp.token=", "--ServerApp.password="]
