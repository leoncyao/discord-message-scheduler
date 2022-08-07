FROM python:3.10-slim as py

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends g++ git && rm -rf /var/lib/apt/lists/*

FROM py as build

COPY requirements.txt /
RUN pip install --prefix=/inst -U -r /requirements.txt

FROM py

COPY --from=build /inst /usr/local

WORKDIR /bot
CMD ["python", "start.py"]
COPY . /bot
