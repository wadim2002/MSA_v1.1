FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/dm_rest

COPY requirements.txt /usr/src/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/dm_rest

EXPOSE 9090
CMD ["python", "manage.py" , "runserver", "0.0.0.0:9090"]