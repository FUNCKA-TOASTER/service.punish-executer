# ⚙️ TOASTER.PUNISH-EXECUTION-SERVICE

![main_img](https://github.com/STALCRAFT-FUNCKA/toaster.message-handling-service/assets/76991612/8bb6b3bf-8385-4d4b-80cc-e104d5283a9c)

Вся документирующая информация продублированна внутри кода на английском языке.<br>
All documenting information is duplicated within the code in English.<br>

## 📄 Информация
**TOASTER.PUNISH-EXECUTION-SERVICE** - сервис обработки событий, классифицированных как "запрос на предупреждение". Событие приходит от сервиса обработки команд или сервиса обработки сообщений. Праллельно производятся необходимые действия внутреннего\внешнего логирования.

### Входные данные:
Warn Event:
```
{
  "author_id": 1111,
  "author_name": "SampleName",
  "reason_message": "text",
  "setting": "SampleName",
  "target_id": 1111,
  "target_name": "SampleName",
  "peer_id": 1111,
  "peer_name": "SampleName",
  "cmid": 1111,
  "warn_count": 5,
  "target_message_cmid": 1111,
}
```
Пример события, которое приходит от toaster.command-handling-service или toaster.message-handling-service сервера на toaster.punish-execution-service.

Далее, сервиc выносит предупреждения, манипулирую с данными в БД и отправляет запрос на уведомление в лог-чаты.

### Дополнительно
Docker stup:
```
docker network
    name: TOASTER
    ip_gateway: 172.18.0.1
    subnet: 172.18.0.0/16
    driver: bridge


docker image
    name: toaster.punish-execution-service
    args:
        TOKEN: "..."
        GROUPID: "..."
        SQL_HOST: "..."
        SQL_PORT: "..."
        SQL_USER: "..."
        SQL_PSWD: "..."


docker container
    name: toaster.punish-execution-service
    network_ip: 172.1.08.9

docker volumes:
    /var/log/TOASTER/toaster.punish-execution-service:/service/logs
```

Jenkins shell command:
```
imageName="toaster.punish-execution-service"
containerName="toaster.punish-execution-service"
localIP="172.18.0.9"
networkName="TOASTER"

#stop and remove old container
docker stop $containerName || true && docker rm -f $containerName || true

#remove old image
docker image rm $imageName || true

#build new image
docker build . -t $imageName \
--build-arg TOKEN=$TOKEN \
--build-arg GROUPID=$GROUPID \
--build-arg SQL_HOST=$SQL_HOST \
--build-arg SQL_PORT=$SQL_PORT \
--build-arg SQL_USER=$SQL_USER \
--build-arg SQL_PSWD=$SQL_PSWD

#run container
docker run -d \
--name $containerName \
--volume /var/log/TOASTER/$imageName:/service/logs \
--restart always \
$imageName

#network setup
docker network connect --ip $localIP $networkName $containerName

#clear chaches
docker system prune -f
```
