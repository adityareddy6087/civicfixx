FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Set environment defaults
ENV PORT=8000
ENV DEMO_MODE=true

EXPOSE 8000

CMD ["python", "run.py"]
