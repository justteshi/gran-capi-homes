# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY app/ .

# Run server (overridden during development)
CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
