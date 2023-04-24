FROM python:3.10

EXPOSE 8090

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "mock_json_flask.py"]
