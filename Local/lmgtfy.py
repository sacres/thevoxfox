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
        if len(message['text'].split()) > 1:
            query = ' '.join(message['text'].split()[1:])
            url = 'https://lmgtfy.com/?q=%s' % query
            self.reply(message, url, opts)
        else:
            self.reply(message, "You didn't give me anything to ask!", opts)

    def get_name(self):
        return 'lmgtfy'

    def get_help(self):
        help_text = "Let me Google that for you! " \
                    "Usage: !g query"
        return help_text
