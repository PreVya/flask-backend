FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --ignore-installed -r requirements.txt --break-system-packages

# Copy the Flask app
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
