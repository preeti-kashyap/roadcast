# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /roadcast
WORKDIR /roadcast

# Copy the current directory contents into the container at /roadcast
COPY . /roadcast

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME roadcast

# Run roadcast.py
