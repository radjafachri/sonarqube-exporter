##==============================================##
## Title    :  DevOps SonarQube Exporter        ##
## Author   :  Radja Fachriyanda                ##
## Date     :  07 October 2024                  ##
##==============================================##

import requests
from prometheus_client import start_http_server, Gauge
import time

# SonarQube API URLs and token
SONARQUBE_URL = "http://xxx.sonarqube.xxx:90XX"
LICENSE_USAGE_ENDPOINT = "/api/projects/license_usage"
SYSTEM_INFO_ENDPOINT = "/api/system/info"
BEARER_TOKEN = "squ_***************************"

# Prometheus metrics
health_check_gauge = Gauge('sonarqube_health_check', 'Health check status of SonarQube')
total_projects_gauge = Gauge('sonarqube_total_projects', 'Total number of projects in SonarQube')
total_loc_gauge = Gauge('sonarqube_total_lines_of_code', 'Total lines of code in SonarQube')
total_users_gauge = Gauge('sonarqube_total_users', 'Total number of users in SonarQube')

# New: Lines of code by project
loc_by_project_gauge = Gauge('sonarqube_loc_by_project', 'Lines of code by project', ['project_name', 'branch'])

# Function to get data from SonarQube API
def get_sonarqube_data():
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    # Get license usage data
    license_usage_url = SONARQUBE_URL + LICENSE_USAGE_ENDPOINT
    license_usage_response = requests.get(license_usage_url, headers=headers)
    license_usage_data = license_usage_response.json()

    # Get system info (for health check)
    system_info_url = SONARQUBE_URL + SYSTEM_INFO_ENDPOINT
    system_info_response = requests.get(system_info_url, headers=headers)
    system_info_data = system_info_response.json()

    return license_usage_data, system_info_data

# Function to update Prometheus metrics
def update_metrics():
    license_usage_data, system_info_data = get_sonarqube_data()

    # Update health check status
    health_check = system_info_data.get("health", {}).get("status", "UNKNOWN")
    health_check_gauge.set(1 if health_check == "GREEN" else 0)

    # Aggregate data for total projects and total lines of code
    total_projects = len(license_usage_data.get("projects", []))
    total_loc = sum(project.get("linesOfCode", 0) for project in license_usage_data.get("projects", []))

    # Update total projects and LOC
    total_projects_gauge.set(total_projects)
    total_loc_gauge.set(total_loc)

    # Update lines of code for each project
    for project in license_usage_data.get("projects", []):
        project_name = project.get("projectName", "unknown_project")
        branch = project.get("branch", "unknown_branch")
        loc = project.get("linesOfCode", 0)
        
        # Update metric for each project with project name and branch as labels
        loc_by_project_gauge.labels(project_name=project_name, branch=branch).set(loc)

    # Assuming user data comes from the system info endpoint (if available)
    total_users = system_info_data.get("users", {}).get("count", 0)
    total_users_gauge.set(total_users)

if __name__ == "__main__":
    # Start Prometheus server to expose metrics
    start_http_server(8000)
    
    # Update metrics in an infinite loop
    while True:
        update_metrics()
        time.sleep(30)  # Scrape every 30 seconds