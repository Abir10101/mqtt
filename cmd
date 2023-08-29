docker run -d --rm --name emqx -e DEV_LISTENERS__TCP__DEFAULT__BIND=1883 -p 18083:18083 -p 1883:1883 emqx:latest
docker network create rnetwork
docker run --name rserver --network rnetwork -d -v redisData:/data -p 6379:6379 redis redis-server --save 60 1 --loglevel warning
docker run -it --network mqtt_mqttApp --rm --name rclient redis:alpine3.18 redis-cli -h redis-server

docker-compose start redis-client
docker-compose start publisher
