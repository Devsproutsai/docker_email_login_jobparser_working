# Use an official Selenium base image with Chrome
FROM selenium/standalone-chrome:latest

# Set the working directory to /app
WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python and pip dependencies
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --trusted-host pypi.python.org -r requirements.txt

# Change the permissions of the /app directory to allow writing
RUN chmod -R a+w /app

# Switch back to the selenium user
USER seluser

# Copy the entire local directory contents into the container at /app
COPY . .

# Change the ownership of the /app directory to seluser
RUN sudo chown -R seluser:seluser /app

# Run the tests and send email
CMD ["sh", "-c", "pytest test_files/*.py --json=report.json; python3 send_email.py"]
