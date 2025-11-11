# Step 1: Use an official Python base image
FROM python:3.9-slim

# Step 2: Set working directory
WORKDIR /app

# Step 3: Copy app code into container
COPY . .

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose Flask default port
EXPOSE 5000

# Step 6: Run the Flask app
CMD ["python3", "app.py"]
