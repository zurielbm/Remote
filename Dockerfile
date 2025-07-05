# Use Python 3.13 alpine image
FROM python:3.13-alpine

WORKDIR /app

COPY server.py /app/
COPY static/ /app/static/

RUN pip install --no-cache-dir flask requests

EXPOSE 80

# Run Flask app
CMD ["python3", "server.py"]
