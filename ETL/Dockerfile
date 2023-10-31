FROM python:3.12

WORKDIR /code

COPY ./ ./

# Install python packages
RUN pip install -r requirements.txt

CMD ["./bootstrap.sh"]
