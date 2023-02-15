FROM python:3.9-buster

RUN apt-get update && \
    apt-get dist-upgrade -y

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "app.py" ]