# The VoxFox

## Installation

We provide a basic config file, it is located at config.example.ini. Please rename it to config.ini

### Local

`pip3 install -r ./requirements.txt`

### venv

```bash
virtualenv --python=/usr/bin/python3 venv
source venv/bin/activate
pip3 install -r ./requirements.txt
```

## Running

If you decide to do this in Docker, local installation is not necessary.

### With Docker

`./run.sh SomeLocalContainerName` will start a local python:3 container, mount the repo into /usr/src/legobot, install deps, and then run the chatbot.py script.

### Without Docker

If you don't use virtualenv you can directly start the bot:

```bash
python3 chatbot.py
```

In case of virtualenv you first have to activate it:

```bash
source venv/bin/activate
python3 chatbot.py
```

### Setting configuration

Use the config.ini to provide settings to the chatbot.py script

### Developing Plugins

See [this link](https://github.com/bbriggs/Legobot/blob/develop/docs/writing-a-lego.md)
