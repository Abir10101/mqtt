FROM python:3.11.2-alpine
LABEL maintainer=abir10101

RUN apk update && apk add --no-cache bash curl \
    && pip install --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "app.py"]
