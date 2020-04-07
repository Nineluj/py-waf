FROM python:3.8.2

# Set up working directory
WORKDIR /app

# Install required packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY run.py .
COPY src ./src

CMD ["python", "/app/run.py"]