FROM python:alpine

# setup wordlr
WORKDIR /app

# copy source code
COPY . .

# install requirements
RUN python -m pip install -r requirements.txt

# start server
CMD python manage.py runserver 0.0.0.0:8000

# enable django port
EXPOSE 8000
