FROM python:3.12.3

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

ADD . /code/

RUN pip3 install --upgrade pip \
    && pip3 install --upgrade setuptools \
    && pip3 install -r requirements.txt

CMD python3 manage.py runserver 0.0.0.0:8000