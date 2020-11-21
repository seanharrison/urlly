FROM python:3.8-slim-buster

RUN apt-get update \
    && apt-get install -y \
        postgresql-client \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY ./ /app
RUN pip install -e .

EXPOSE 8000
ENTRYPOINT [ "./docker-entrypoint.sh" ]
CMD ["bash"]