FROM python:3.11.8

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

# 啟動 Django 服務
CMD ["python", "manage.py", "runserver"]