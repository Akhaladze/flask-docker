FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install the Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code to the working directory
COPY . .

# Set environment variables
ENV FLASK_ENV=production
ENV FLASK_APP=your_flask_app.py

# Volume for code changes
VOLUME /app

# Expose port
EXPOSE 5000

# Run Flask using WSGI server (gunicorn) with web configuration options
CMD ["gunicorn", "--workers=4", "--threads=2", "--bind=0.0.0.0:5000", "your_flask_app:app"]
