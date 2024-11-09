# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Prometheus will scrape (8000)
EXPOSE 8000

# Define environment variable for SonarQube URL and Bearer Token (you can also set these as docker environment variables)
# ENV SONARQUBE_URL="https://your-sonarqube-instance.com"
# ENV BEARER_TOKEN="your_bearer_token_here"

# Run the Python script when the container launches
CMD ["python", "sonar-exporter.py"]