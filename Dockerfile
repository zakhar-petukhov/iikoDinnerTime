FROM python:3.7

RUN mkdir -p /var/log/gunicorn
RUN mkdir -p app
COPY . /app/

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["sh"]