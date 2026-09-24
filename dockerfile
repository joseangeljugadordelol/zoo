
FROM python:3.14


WORKDIR /app





COPY . .



RUN pip install -r requirement.txt


CMD ("python", "app.py")