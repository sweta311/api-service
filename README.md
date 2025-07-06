# Request Inspector API Service

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Framework](https://img.shields.io/badge/Framework-FastAPI-green)

This project is a simple, cloud-native web service built with Python and FastAPI. It fulfills the assessment requirement to create an API that inspects incoming HTTP requests and returns their details. The service is also instrumented with Prometheus metrics for observability, adhering to modern DevOps best practices.

---

### Key Features

*   **Request Inspection:** A multi-method endpoint at `/api` that details the headers, method, and body of any request.
*   **Prometheus Metrics:** A `/metrics` endpoint that automatically exposes key performance indicators, including a total request counter.
*   **Interactive Documentation:** Automatic, interactive API documentation (Swagger UI) available at `/docs`, provided by FastAPI.
*   **Cloud-Native Design:** Built following the Twelve-Factor App methodology for configuration, logging, and deployment.

---

### Setup and Running the Service

Follow these steps to get the application running locally.

#### Prerequisites

*   Python 3.9+
*   `pip` and `venv`

#### Instructions

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:sweta311/Task-1-API-service.git
    cd Task-1-API-service
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8080
    ```
    The server will be running at `http://localhost:8080`.

---

### Usage and Testing

You can interact with the service in several ways.

#### 1. Testing the `/api` Endpoint with cURL

You can send a `POST` request with a JSON body to the `/api` endpoint. The service will respond with the details of your request.

**Command:**
```bash
curl --header "Content-Type: application/json" --data '{"username":"sweta","password":"sweta@981"}' http://localhost:8080/api
