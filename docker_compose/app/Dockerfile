FROM python:3.7-slim

RUN ls -al
# VOLUME MAPPED ./web:/var/www/app
WORKDIR /var/www/app
RUN ls -al

ADD . .
RUN ls -al

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

CMD ["gunicorn", "--reload", "wsgi:app", "w", "1", "-b", "0.0.0.0:8080"]

# migrationss
# RUN python manage.py migrate
