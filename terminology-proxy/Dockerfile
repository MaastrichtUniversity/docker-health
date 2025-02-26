FROM python:3.12

WORKDIR /opt/app

# Python requirements
RUN pip install Flask requests Flask-RESTful

ADD main.py .

# Entrypoint
ENTRYPOINT ["python", "-u", "main.py"]