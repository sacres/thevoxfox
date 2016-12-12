import requests
from Legobot.Lego import Lego
import logging

logger = logging.getLogger(__name__)

class lmgtfy(Lego):
    def listening_for(self, message):
        return message['text'].split()[0] == '!g'

    def handle(self, message):
        try:
            target = message['metadata']['source_channel']
            opts = {'target':target}
        except IndexError:
            logger.error('Could not identify message source in message: %s' % str(message))
        base_url = 'https://lmgtfy.com/?q='
        search_params = ' '.join(message['text'].split()[1:])
        if not search_params:
            self.reply(message, "You need to enter a search string ... ", opts)
            return
        else:
            r = requests.get(base_url + search_params)
        if r.status_code == 200:
            self.reply(message, r.url, opts)
        else:
            self.reply(message, "Google unreachable, I could not Google for You. Sorry.", opts)

    def get_name(self):
        return 'lmgtfy'

    def get_help(self):
        help_text = "Let me Google that for you! " \
                "Usage: !g query"
        return help_text
