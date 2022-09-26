FROM python:3.9-buster

RUN mkdir /app
WORKDIR /app

RUN pip install Flask

COPY . .

CMD ["python", "app.py"]