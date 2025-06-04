# Use a lightweight, secure Python image
FROM python:3.13-alpine


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apk update && apk add --no-cache \
    build-base \
    postgresql-dev \
    libffi-dev \
    musl-dev \
    gcc \
    python3-dev \
    jpeg-dev \
    zlib-dev \
    curl \
    netcat-openbsd

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port your app runs on
EXPOSE 8000

# Run the app using Gunicorn
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

