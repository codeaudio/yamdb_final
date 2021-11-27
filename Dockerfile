FROM python:3.8.5
RUN sudo docker stop $(sudo docker ps -a -q)
RUN sudo docker rm $(sudo docker ps -a -q)
RUN sudo docker rmi $(sudo docker images -q)
WORKDIR /newcode
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
RUN python manage.py collectstatic --noinput
CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
