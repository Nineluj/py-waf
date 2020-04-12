FROM python:slim

# Set up working directory
WORKDIR /app

# Install required packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app/src/"
COPY run.py ./run.py
COPY waf ./waf

ENTRYPOINT ["python", "/app/run.py"]