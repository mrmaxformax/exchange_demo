# Build and Install Stage
FROM python:3.8-alpine as base

FROM base as builder
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
RUN mkdir /opt/allure && mkdir /opt/allure-config
RUN wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.1/allure-commandline-2.13.1.tgz
RUN tar -xvf allure-commandline-2.13.1.tgz -C /opt/allure --strip-components=1
RUN apk add --no-cache --virtual curl
RUN pip install --no-cache-dir -r requirements.txt && \
    rm allure-commandline-2.13.1.tgz
RUN find /usr/local/lib/python3.8 -name '__pycache__' | xargs rm -rf
RUN find /usr/local/lib/python3.8 -name '*.c' -delete
RUN find /usr/local/lib/python3.8 -name '*.pyc' -delete
RUN find /usr/local/lib/python3.8 -name '*.pyc0' -delete
RUN rm -rf /root/.cache

# Final Stage
FROM base
RUN apk update && apk upgrade && \
    apk add --no-cache make openjdk8-jre curl sed
COPY --from=builder /usr/local/lib/ /usr/local/lib/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /opt/allure /opt/allure

ENV PATH="/opt/allure/bin:${PATH}"
ENV ALLURE_CONFIG="/opt/allure-config/allure.properties"

WORKDIR /opt/exchange_demo
COPY . /opt/exchange_demo
