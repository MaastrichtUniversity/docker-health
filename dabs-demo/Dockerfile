FROM python:3.13

WORKDIR /opt/app

ENV PYTHONUNBUFFERED=1

EXPOSE 8800

COPY fixtures fixtures
COPY fixtures-rich fixtures-rich
COPY tools tools
COPY web web
ADD server.py .

ENTRYPOINT ["python3", "server.py", "--mode", "fixture", "--dataset", "rich"]
# TODO Fix federation and the ENTRYPOINT change to
# ENTRYPOINT ["python3", "server.py", "--mode", "live"]