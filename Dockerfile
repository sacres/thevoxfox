FROM python:3

ADD . /usr/src/legobot 
WORKDIR /usr/src/legobot
RUN pip install -r /usr/src/legobot/requirements.txt
ENTRYPOINT python ./chatbot.py
