FROM python:3.12

WORKDIR /code

COPY requirements.txt ./

# Install python packages
ARG ENV_RULE_WRAPPER_VERSION
RUN sed -i -e "s|ENV_RULE_WRAPPER_VERSION|${ENV_RULE_WRAPPER_VERSION}|g" requirements.txt
RUN pip install -r requirements.txt


COPY ./ ./

CMD ["./bootstrap.sh"]