FROM python:3

EXPOSE 80

ENV READTHEDOCS True
RUN pip install picamera
RUN pip install flask

ENV PICAMERA_USER admin
ENV PICAMERA_PASSWORD admin

RUN mkdir -p /app

WORKDIR /app

COPY . /app

CMD ["python", "main.py"]