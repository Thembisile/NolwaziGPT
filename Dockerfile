# Use the official Python image as the base image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE nzulu_webapp.settings
ENV PORT 5000

# Create and set the working directory
WORKDIR /nzulu_chatapp

# Copy the project requirements file to the working directory
COPY requirements.txt /nzulu_chatapp/

# Install project dependencies
RUN pip install -r requirements.txt

# Copy the entire project directory to the working directory
COPY . /nzulu_chatapp/

# Install Gunicorn
RUN pip install gunicorn

# Run Gunicorn
CMD ["sh", "-c", "gunicorn nzulu_webapp.wsgi:application --bind 0.0.0.0:$PORT"]
