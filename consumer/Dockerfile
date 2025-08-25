FROM python:3.12-slim
WORKDIR /app
COPY /app /app/
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "consume.py"]
