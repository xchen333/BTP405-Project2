FROM python:latest

WORKDIR /proj

RUN mkdir -p /proj/app

COPY app/ /proj/app/
COPY test_app.py /proj/
COPY init-mongo.js /proj/
COPY nginx.conf /proj/
COPY requirements.txt /proj/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80 443

CMD gunicorn -b 0.0.0.0:8080 app:app
