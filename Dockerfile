# Use a lightweight Python base image
FROM python:3.12-slim

# Install Node.js and npx
RUN apt-get update && apt-get install -y curl \
    && curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

RUN apt-get install -y --no-install-recommends \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /tds-project1

# Copy and install dependencies separately for better caching
COPY requirements.txt .
RUN pip install torch==2.3.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install sentence-transformers pytesseract
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose the FastAPI server port
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "hello:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]