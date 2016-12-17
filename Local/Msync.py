import requests
import logging
import semver
from Legobot.Lego import Lego

logger = logging.getLogger(__name__)
api_url = 'https://api.github.com/'
raw_url = 'https://raw.githubusercontent.com/voxpupuli/'

class Audit(Lego):
    def listening_for(self, message):
        return message['text'].split()[0] == '!msync'

    def handle(self,message):
        try:
            target = message['metadata']['source_channel']
            opts = {'target':target}
        except IndexError:
            logger.error('Could not identify message source in message: {0!s}'.format(str(message)))
        arg = self.parse_args(message)

        if arg == None:
            response = self.get_current_msync()
            self.reply(message, response, opts)

        elif arg == "getver":
            modname = None
            try:
                modname = message['text'].split()[2]
            except IndexError:
                self.reply(message, "Could not find a module name in your request.", opts)

            if modname == None:
                self.reply(message,self.get_help(),opts)
            else:
                response = self.get_single_version(modname)
                self.reply(message,response,opts)
        return

    def get_name(self):
        return 'msync'

    def get_help(self):
        return 'Discover information about the status of modulesync on managed\
 repositories. Usage: !msync [getver modulename].'

    def get_current_msync(self):
        try:
            msync_tags = requests.get("{0!s}repos/voxpupuli/modulesync_config/tags".format(api_url))
            if msync_tags.status_code == requests.codes.ok:
                releases = msync_tags.json()
                latest_release = self._compare_semver(releases)
                return latest_release
            else:
                return "Something happened, boss. Got a {0!s} ".format( \
                    str(msync_tags.status_code))
        except Exception as e:
            logger.exception('Caught exception in !msync:' + str(e))
            return "Unable to fetch latest msync version."


    def get_single_version(self,modname):
        try:
            msync_ver = requests.get(raw_url + modname + '/master/.msync.yml')
            msync_ver = msync_ver.text
            return "{0!s} {1!s} ".format(modname, msync_ver.strip('\n'))
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

    def _compare_semver(self,releases):
        latest = '0.0.0'
        for release in releases:
            logger.debug('Comparing: {0!s} and {1!s}'.format(latest, release['name']))
            if semver.compare(latest,release['name']) == -1:
                latest = str(release['name'])
                logger.debug('Found a newer release: {0!s}'.format(latest))
        return latest
