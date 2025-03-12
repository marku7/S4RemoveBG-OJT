FROM python:3.9-slim

WORKDIR /app

# system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# copy and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy main code
COPY main.py .

# Expose port
EXPOSE 8000

# run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]