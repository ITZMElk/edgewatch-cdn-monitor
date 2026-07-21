FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV PYTHONUNBUFFERED=1
ENV DISABLE_BROWSER=1
EXPOSE 5000 5001 5002 5003 8000
CMD ["python", "main.py"]
