
# Use a lightweight official Python image.
FROM python:3.13-slim

# Prevent Python from writing bytecode files.
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure Python logs appear immediately in container output.
ENV PYTHONUNBUFFERED=1

# Set the application working directory.
WORKDIR /app

# Install system dependencies required for package installation.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definitions first.
# This allows Docker to reuse the dependency layer when
# application source code changes.
COPY requirements.txt .

# Install Python dependencies.
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

# Copy application source code.
COPY app/ ./app/

# Create a non-root user for better security.
RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser \
    && chown -R appuser:appgroup /app

# Run the application as a non-root user.
USER appuser

# Document the port used by the application.
EXPOSE 8000

# Start the FastAPI application.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
