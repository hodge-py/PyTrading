# Use Python 3.12 slim for the smallest base possible
FROM python:3.12-slim

# 1. Install 'uv' (incredibly fast pip replacement)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Add the virtual environment to the PATH
ENV PATH="/opt/venv/bin:$PATH"

# 3. Set the working directory
WORKDIR /app

# 4. Copy requirements and install them into a virtual environment
# We do this BEFORE copying the rest of the code to speed up future builds
COPY requirements.txt .
RUN /bin/uv venv /opt/venv && \
    /bin/uv pip install --no-cache -r requirements.txt

# 5. Copy ONLY your source files to prevent accidental bloat
# This ensures we don't copy local .venv or huge data folders
COPY app.py .
COPY all_tickers.txt .
COPY pystock.py .
# If you have a 'pages' folder, uncomment the line below:
COPY pages/ ./pages/


# 6. Safety check: remove any local virtual environments if they were copied
RUN rm -rf venv .venv

# 7. Expose the Streamlit port
EXPOSE 8501

# 8. Start the app (Pointing to app.py)
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]