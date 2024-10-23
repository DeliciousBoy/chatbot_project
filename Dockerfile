FROM python:3.11.9

# Set the working directory inside the container
WORKDIR /app

# Copy all project files to the /app directory inside the container
# COPY . /app
COPY ./src /app/src
COPY ./data /app/data
COPY ./logs /app/logs
COPY .env /app/
COPY config.yaml /app/
COPY requirements.txt /app/
COPY pyproject.toml /app/
COPY setup.cfg /app/
COPY README.md /app/

# Install required dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Add dependencies for Chrome to work in Docker
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    libgconf-2-4 \
    libx11-6 \
    libxcb1 \
    libnss3 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libxrandr2 \
    libxss1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    libgbm1 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

CMD ["python", "src/scraping/main.py"]