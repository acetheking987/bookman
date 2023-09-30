FROM python:alpine
COPY ./src /app
COPY requirements.txt /app/requirements.txt
COPY ./.env /app/.env
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 27018
CMD ["python", "main.py"]