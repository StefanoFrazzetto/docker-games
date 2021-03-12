# Docker Game Servers

## Configuration

- Install Docker: you can find the instructions for 
   installing Docker on the [official website](https://docs.docker.com/get-docker/).
- Ensure you have [Python](https://www.python.org/downloads/) 3.x on your system by running `python --version`.

## Running a Game Server

1. Install this package
```shell
$ pip install docker-games
```
2. Create your server's configuration in a new Python file
3. Enjoy!

### Minecraft

```python
from docker_games import Minecraft

minecraft = Minecraft('creepers_go_boom', '2GB', '/home/stefano/mc_data')
minecraft.add_ports(25565, 25565)
minecraft.accept_license()  # <-- accept Minecraft's EULA
minecraft.online_mode()     # <-- server checks connecting players against Minecraft account database

minecraft.start()
```

Docker image: https://hub.docker.com/r/itzg/minecraft-server

### Factorio

```python
from docker_games import Factorio

factorio = Factorio('flying_robots', '/home/stefano/factorio_data')
factorio.add_ports(34197, '34197/udp')
factorio.add_ports(27015, '27015/tcp')

factorio.start()
```

Docker image: https://hub.docker.com/r/factoriotools/factorio

### TeamSpeak

```python
from docker_games import TeamSpeak

teamspeak = TeamSpeak('tsserver', '/tmp/ts_data')
teamspeak.add_ports(9987, '9987/udp')
teamspeak.add_ports(10011, 10011)
teamspeak.add_ports(30033, 30033)
teamspeak.accept_license()  # <-- accept TeamSpeak's license

teamspeak.start()
```

Docker image: https://hub.docker.com/_/teamspeak 

## Contributing

Contributions are very welcome!

If you want to improve this project, or add more server, fork the repo and submit a pull request.
