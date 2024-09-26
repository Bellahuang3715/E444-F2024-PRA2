FROM python:3.11.5

# set the container working directory
WORKDIR /app

# copy the requirements.txt into the container
COPY requirements.txt .

# install dependencies into the container
RUN pip install -r requirements.txt

# copy the entire project into the container
COPY . .

# set the environment variable
ENV FLASK_APP=hello.py

# command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]

# set the port number
EXPOSE 5000
