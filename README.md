# Version 1.1
# SonarQube Prometheus Exporter

This project is a Python-based Prometheus exporter that fetches metrics from SonarQube via its REST API and exposes them to Prometheus for monitoring and visualization (e.g., in Grafana). The exporter collects information about project health, total number of projects, lines of code (LOC), and user count in your SonarQube instance.

## Features

- **Health Check**: Monitors the health status of your SonarQube instance.
- **Total Projects**: Displays the total number of projects in SonarQube.
- **Lines of Code (LOC)**: Provides the total lines of code across all projects and lines of code per project.
- **User Monitoring**: Tracks the total number of users in the SonarQube instance.
- **Computer Engine Task Metrics**: Provides key metrics for tasks performed by the computer engine.
- **Computer Engine JVM State Metrics**: Monitors and displays the current state of the JVM used by the computer engine, including memory usage, thread counts, and other JVM-specific metrics.

## Prerequisites

- **SonarQube Instance**: Make sure you have a running SonarQube instance with access to its REST API.
- **Prometheus**: Prometheus should be set up to scrape the metrics from this exporter.
- **Docker (Optional)**: The exporter can be containerized using the provided Dockerfile.

## Requirements

- **Python 3.9+**
- **requirements.txt**: requests, prometheus-client

## Installation

- **Build Docker Image**: docker build -t radjafachri/sonarqube-exporter:latest . 
- **Create Container**: docker run -d --name='sonarqube-exporter' -p8000:8000 -eSONARQUBE_URL='http://xxx.sonarqube.xxx:90XX' -eBEARER_TOKEN='squ_27*******************' radjafachri/sonar-exporter:latest