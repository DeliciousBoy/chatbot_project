FROM python:3.11.9

WORKDIR /app

COPY requirments.txt .

RUN pip install --no-cache-dir -r requirments.txt

COPY . .

CMD ["python", "scraping/main.py"]

