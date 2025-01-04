FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 

COPY app ./
EXPOSE 8000

ENTRYPOINT ["fastapi", "run", "main.py"]




