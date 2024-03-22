# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install pipenv
RUN pip install pipenv

# Install dependencies using Pipenv
# --system: Install packages into the system Python, not a virtualenv
# --deploy: Abort if the Pipfile.lock is out-of-date, or Python version is wrong
# --ignore-pipfile: Ignore the Pipfile for installation and use what's in the Pipfile.lock
RUN pipenv install --system --deploy --ignore-pipfile

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]