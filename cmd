docker run -d --rm --name emqx -e DEV_LISTENERS__TCP__DEFAULT__BIND=1883 -p 18083:18083 -p 1883:1883 emqx:latest
docker run --name rserver -d -v redisData:/data redis redis-server --save 60 1 --loglevel warning