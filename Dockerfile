FROM python:3.8.2

# Set up working directory
WORKDIR /app

# Install required packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app/src/"
COPY src ./src

ENTRYPOINT ["python", "/app/src/main.py"]