import requests
import logging
from Legobot.Lego import Lego

logger = logging.getLogger(__name__)
base_url = 'https://raw.githubusercontent.com/voxpupuli/'

class Audit(Lego):
    def listening_for(self, message):
        return message['text'].split()[0] == '!msync'

    def handle(self,message):
        try:
            target = message['metadata']['source_channel']
            opts = {'target':target}
        except IndexError:
            logger.error('Could not identify message source in message: %s' % str(message))
        arg = self.parse_args(message)

        if arg == None:
            response = self.get_current_msync()
            self.reply(message, response)

        elif arg == "getver":
            try:
                modname = message['text'].split()[2]
                response = self.get_single_version(modname)
                self.reply(message,response)
            except Exception as e:
                self.reply(message, "womp womp :/ unable to get version.", opts)
                logger.exception('Caught exception in !msync:' + str(e))
        return

    def get_name(self):
        return 'msync'

    def get_help(self):
        return 'Discover information about the status of modulesync on managed repositories. Usage: !msync [getver modulename].'

    def get_current_msync(self):
        try:
            msync_version = requests.get("%smodulesync_config/master/moduleroot/.msync.yml" % base_url)
            msync_version = msync_version.text
            return msync_version.strip()
        except Exception as e:
            logger.exception('Caught exception in !msync:' + e)
            return "Unable to fetch latest msync version."


    def get_single_version(self,modname):
        try:
            msync_ver = requests.get(base_url + modname + '/master/.msync.yml')
            msync_ver = msync_ver.text
            return msync_ver.strip('\n')
        except:
            return 'Could not find a module to query :/'

    def parse_args(self,message):
        arg = None
        if len(message['text'].split()) == 1:
            # No args supplied
            arg = None
        elif len(message['text'].split()) > 1:
            arg = message['text'].split()[1]
        return arg
