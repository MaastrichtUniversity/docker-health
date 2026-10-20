FROM python:3.13

WORKDIR /opt/app

ENV PYTHONUNBUFFERED=1

# Federation base and keys are supplied at runtime by the environment:
#   DABS_FEDERATION_BASE, DABS_KEY, DABS_BTG_KEY, DABS_NODES
# The app is live-only: no fixtures, no fallback, no --mode/--dataset.
EXPOSE 8800

COPY tools tools
COPY web web
COPY server.py .

ENTRYPOINT ["python3", "server.py"]
