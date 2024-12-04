FROM python:3.9.19-alpine3.19
WORKDIR /app
COPY . .
RUN pip install -r task2_requirements.txt
ENV PYTHONUNBUFFERED=1
CMD ["python", "task2.py"]