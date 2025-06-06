# Streamlit Cohort Analysis - Cloud Run Deployment

This repository contains a Streamlit application for streaming cohort analysis, packaged for deployment on Google Cloud Run.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed locally
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed
- A Google Cloud Platform account with billing enabled

## Local Development

1. Create a virtual environment:
   ```bash
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

3. Run the Streamlit app locally:
   ```bash
   streamlit run Home.py
   ```

## Using Docker for Development

You can also run the application locally using Docker:

1. Build the Docker image:
   ```bash
   docker build -t streamlit-app .
   ```

2. Run in development mode:
   ```bash
   docker run -p 8501:8501 -e DEV_MODE=true streamlit-app
   ```

## Deployment Steps

### 1. Build Docker Image

For Mac with Apple Silicon or other ARM-based systems:
```bash
# Build for the platform required by Cloud Run
docker build --platform linux/amd64 -t streamlit-cohort-analysis .
```

For x86/amd64 systems:
```bash
docker build -t streamlit-cohort-analysis .
```

### 2. Authenticate with Google Cloud

```bash
# Login to Google Cloud
gcloud auth login

# Configure Docker to use Google Cloud credentials
gcloud auth configure-docker

# Set your project ID
gcloud config set project YOUR_PROJECT_ID
```

### 3. Tag and Push the Docker Image

```bash
# Tag the image for Google Container Registry
docker tag streamlit-cohort-analysis gcr.io/YOUR_PROJECT_ID/streamlit-cohort-analysis

# Push the image to Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/streamlit-cohort-analysis
```

### 4. Deploy to Cloud Run

```bash
gcloud run deploy streamlit-cohort-analysis \
  --image gcr.io/YOUR_PROJECT_ID/streamlit-cohort-analysis \
  --platform managed \
  --allow-unauthenticated \
  --region us-central1 \
  --project YOUR_PROJECT_ID
```

After successful deployment, you'll receive a URL where your application is accessible.

## Configuration Options

You can customize the deployment with additional flags:

```bash
gcloud run deploy streamlit-cohort-analysis \
  --image gcr.io/YOUR_PROJECT_ID/streamlit-cohort-analysis \
  --platform managed \
  --allow-unauthenticated \
  --region us-central1 \
  --project YOUR_PROJECT_ID \
  --cpu 1 \
  --memory 512Mi \
  --min-instances 0 \
  --max-instances 10
```

## Troubleshooting

- **Platform errors**: Ensure you're building for `linux/amd64` if using Mac with Apple Silicon
- **Authentication errors**: Run `gcloud auth login` and `gcloud auth configure-docker`
- **Permission errors**: Make sure you have the necessary IAM roles (Cloud Run Admin, Storage Admin)
- **Container Registry access**: Enable the Container Registry API in your GCP project

## Theme Configuration

This app uses a light theme configuration. To apply the theme:

1. Copy the contents of `.streamlit/theme.toml` into `.streamlit/config.toml`
2. If the `.streamlit` directory doesn't exist, create it first:
   ```bash
   mkdir -p .streamlit
   cp .streamlit/theme.toml .streamlit/config.toml
   ```

The theme configuration isn't automatically applied because `.streamlit/config.toml` is typically ignored in Git repositories.
