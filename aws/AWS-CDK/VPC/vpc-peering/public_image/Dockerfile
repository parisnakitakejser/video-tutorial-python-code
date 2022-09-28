FROM python:3.9-buster

RUN mkdir /app
WORKDIR /app
COPY . .

RUN pip install -U Flask
RUN pip install requests

CMD ["python", "app.py"]