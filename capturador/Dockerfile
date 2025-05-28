FROM python:3.12.3
WORKDIR /capturador
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "capturador.py"]



