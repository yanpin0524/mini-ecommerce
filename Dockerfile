FROM python:3.11.8

# ENV django_secret_key=""
# ENV db_host=localhost
# ENV db_port=3306
# ENV db_user=root
# ENV db_password=123456
# ENV db_name=mini_ecommerce

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000