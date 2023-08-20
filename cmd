docker run -d --rm --name emqx -e DEV_LISTENERS__TCP__DEFAULT__BIND=1883 -p 18083:18083 -p 1883:1883 emqx:latest

docker network create mongo

docker run -d --rm --name mongo-server \
--net=mongo \
-p 27017:27017 \
-e MONGO_INITDB_ROOT_USERNAME=root \
-e MONGO_INITDB_ROOT_PASSWORD=pass \
mongo:latest

docker run -d --name mongo-exp \
--net=mongo \
--restart=always \
-p 8081:8081 \
-e ME_CONFIG_MONGODB_ADMINUSERNAME=root \
-e ME_CONFIG_MONGODB_ADMINPASSWORD=pass \
-e ME_CONFIG_MONGODB_SERVER="127.0.0.1" \
mongo-express:latest

