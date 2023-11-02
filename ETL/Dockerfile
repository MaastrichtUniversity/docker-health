FROM python:3.12.0

WORKDIR /code

# Copy requirements.txt first to install the packages early during the build
COPY requirements.txt ./

# Install python packages
RUN pip install -r requirements.txt

COPY ./ ./

ENTRYPOINT ["./bootstrap.sh"]
CMD ["run"]

