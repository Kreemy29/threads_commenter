# Stage 1: Dependencies
FROM python:3.11-slim AS dependencies

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from the dependencies stage
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application code
COPY . .

# Create a non-root user to run the application
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8000

# Expose the port
EXPOSE ${PORT}

# Run the application
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"] 