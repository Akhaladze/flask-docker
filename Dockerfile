FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install the Python dependencies
COPY requirements.txt .
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code to the working directory


# Set environment variables
#ENV FLASK_ENV=production
#ENV FLASK_ENV=development
#ENV FLASK_APP=iot.py
#ENV DEBUG=1

# Volume for code changes
VOLUME /app

# Expose port
#EXPOSE 5030

# Run Flask using WSGI server (gunicorn) with web configuration options
#CMD ["gunicorn", "--workers=4", "--threads=2", "--bind=0.0.0.0:5353", "app:app"]
#CMD ["flask -A app run -h 0.0.0.0 -p 5030"]
