# Use the official Apache Airflow image as the base image
FROM apache/airflow:2.7.1-python3.9

# Switch to root to install system dependencies
USER root

# Update and install necessary system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Copy the requirements.txt file to the container
COPY requirements.txt /opt/airflow/requirements.txt

# Check if requirements.txt is copied correctly
RUN ls -l /opt/airflow/requirements.txt

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies with detailed output
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt || \
    { echo "Failed to install requirements" >&2; exit 1; }

# Set the working directory
WORKDIR /opt/airflow

# Default command
CMD ["airflow", "worker"]
