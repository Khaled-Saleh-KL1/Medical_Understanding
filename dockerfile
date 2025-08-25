# 1. Use an official, lightweight Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# 4. Install the dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 5. Copy your entire project (api, gui, src folders) into the container
COPY . .

# 6. Expose the port the app will run on
EXPOSE 80

# 7. Define the command to run your application
# IMPORTANT: VERIFY THIS LINE! 
# Adjust "api.main:app" to point to your FastAPI app instance.
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]