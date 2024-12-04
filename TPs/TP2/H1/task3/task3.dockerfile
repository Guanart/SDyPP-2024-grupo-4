FROM python:3.9.19-alpine3.19
WORKDIR /app
COPY . .
RUN pip install -r task3_requirements.txt
ENV PYTHONUNBUFFERED=1
CMD ["python", "task3.py"]