# Use a slim Python image to keep the size down
FROM python:3.11-slim

# Install system dependencies (needed for TA-Lib or C-based packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app (including /pages and all_tickers.txt)
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Run the app
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]