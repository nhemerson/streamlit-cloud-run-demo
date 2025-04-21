FROM python:3.9-slim

WORKDIR /app

# Install Astral UV
RUN pip install --no-cache-dir uv

# Create a virtual environment
RUN uv venv .venv

# Copy requirements first for better caching
COPY requirements.txt .

# Use Astral UV with the virtual environment
RUN . .venv/bin/activate && uv pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port that Cloud Run will use
EXPOSE 8080

# Set default port for local development
ENV DEV_PORT=8501

# Cloud Run will set the PORT environment variable
# Set Streamlit to run using the virtual environment
CMD . .venv/bin/activate && \
    if [ "$DEV_MODE" = "true" ]; then \
        streamlit run Home.py --server.port=$DEV_PORT --server.address=0.0.0.0; \
    else \
        streamlit run Home.py --server.port=$PORT --server.address=0.0.0.0; \
    fi 