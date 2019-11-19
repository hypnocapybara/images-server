FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN apt install libmagickwand-dev

COPY . /app
RUN pip install -r /app/requirements.txt
