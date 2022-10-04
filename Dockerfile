FROM python:3.10-slim-bullseye AS build
LABEL maintainer="Sean Harrison <sah@kruxia.com>"

RUN apt-get update \
    && apt-get install -y \
    postgresql-client \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY ./ /app

FROM build AS deploy
EXPOSE 8000
ENTRYPOINT [ "./docker-entrypoint.sh" ]
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--log-level", "debug", "app.main:app"]

FROM deploy AS test
RUN pip install -e .[test]

FROM deploy AS develop
RUN pip install -e .[dev,test]
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]
