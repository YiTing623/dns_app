FROM python:3.8

WORKDIR /app

COPY /path/to/your/US_Docker/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY us.py ./

EXPOSE 8080

CMD ["python", "us.py"]

