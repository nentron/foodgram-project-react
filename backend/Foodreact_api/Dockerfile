FROM python:3.7-slim
WORKDIR /app
COPY . .
RUN pip install requirements.txt --no-cache-dir
CMD ["python", "manage.py", "runserver", "0:8000"]
