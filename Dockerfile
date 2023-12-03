# Use the official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

RUN curl -fsSLO https://get.docker.com/builds/Linux/x86_64/docker-17.04.0-ce.tgz \
  && tar xzvf docker-17.04.0-ce.tgz \
  && mv docker/docker /usr/local/bin \
  && rm -r docker docker-17.04.0-ce.tgz
# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 5200


# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "API:app", "--host", "0.0.0.0", "--port", "5200"]
