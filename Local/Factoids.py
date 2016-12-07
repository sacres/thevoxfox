import logging
from Legobot.Lego import Lego

logger = logging.getLogger(__name__)

class Factoids(Lego):
    def listening_for(self, message):
        cmds = ['!shrug', '!tableflip', '!nope', '!doit', '!wat', '!@', '!source', '!deal', '!awesome', '!nuke', '!stats']
        return message['text'].split()[0] in cmds

    def handle(self, message):
        opts = None
        logger.info(message)
        try:
            target = message['metadata']['source_channel']
            opts = {'target':target}
        except IndexError:
            logger.error('Could not identify message source in message: %s' % str(message))
        command = message['text'].split()[0]
        if command == '!shrug':
            txt = '¯\_(ツ)_/¯'
        elif command == '!tableflip':
            txt = '(╯°O°）╯︵ ┻━┻'
        elif command == '!nope':
            txt = 'https://p.bastelfreak.de/Pfkh/'
        elif command == '!doit':
            txt = 'Dooooooooo eeeeeeeettttttttt'
        elif command == '!wat':
            txt = 'https://p.bastelfreak.de/1gxL/'
        elif command == '!@':
            txt = 'IRC is not Twitter – please do not use @name to address people. use name,' \
            ' or name: instead. Using @ also prevents you from tab-completing nicks in your IRC client'
        elif command == '!source':
            txt = "You can find me on: 'https://github.com/voxpupuli/thevoxfox'"
        elif command == '!deal':
            txt = 'https://p.bastelfreak.de/dQ4S/'
        elif command == '!awesome':
            txt = 'https://p.bastelfreak.de/tgnla/'
        elif command == '!nuke':
            txt = 'https://p.bastelfreak.de/1MQ/'
        elif command == '!stats':
            txt = 'http://voxpupuli.bastelfreak.de/'
        self.reply(message, txt, opts)


    def get_name(self):
        return 'factoids'

    def get_help(self):
        help_text = "collection of nice factoids (static reponses). " \
                "Usage: !shrug, !tableflip, !nope, !doit, !wat, !@, !source, !deal, !awesome, !nuke, !stats "
        return help_text
