##==============================================##
## Title    :  DevOps SonarQube Exporter        ##
## Author   :  Radja Fachriyanda                ##
## Date     :  09 November 2024                 ##
## Version  :  v1.1                             ##
##==============================================##

import requests
from prometheus_client import start_http_server, Gauge
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env into os.environ
load_dotenv() 

# SonarQube API URLs and token
print(os.environ['SONARQUBE_URL'])
print(os.environ['BEARER_TOKEN'])
LICENSE_USAGE_ENDPOINT = "/api/projects/license_usage"
SYSTEM_INFO_ENDPOINT = "/api/system/info"

# Prometheus metrics
health_check_gauge = Gauge('sonarqube_health_check', 'Health check status of SonarQube')
total_projects_gauge = Gauge('sonarqube_total_projects', 'Total number of projects in SonarQube')
total_loc_gauge = Gauge('sonarqube_total_lines_of_code', 'Total lines of code in SonarQube')
total_users_gauge = Gauge('sonarqube_total_users', 'Total number of users in SonarQube')
task_error_gauge = Gauge('compute_engine_tasks_error_progress', 'Tasks Error Progress in SonarQube')
task_success_gauge = Gauge('compute_engine_tasks_success_progress', 'Tasks Success Progress in SonarQube')
task_processing_gauge = Gauge('compute_engine_tasks_progressing_time', 'Tasks Processing Time in SonarQube')
task_web_jvm_max_memory_gauge = Gauge('web_jvm_max_memory', 'web_jvm_max_memory Web JVM Max Memory (MB)')
task_web_jvm_free_memory_gauge = Gauge('web_jvm_free_memory', 'web_jvm_free_memory Web JVM Free Memory (MB)')
task_web_jvm_heap_commited_gauge = Gauge('web_jvm_heap_commited', 'web_jvm_heap_commited Web JVM Heap Committed (MB)')
task_web_jvm_heap_init_gauge = Gauge('web_jvm_heap_init', 'web_jvm_heap_init Web JVM Heap Init (MB)')
task_web_jvm_heap_max_gauge = Gauge('web_jvm_heap_max', 'web_jvm_heap_max Web JVM Heap Max (MB)')
task_web_jvm_heap_used_gauge = Gauge('web_jvm_heap_used', 'web_jvm_heap_used Web JVM Heap Used (MB)')
task_web_jvm_non_heap_committed_gauge = Gauge('web_jvm_non_heap_committed', 'web_jvm_non_heap_committed Web JVM Non Heap Committed (MB)')
task_web_jvm_non_heap_init_gauge = Gauge('web_jvm_non_heap_init', 'web_jvm_non_heap_init Web JVM Non Heap Init (MB)')
task_web_jvm_non_heap_used_gauge = Gauge('web_jvm_non_heap_used', 'web_jvm_non_heap_used Web JVM Non Heap Used (MB)')
task_web_jvm_threads_gauge = Gauge('web_jvm_threads', 'web_jvm_threads Web JVM Threads')

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
    health_check = system_info_data.get("Health", {})
    if health_check == "GREEN":
        health_check_gauge.set(1)
    else:
        health_check_gauge.set(0)
        
    # Access the "Compute Engine Tasks" section from the response
    compute_engine_tasks = system_info_data.get("Compute Engine Tasks", {})

    # Get the value for "Processed With Error"
    task_error = compute_engine_tasks.get("Processed With Error", {})
    task_error_gauge.set(task_error)

    task_success = compute_engine_tasks.get("Processed With Success", {})
    task_success_gauge.set(task_success)

    task_processing = compute_engine_tasks.get("Processing Time (ms)", {})
    task_processing_gauge.set(task_processing)

    # Access the "Compute Engine JVM State" section from the response
    compute_engine_jvm_tasks = system_info_data.get("Compute Engine JVM State", {})

    # Get the value for "JVM State"
    task_jvm_max_memory = compute_engine_jvm_tasks.get("Max Memory (MB)", {})
    task_web_jvm_max_memory_gauge.set(task_jvm_max_memory)

    task_jvm_free_memory = compute_engine_jvm_tasks.get("Free Memory (MB)", {})
    task_web_jvm_free_memory_gauge.set(task_jvm_free_memory)

    task_jvm_heap_commited = compute_engine_jvm_tasks.get("Heap Committed (MB)", {})
    task_web_jvm_heap_commited_gauge.set(task_jvm_heap_commited)

    task_jvm_heap_init = compute_engine_jvm_tasks.get("Heap Init (MB)", {})
    task_web_jvm_heap_init_gauge.set(task_jvm_heap_init)

    task_jvm_heap_max = compute_engine_jvm_tasks.get("Heap Max (MB)", {})
    task_web_jvm_heap_max_gauge.set(task_jvm_heap_max)

    task_jvm_heap_used = compute_engine_jvm_tasks.get("Heap Used (MB)", {})
    task_web_jvm_heap_used_gauge.set(task_jvm_heap_used)

    task_jvm_non_heap_committed = compute_engine_jvm_tasks.get("Non Heap Committed (MB)", {})
    task_web_jvm_non_heap_committed_gauge.set(task_jvm_non_heap_committed)

    task_jvm_non_heap_init = compute_engine_jvm_tasks.get("Non Heap Init (MB)", {})
    task_web_jvm_non_heap_init_gauge.set(task_jvm_non_heap_init)

    task_jvm_non_heap_used = compute_engine_jvm_tasks.get("Non Heap Used (MB)", {})
    task_web_jvm_non_heap_used_gauge.set(task_jvm_non_heap_used)

    task_jvm_threads = compute_engine_jvm_tasks.get("Threads", {})
    task_web_jvm_threads_gauge.set(task_jvm_threads)

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