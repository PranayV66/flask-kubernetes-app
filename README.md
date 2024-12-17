# Flask Kubernetes Application with CI/CD, Helm, Argo CD and GitHub Pages Helm Repository

This repository demonstrates a fully automated pipeline and GitOps workflow for deploying a Python flask based microservices application to a K8s cluster. The setup uses Helm charts for packaging and versioning, a separate GitHub Pages Repository to store Helm charts and Argo CD for continuously delivering changes to the cluster. 

## Application Overview

The application consists of two main components:

1. **Backend (Flask API)**:
    A Python Flask application which, at this point, provides backend logic to access data from a Postgres Database. This is containerized with Docker and published to Docker Hub with unique tags corresponding to the commit hash.

2. **Frontend (Flask based Web UI)**:
    Another flask instance serving a simple web interface. It communicates with the backend API to display the information retrieved from the Postgres DB. Similarly containerized and pushed to Docker Hub.

3. **PostgreSQL Database**:
    Deployed using the Bitnami PostgreSQL Helm Chart as a dependency. The DB is initialized using the `initdb` script to run on first startup. This script creates a table and insert initial data, so the application is initialized with some dummy starting from the first run.

## Architecture and Workflow:

1. **Repositories**
   - **`flask-kubernetes-app`** (this repo):  
     Contains:
     - **Application Source Code**: `frontend/` and `backend/` directories with Dockerfiles and Flask logic.
     - **Helm Chart Source**: `charts/flask-kubernetes-app/` including `Chart.yaml`, `values.yaml`, and `templates/` for Kubernetes manifests. The chart also references the Bitnami PostgreSQL chart as a dependency.
     - **CI/CD Pipeline**: `.github/workflows/ci-cd.yaml` that builds images, increments the chart version, updates `values.yaml`, packages the chart, and triggers updates in another repo.

   - **`flask-kubernetes-app-helm`**:
     A separate repository hosting the packaged Helm charts and `index.yaml`

2. **CI/CD Pipeline (GitHub Actions)**:
   On every commit to `main` in `flask-kubernetes-app`:
   - **Build and Push Docker Images**:  
     The backend and frontend Docker images are rebuilt, tagged with the commit SHA, and pushed to Docker Hub.
   - **Update `values.yaml`**:  
     The Helm chart’s `values.yaml` is updated with the new image tags so the cluster can pull the correct images.
   - **Increment Chart Version**:  
     The chart version in `Chart.yaml` is bumped (e.g., from `2.0.0` to `2.0.1`) to ensure Argo CD recognizes a new release.
   - **Package the Chart**:  
     The chart is packaged into a `.tgz` file for distribution.
   - **Trigger `flask-kubernetes-app-helm` Repo Dispatch**:  
     An event signals the `flask-kubernetes-app-helm` repo to update `index.yaml` and commit the new `.tgz` file. This refreshes the Helm repository served by GitHub Pages.

     https://PranayV66.github.io/flask-kubernetes-app-helm/helm-repo/

     Anyone can `helm repo add` this URL and install the chart.

3. **Argo CD for GitOps**:
    - Argo CD watches the code repository for when the chart version changes, it detects the new release and automatically synchronizes the Kubernetes cluster.
    - Because each run increments the chart version and updates image tags, Argo CD continuously delivers new application versions without manual intervention.

## Using the application

### Initial Database Setup

The Postgres chart is configured with `initdb.scripts` to run a SQL script on the first run. This script creates a table (`items`) and inserts initial rows. As a result, when the backend starts, it can query and show meaningful data right away, and the frontend can display this data.

If you delete the PVC and redeploy from scratch, the `initdb` scripts run again, ensuring a fresh start with seeded data.

### Installing the Chart Locally (Optional)

If someone wants to install the application locally (without Argo CD or the GitOps pipeline):

1. Add the Helm repo:
```bash
helm repo add myapp-repo https://PranayV66.github.io/flask-kubernetes-app-helm/helm-repo/
helm repo update
```
2. Install the chart:
```bash
helm install my-flask-app myapp-repo/flask-kubernetes-app
