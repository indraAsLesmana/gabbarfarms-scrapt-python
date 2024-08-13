# Use the official Ubuntu image as the base image
FROM ubuntu:20.04

# Update the package list and install Python
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./gabbarfarmsapi.py /app/
COPY ./dbconnection.py /app/
COPY ./main.py /app/
COPY ./config.py /app/

# Define environment variable
# ENV NAME PythonDocker

# Copy your Python script and requirements file into the container
COPY ./requirements.txt /app/

# Expose the port on which your Flask application will run
EXPOSE 5500

# Install Python dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt

# Run a Python script
CMD ["python3", "gabbarfarmsapi.py"]
