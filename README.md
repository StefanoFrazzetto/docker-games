# DockerGameServers

## Configuration

1. Install Docker: you can find the instructions for 
   installing Docker on the [official website](https://docs.docker.com/get-docker/)
2. Ensure you have [Python](https://www.python.org/downloads/) 3.x on your system, by running `python --version`

## Running Game Servers

1. Install this package
```shell
$ pip install docker-games
```
2. Create your server's configuration in a new Python file
```python
from docker_games import Minecraft

minecraft = Minecraft('my_minecraft_server', '1GB', '/tmp/mcserver')
minecraft.add_ports(25565, 25565)
minecraft.accept_license()  # <-- you accept Minecraft's EULA
minecraft.online_mode()     # <-- server checks connecting players against Minecraft account database

minecraft.start()
```
```text
* Minecraft is running... (Press CTRL+C to terminate)
```
3. Enjoy!

### Minecraft
Default port: 25565

Docker image: https://hub.docker.com/r/itzg/minecraft-server

### TeamSpeak
Default ports: 9987, 10011, 30033

Docker image: https://hub.docker.com/_/teamspeak 

## Contributing

Contributions are very welcome!

If you want to improve this project, or add more server, fork the repo and submit a pull request.
