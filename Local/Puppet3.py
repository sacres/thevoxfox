import logging
import datetime
from Legobot.Lego import Lego

logger = logging.getLogger(__name__)

class Puppet3(Lego):
    def listening_for(self, message):
        cmds = ['!puppet3', '!rnelson0']
        return message['text'].split()[0] in cmds

    def handle(self, message):
        opts = None
        logger.info(message)
        try:
            target = message['metadata']['source_channel']
            opts = {'target':target}
        except IndexError:
            logger.error('Could not identify message source in message: %s' % str(message))
        eol = datetime.datetime(2016, 12, 31)
        now = datetime.datetime.now()
        delta = eol - now
        days = delta.days
        if days > 0:
            txt = "Puppet 3 is End of Life in %s Days" % days
        else:
            txt = "Puppet 3 is End of Life! Fly you fools!"
        self.reply(message, txt, opts)


    def get_name(self):
        return 'puppet3'

    def get_help(self):
        help_text = "Get the number of days till puppet3 is EOL. Usage: " \
                    "!puppet3 "
        return help_text
