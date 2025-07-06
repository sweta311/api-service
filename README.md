# Cloud-Native Application Assessment

[![Build, Test, and Publish API Service](https://github.com/sweta311/api-service/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/sweta311/api-service/actions/workflows/ci-cd.yml)

## Overview

This repository contains the complete solution for a technical assessment designed to showcase skills in modern cloud-native development and DevOps practices. The project follows the lifecycle of a simple API service, from initial code creation to a secure, policy-enforced deployment on Kubernetes.

**Core Technologies Used:**
*   **Application:** Python, FastAPI
*   **Containerization:** Docker
*   **CI/CD:** GitHub Actions
*   **Deployment:** Kubernetes, Helm
*   **Policy & Governance:** Open Policy Agent (OPA) Gatekeeper
*   **advanced optimizations:** advanced optimizations
---

## Table of Contents

*   [Task 0: Public Git Repository](#task-0-public-git-repository)
*   [Task 1: API Service Creation](#task-1-api-service-creation)
*   [Task 2: Dockerize the Application](#task-2-dockerize-the-application)
*   [Task 3: CI/CD with GitHub Actions](#task-3-ci-cd-with-github-actions)
*   [Task 4: Create a Helm Chart](#task-4-create-a-helm-chart)
*   [Task 5: Deploy to Kubernetes with OPA](#task-5-deploy-to-kubernetes-with-opa)
*   [Task 6: Documentation](#task-6-documentation)
*   [Task 7: advanced optimizations](#task-7-documentation)

---

### Prerequisites

Before you begin, ensure you have the following tools installed and configured:
*   [Git](https://git-scm.com/)
*   [Python](https://www.python.org/) 3.9+ & `pip`
*   [Docker](https://www.docker.com/)
*   [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) connected to a Kubernetes cluster (e.g., Minikube, Docker Desktop, or a cloud provider)
*   [Helm](https://helm.sh/docs/intro/install/)
*   [container-structure-test](https://github.com/GoogleContainerTools/container-structure-test/releases) (for local testing)

---

## Task 0: Public Git Repository

This public GitHub repository serves as the answer to this task. It was created to host the source code, configuration files, and documentation for all subsequent tasks.

**Best Practices Followed:**
*   **Meaningful Commits:** Commits follow a format to provide a clear and readable history of the project's development.
*   **`.gitignore`:** A standard Python `.gitignore` file is used to exclude unnecessary files (e.g., `__pycache__`, `venv/`) from version control.

---

## Task 1: API Service Creation

A simple web service was created using Python and the FastAPI framework.

*   **Endpoint `/api`:** Accepts requests and returns the method, headers, and body.
*   **Endpoint `/metrics`:** Exposes Prometheus-compatible metrics for observability.

### How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/sweta311/api-service.git
    cd api-service
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Run the service:**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8080
    ```

4.  **Test the API:**
    ```bash
    # Test the main endpoint
    curl --header "Content-Type: application/json" --data '{"user":"test"}' http://localhost:8080/api

    # Test the metrics endpoint
    curl http://localhost:8080/metrics
    ```

---

## Task 2: Dockerize the Application

A `Dockerfile` was created to containerize the API service, following best practices for security and efficiency.

**Key Files:**
*   `Dockerfile`: Defines the build process for the container image.
*   `.dockerignore`: Excludes unnecessary files to keep the image small and secure.
*   `test-config.yaml`: Defines integration tests for the built container image.

**Best Practices Implemented:**
*   **Multi-Stage Build:** A builder stage is used to install dependencies, keeping the final image minimal.
*   **Non-Root User:** The application runs as a dedicated non-root user inside the container to enhance security.
*   **Layer Caching:** Instructions are ordered to leverage Docker's build cache, speeding up subsequent builds.

### How to Build, Test, and Run

1.  **Build the Docker image:**
    ```bash
    docker build -t assessment-api-service .
    ```

2.  **Run automated integration tests (Bonus):**
    ```bash
    container-structure-test test --image assessment-api-service --config test-config.yaml
    ```
    This test verifies the image's metadata, file structure, and runtime behavior.

3.  **Run the container:**
    ```bash
    docker run -d -p 8080:8080 --name my-api assessment-api-service
    ```
    You can then test it at `http://localhost:8080`.

---

## Task 3: CI/CD with GitHub Actions

A CI/CD pipeline was implemented using GitHub Actions to automate the entire process from code commit to artifact publication.

**Key File:**
*   `.github/workflows/ci-cd.yml`

**Pipeline Stages:**
1.  **Lint:** Checks the Python code for style issues using `flake8`.
2.  **Build & Test:** Builds the Docker image and runs the `container-structure-test` suite.
3.  **Publish:** On a successful push to the `main` branch, the validated Docker image is pushed to a container registry.

This workflow ensures that only high-quality, tested code is turned into a deployable artifact.

---

## Task 4: Create a Helm Chart

A Helm chart was created to package the application and its Kubernetes configurations for easy and repeatable deployments.

**Location:** The chart is located in the `assessment-api-service-chart/` directory.

### How to Use the Chart

1.  **Lint the chart (check for errors):**
    ```bash
    cd assessment-api-service-chart/
    helm lint .
    ```

2.  **Install the chart:**
    ```bash
    helm install assessment-api-service . --namespace dev --create-namespace
    ```

3.  **Run Helm tests (Bonus):**
    After installation, you can run the built-in test to verify in-cluster connectivity.
    ```bash
    helm test assessment-api-service --namespace dev
    ```

---

## Task 5: Deploy to Kubernetes with OPA

This section details how to deploy the application and implement a security policy using Open Policy Agent (OPA) Gatekeeper. This demonstrates a production-grade, policy-as-code approach to governance.

### Step 1: Install OPA Gatekeeper and Apply Policies

First, we install Gatekeeper. Then, we wait for its Custom Resource Definitions (CRDs) to become active before applying our policy rules.

```bash
# Add the official Gatekeeper Helm repository
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts

# Install Gatekeeper into its own dedicated namespace
helm install gatekeeper gatekeeper/gatekeeper -n gatekeeper-system --create-namespace

# CRITICAL: Wait for the Gatekeeper CRDs to be established in the cluster
kubectl wait --for condition=established --timeout=60s crd/constrainttemplates.templates.gatekeeper.sh

# Apply the template that defines our security policy logic (the "what")
kubectl apply -f k8s-policy-template.yaml

# Apply the constraint that enforces the policy on all Deployments (the "where")
kubectl apply -f k8s-policy-constraint.yaml

# This deployment uses the 'default' service account and runs as root.
kubectl apply -f invalid-deployment.yaml -n dev

# The path to the chart is specified here
helm install assessment-api-service  --namespace dev
    ```

## Task 7: Workflow Optimization and Automation

This final section addresses the open-ended question about further optimizations and automation. The foundation we've built is solid, but in a real-world, production-grade environment, we can enhance it significantly in several key areas. Here are three proposals to create a truly automated, secure, and observable platform.

### 1. The GitOps Revolution: Deploying with Argo CD

Our current workflow uses `helm install`, which is a "push-based" manual command. A more advanced and declarative approach is **GitOps**, which makes Git the single source of truth for the desired state of our Kubernetes cluster.

**Proposed Implementation:**
1.  **Introduce Argo CD:** Deploy Argo CD into the Kubernetes cluster.
2.  **Manifest Repository:** Create a new, separate Git repository to store our application's Kubernetes manifests (the hydrated output of the Helm chart).
3.  **Update CI Pipeline:** The final step of the GitHub Actions pipeline would be modified. Instead of just pushing a Docker image, it would also automatically update the image tag in a file within the new manifest repository.
4.  **Automated Sync:** Argo CD would continuously monitor the manifest repository. Upon detecting the change, it would automatically "pull" the new configuration and sync the cluster, deploying the new version of the application without any manual intervention.


**Value Proposition:**
*   **Fully Declarative & Automated:** Deployments are triggered by a `git push`, requiring zero manual `kubectl` or `helm` commands.
*   **Enhanced Security & Auditability:** The entire deployment history lives in Git. Reverting to a previous version is as simple as `git revert`, and developers no longer need direct `kubectl` access to the production cluster.

### 2. Advanced "Shift-Left" and Runtime Security

Our OPA policy is excellent for admission control, but a robust security posture requires layers throughout the entire application lifecycle.

**Proposed Implementation:**
1.  **Container Vulnerability Scanning in CI:** Integrate a scanner like **Trivy** directly into our GitHub Actions workflow. A new step would be added after the `docker build` to scan the newly created image for known CVEs. The pipeline would be configured to fail if any high or critical severity vulnerabilities are found, preventing insecure images from ever being pushed to the registry.
2.  **Runtime Security with Falco:** Deploy **Falco**, the CNCF's runtime security engine, as a DaemonSet in the cluster. Falco acts as a behavioral sensor, detecting anomalous activity *inside* running containers (e.g., unexpected shell access, writing to sensitive directories, or suspicious network connections). If a rule is violated, Falco can trigger an alert or even automatically terminate the compromised pod.

**Value Proposition:**
*   **Defense-in-Depth:** We move from only securing what comes *in* (with OPA) to also securing what is *running* (with Falco), providing protection against zero-day exploits.
*   **Proactive Risk Reduction:** Vulnerability scanning in the CI pipeline prevents known security risks from ever reaching a production environment.

### 3. Full-Spectrum Observability: Logs and Traces

We have Prometheus metrics, which is one of the three pillars of observability. To achieve a complete operational picture, we must add logs and traces.

**Proposed Implementation:**
1.  **Log Aggregation with the PLG Stack:** Deploy **Promtail** as a DaemonSet to automatically scrape logs from all pods and send them to **Loki**. Loki is a log aggregation system designed by Grafana to integrate perfectly with Prometheus.
2.  **Distributed Tracing with OpenTelemetry:** Instrument the FastAPI application with the **OpenTelemetry SDK**. This would allow us to trace a single request as it flows through our system (and any other future microservices). The trace data would be sent to a backend like **Jaeger** or **Grafana Tempo**.
3.  **Unified Dashboarding in Grafana:** All three pillars—Prometheus metrics, Loki logs, and Tempo traces—can be visualized and correlated in a single **Grafana** dashboard. This enables powerful debugging workflows where an engineer can see a spike in a metric graph, instantly jump to the logs from that exact moment, and then pivot to the specific trace that caused the error.

**Value Proposition:**
*   **Radically Reduced Debugging Time:** This unified view moves troubleshooting from "What is broken?" to "Why is it broken?" in seconds.
*   **Proactive Performance Monitoring:** Allows us to understand the complete user experience and system performance, not just component health.
