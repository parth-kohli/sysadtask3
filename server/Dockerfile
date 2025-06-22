FROM python:3.11-slim
WORKDIR /app
COPY server.py db.py ./
RUN pip install mysql-connector-python
CMD ["python", "server.py"]
