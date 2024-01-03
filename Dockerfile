FROM python:3.12.1-slim

#set the working directory
WORKDIR /app

#install dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

#copy the scripts to the forlder
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 8080

#start the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]