import logging
from Legobot.Lego import Lego

logger = logging.getLogger(__name__)


FACTOIDS = {
    '!shrug': r'¯\_(ツ)_/¯',
    '!tableflip': '(╯°O°）╯︵ ┻━┻',
    '!nope': 'https://p.bastelfreak.de/Pfkh/',
    '!doit': 'Dooooooooo eeeeeeeettttttttt',
    '!wat': 'https://p.bastelfreak.de/1gxL/',
    '!@': 'IRC is not Twitter – please do not use @name to address people. use name, or name: ' \
            'instead. Using @ also prevents you from tab-completing nicks in your IRC client',
    '!source': "You can find me on: 'https://github.com/voxpupuli/thevoxfox'",
    '!deal': 'https://p.bastelfreak.de/dQ4S/',
    '!awesome': 'https://p.bastelfreak.de/tgnla/',
    '!nuke': 'https://p.bastelfreak.de/1MQ/',
    '!stats': 'http://voxpupuli.bastelfreak.de/',
    '!docs': 'https://voxpupuli.org/docs/',
    '!http': 'Please supply the full URL! Some of us are lazy',
    '!no': 'https://blag.esotericsystems.at/igor/says/no',
    '!dog': 'https://p.bastelfreak.de/xtI/',
    '!cat': 'https://p.bastelfreak.de/vi6f05/',
    '!aww': 'https://p.bastelfreak.de/vi6f05/',
    '!awww': 'https://p.bastelfreak.de/vi6f05/',
    '!please': 'https://p.bastelfreak.de/vi6f05/',
    '!dance': "^('-')^ ^('-')^ v('-')v v('-')v <('-'<) (>'-')> <('-'<) (>'-')>",
    '!slowclap': 'https://p.bastelfreak.de/yVB9/',
    '!eyeballs': 'http://i2.kym-cdn.com/photos/images/original/000/282/317/50d.png',
}

class Factoids(Lego):
    """Class to hold all factoids
    Args: Lego
    """

    def listening_for(self, message):
        """Checks if the message contains a command that we need to execute
        Args:
            self:
            message: The complete line/message that comes from an IRC channel

        Returns:
            Bool: Returns true if the first word in the message is a command for this class
        """
        return message['text'].split()[0] in FACTOIDS

    def handle(self, message):
        """Execute the needed command
        Args:
            self:
            message: The complete line/message that comes from an IRC channel

        Returns:
            string: Returns the suitable factoid"""
        opts = None
        logger.info(message)
        try:
            target = message['metadata']['source_channel']
            opts = {'target':target}
        except IndexError:
            logger.error('Could not identify message source in message: %s', message)
        command = message['text'].split()[0]
        try:
            txt = FACTOIDS[command]
        except KeyError:
            logger.error('Failed to find factoid %s', command)
        else:
            self.reply(message, txt, opts)

    def get_name(self):
        """Returns the name of this class
        Args:
            self:

        Returns:
            string: The name of this class
        """
        return 'factoids'

    def get_help(self):
        """Prints a useful help message into the channel

        Args:
            self:

        Returns:
            String: A help message that explains this class
        """
        help_text = "collection of nice factoids (static reponses). " \
                "Usage: " + sorted(FACTOIDS.keys()).join(', ')
        return help_text
