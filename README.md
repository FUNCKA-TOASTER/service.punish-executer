# ⚙️ SERVICE.PUNISHMENT-EXECUTER

![main_img](https://github.com/FUNCKA-TOASTER/service.punishment-executer/assets/76991612/8bb6b3bf-8385-4d4b-80cc-e104d5283a9c)

## 📄 Информация

**SERVICE.PUNISHMENT-EXECUTER** - сервис обработки событий, классифицированных как "warn", "unwarn", "kick", "delete".

### Входные данные

Warn Event:

```python
class Punishment:
    punishment_type: str
    comment: str
    cmids: Union[int, List[int]]
    bpid: int
    uuid: int
    points: Optional[int]
    mode: Optional[str]
```

Пример события, которое приходит на service.punishment-executer.

Далее, в зависимости от типа санкций, сервис выполняет действия предупреждения, кика или удаления сообщений.

### Дополнительно

Docker stup:

```shell
docker network
    name: TOASTER
    ip_gateway: 172.18.0.1
    subnet: 172.18.0.0/16
    driver: bridge


docker image
    name: service.punishment-executer
    args:
        TOKEN: "..."
        GROUPID: "..."
        SQL_HOST: "..."
        SQL_PORT: "..."
        SQL_USER: "..."
        SQL_PSWD: "..."


docker container
    name: service.punishment-executer
    network_ip: 172.1.08.9
```

Jenkins shell command:

```shell
imageName="service.punishment-executer"
containerName="service.punishment-executer"
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
--restart always \
$imageName

#network setup
docker network connect --ip $localIP $networkName $containerName

#clear chaches
docker system prune -f
```
