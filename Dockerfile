FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["/usr/local/bin/python3.13"]
ENV PYTHONUNBUFFERED=1
CMD ["/app/main.py"]