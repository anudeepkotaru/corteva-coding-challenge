
## Problem 5 – Extra Credit: Deployment on AWS

### Step 1: Containerize the Django Project

1. Create a `Dockerfile` at the root of your project:

   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY . /app
   RUN pip install --no-cache-dir -r requirements.txt
   CMD ["gunicorn", "weather_project.wsgi:application", "--bind", "0.0.0.0:8000"]
   ```

2. Build the Docker image locally to ensure it works:

   ```bash
   docker build -t weather-api .
   ```

---

### Step 2: Push the Image to AWS ECR

1. Create an ECR repository

2. Authenticate Docker with ECR and push
---

### Step 3: Deploy the API to AWS

#### Option A: Use AWS Elastic Beanstalk

1. Initialize a Beanstalk environment with Docker support

2. Set environment variables (e.g., DB credentials) via the Beanstalk console or `eb setenv`.

3. Deploy the image

#### Option B: Use Amazon ECS + Fargate

1. Create a Task Definition that uses your container from ECR.

2. Set up a Service with Fargate launch type, and expose it via an Application Load Balancer (ALB).

3. Store secrets like DB credentials in AWS Secrets Manager or SSM Parameter Store.

4. Attach necessary IAM roles to allow ECS tasks to access RDS, logs, etc.

---

### Step 4: Deploy the PostgreSQL Database with Amazon RDS

1. Launch a new PostgreSQL instance on RDS.

2. Enable automatic backups, Multi-AZ for high availability, and IAM authentication if desired.

3. Whitelist the IPs or VPC security groups used by your ECS tasks or Beanstalk environment.

4. Store connection details in AWS Secrets Manager and reference them from your Django settings via environment variables.

---

### Step 5: Automate Weather Data Ingestion and Stats Computation

1. Package your Django management commands (`ingest_weather` and `compute_weather_stats`) as standalone Python functions.

2. Create two AWS Lambda functions:

   * One for ingesting weather data (periodic)
   * One for computing stats (daily or weekly)

3. Optionally, host your `.txt` weather files in Amazon S3 and have Lambda fetch from there.

4. Use Amazon EventBridge (or CloudWatch Events) to schedule these functions:

---

### Step 6: Add Monitoring and Logging

1. Send logs from your Django app, ECS, or Lambda functions to Amazon CloudWatch Logs.

2. Use CloudWatch Metrics and Alarms to track:

   * Lambda errors
   * API latency or 5xx errors from ECS/ALB
   * DB CPU/memory usage

3. Set up alerts via Amazon SNS to notify you of failures.

---

### Step 7: Manage Secrets and Configurations Securely

1. Store all sensitive values (DB creds, secret keys) in AWS Secrets Manager or SSM Parameter Store.

2. Use IAM roles for Lambda or ECS tasks to fetch these secrets securely without hardcoding them.

3. In your Django `settings.py`, pull in secrets using environment variables.

---

### Summary

This setup provides a production-ready cloud architecture with:

* Scalable compute (Beanstalk or ECS)
* Managed database (RDS)
* Scheduled jobs (Lambda + EventBridge)
* Secure secrets handling
* Monitoring, logging, and alerting

---


