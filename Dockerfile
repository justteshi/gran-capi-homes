FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 3000

CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
