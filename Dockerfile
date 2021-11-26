FROM python:3.8.5
ENV secret_key mysecretkey
RUN mkdir /code
RUN apt -y update && apt upgrade -y && \
   apt install nginx -y && apt install -y postgresql 
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
COPY . /code
WORKDIR /code
CMD [ "gunicorn", "--workers=1", "--threads=1", "-b 0.0.0.0:8000"]
