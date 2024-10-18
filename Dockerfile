FROM python:3.11.9

# Set the working directory inside the container
WORKDIR /app

# Copy all project files to the /app directory inside the container
COPY . /app

# Install required dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install cron (to schedule tasks)
RUN apt-get update && apt-get install -y cron

# Copy the cron job configuration file to the cron.d directory
COPY  cronjob /etc/cron.d/scrape-cron

# Set permissions for the cron job file
RUN chmod 0644 /etc/cron.d/scrape-cron

# Register the cron job and ensure logs are output to stdout
RUN crontab /etc/cron.d/scrape-cron

# Create a log file for cron output
RUN touch /var/log/cron

# Command to start cron service and keep the container running by tailing the cron log file
CMD cron && tail -f /var/log/cron.log

