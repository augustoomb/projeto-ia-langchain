# Use Python 3.10 as the base image
FROM python:3.10.13

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Install Python dependencies
RUN python -m venv venv && \
    /app/venv/bin/python -m pip install --upgrade pip && \
    /app/venv/bin/python -m pip install -r requirements.txt

COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["/app/venv/bin/gunicorn", "app:app", "--timeout", "900", "--bind", "0.0.0.0:8000"]
