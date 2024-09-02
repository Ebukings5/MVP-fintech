# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /mvp-fintech

# Copy the current directory contents into the container at /mvp-fintech
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy wait-for-it.sh to the working directory
COPY wait-for-it.sh /mvp-fintech/wait-for-it.sh
RUN chmod +x /mvp-fintech/wait-for-it.sh

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]