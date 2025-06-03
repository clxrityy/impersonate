# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.13-alpine

# Update system packages to reduce vulnerabilities
RUN apk update && apk upgrade && apk add --no-cache gcc musl-dev


# Keeps Python from writing pyc files to disc (which avoids filling up the container)
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
# Install any additional dependencies here
# Copy the current directory contents into the container at /bot
# and set the working directory to /bot
COPY . /bot
WORKDIR /bot

# Creates a non-root user with an explicit UID and adds permission to access the /bot directory
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN pwd && \
    adduser -u 1063 --disabled-password --gecos "" botuser && chown -R botuser /bot
USER botuser

# During debugging, this entry point will be overridden
# For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "main.py"]