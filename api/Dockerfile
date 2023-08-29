FROM python:3.11.2-alpine
LABEL maintainer=abir10101

RUN apk update && apk add --no-cache bash curl \
    && pip install --upgrade pip

WORKDIR /backend
COPY ./requirements.txt /backend
RUN pip install --no-cache-dir -r requirements.txt

COPY . /backend

EXPOSE 5000
CMD ["sh", "run.sh"]
