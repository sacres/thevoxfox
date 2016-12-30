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
        # EOL is end of day on 31 Dec
        eol = datetime.datetime(2016, 12, 31,hour=23,minute=59)
        now = datetime.datetime.now()
        if now > eol:
            txt = "Puppet 3 is End of Life! Fly you fools!"
        else:
            delta = eol - now
            days = delta.days
            hours = delta.seconds//3600
            if days > 0:
                txt = "Puppet 3 is End of Life in %s days" % days
            else:
                txt = "Puppet 3 is End of Life in %s hours. Maybe make it a New Year's resolution?" % hours
        self.reply(message, txt, opts)


    def get_name(self):
        return 'puppet3'

    def get_help(self):
        help_text = "Get the number of days till puppet3 is EOL. Usage: " \
                    "!puppet3 "
        return help_text
