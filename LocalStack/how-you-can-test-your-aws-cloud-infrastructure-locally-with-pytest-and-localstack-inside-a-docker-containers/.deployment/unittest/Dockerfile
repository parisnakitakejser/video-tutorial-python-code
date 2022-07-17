FROM python:3.9-buster

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN touch tests/.env
RUN rm -rf tests/.env
RUN mv tests/.env-test tests/.env

CMD [ "pytest" ]