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

# Pre-download the model
RUN python -c "from rembg.bg import download_models; download_models()"

# copy main code
COPY main.py .

# Expose port
EXPOSE 8000

# run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]