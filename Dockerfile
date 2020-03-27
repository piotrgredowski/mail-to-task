FROM python:3.8.2-slim

WORKDIR /dependencies

# Install dependencies
COPY requirements.txt /dependencies
RUN pip3 install -r requirements.txt

# ONLY FOR DEVELOPMENT
COPY requirements-dev.txt /dependencies
RUN pip3 install -r requirements-dev.txt

# Copy whole current directory
WORKDIR /app
COPY ./ /app

# Expose port of application
EXPOSE 8191

CMD python -m mail_to_task.__init__