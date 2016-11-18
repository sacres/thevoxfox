### Installation

#### Local

`pip3 install -r ./requirements.txt`

#### venv

Coming soon

### Running

If you decide to do this in Docker, local installation is not necessary.

#### Docker

`./run.sh SomeLocalContainerName` will start a local python:3 container, mount the repo into /usr/src/legobot, install deps, and then run the chatbot.py script.

#### Local

`pip3 install -r ./requirements.txt && python3 ./chatbot.py`

### Setting configuration

Use the config.ini to provide settings to the chatbot.py script

### Developing Plugins

See [this link](https://github.com/bbriggs/Legobot/blob/develop/docs/writing-a-lego.md)
