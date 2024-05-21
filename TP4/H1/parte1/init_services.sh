# Levantar Redis en docker:
docker rm -f redis-stack && docker run -d --rm --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

# Levantar RabbitMQ en docker:
docker rm -f rabbitmq && docker run -d -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management