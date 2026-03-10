# Use Python 3.12 slim for the smallest base possible
FROM python:3.12-slim

# 1. Install 'uv' (incredibly fast pip replacement)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Add the virtual environment to the PATH so we can run 'streamlit' directly
ENV PATH="/opt/venv/bin:$PATH"

# 3. Set the working directory
WORKDIR /app

# 4. Copy your requirements and install them into a virtual environment
COPY requirements.txt .
RUN /bin/uv venv /opt/venv && \
    /bin/uv pip install --no-cache -r requirements.txt

# 5. Copy your code (main.py, pages folder, all_tickers.txt)
COPY . .

# 6. Expose the Streamlit port
EXPOSE 8501

# 7. Start the app
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]