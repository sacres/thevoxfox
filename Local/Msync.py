import requests
import logging
import semver
import re
import json
from datetime import date
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
            self.opts = {'target':target}
            self.message = message
        except IndexError:
            logger.error('Could not identify message source in message: %s' \
                         % str(message))

        # A python workaround for case statements
        dispatcher = {'getver':self._get_single_version,
                     'olderthan':self._compare_to_version,
                     'newerthan':self._compare_to_version,
                     'current':self._compare_to_version,
                     'version':self._get_current_msync}

        args = message['text'].split()
        if len(args) > 1:
            command = args[1]
        else:
            command = 'version'
        logger.debug('%s requested. Dispatching %s with args: %s' % (command,
                                                                     str(dispatcher[command]),
                                                                     str(args)))
        response = dispatcher[command](*args)
        # Returning things other than a str to chat really freaks legobot out.
        # Someone should fix that.
        self.reply(message,str(response),self.opts)

    def get_name(self):
        return 'msync'

    def get_help(self):
        return 'Discover information about the status of modulesync on managed '\
                'repositories. Usage: !msync. Fore more info, see the docs at '\
                'https://github.com/voxpupuli/thevoxfox/tree/master/docs/msync.md'

    def _get_current_msync(self,*args,**kwargs):
        try:
            msync_tags = requests.get("%srepos/voxpupuli/modulesync_config/tags" \
                                      % api_url)
            if msync_tags.status_code == requests.codes.ok:
                releases = msync_tags.json()
                latest_release = self._compare_semver(releases)
                return latest_release
            else:
                return "Something happened, boss. Got a %s " % \
                    str(msync_tags.status_code)
        except Exception as e:
            logger.exception('Caught exception in !msync:' + str(e))
            return "Unable to fetch latest msync version."

    def _get_all_modules(self):
        try:
            slug = 'modulesync_config/master/managed_modules.yml'
            all_modules = requests.get(raw_url + slug)
            if all_modules.status_code == requests.codes.ok:
                yaml_artifacts = ['---','- ','','...','# vim: syntax=yaml']
                modules = all_modules.text
                modules = modules.split('\n')
                modules = [module.strip() for module in modules]
                modules = [module for module in modules if \
                           module not in yaml_artifacts]
                modules = [module[2:] for module in modules]
                return modules
        except:
            logger.error('Unable to reach modulesync_config repo!')
            # Helllooooooo antipattern!
            return ['']

    def _compare_semver(self,releases):
        latest = '0.0.0'
        for release in releases:
            logger.debug('Comparing: %s and %s' % (latest,release['name']))
            if semver.compare(latest,release['name']) == -1:
                latest = str(release['name'])
                logger.debug('Found a newer release: %s' % latest)
        return latest

    def _compare_to_version(self,*args,**kwargs):
        try:
            status = args[1]
        except IndexError:
            logger.error('msync._compare_to_version() called '\
                         'without enough arguments!')
            return "Not enough arguments!"

        # Now the fun begins
        working_prompt = 'Fetching and comparing against all our modules. '\
                'This takes a second...'
        self.reply(self.message,str(working_prompt),self.opts)
        all_modules = self._get_all_modules()
        matching_modules = []
        if status == 'current':
            current_msync = self._get_current_msync()
            for module in all_modules:
                # Use a requests Session to take advantage of connection pooling
                s = requests.Session()
                kwargs = {'module':module,'session':s}
                modver = self._get_single_version(**kwargs) # Workaround until **kwargs is ironed out
                # Sometimes we get 404s. ¯\_(ツ)_/¯
                if modver != False:
                    if semver.compare(modver,current_msync) == 0: # semvers matched
                        matching_modules.append(module)
            report_url = self._gist(matching_modules)
            return report_url

        elif status == 'olderthan' or status == 'newerthan':
            try:
                compare_version = args[2]
            except IndexError:
                logger.error("msync._compare_to_version() called with 'olderthan' or "\
                        "'newerthan' but no version provide to compare against...")
                return "Not enough arguments!"
            compare = {'olderthan': -1,'newerthan': 1}
            try:
                semver.parse(compare_version)
            except ValueError:
                return "Invalid semver"
            for module in all_modules:
                modver = self._get_single_version('','',module) # Workaround until **kwargs is worked out
                if modver != False:
                    comparison = semver.compare(modver,compare_version)
                    if comparison == compare[status] or comparison == 0:
                        matching_modules.append(module)

            report_url = self._gist(matching_modules)
            return report_url
        else:
            return 'How did you get here?'

    def _get_current_msync(self,*args,**kwargs):
        try:
            msync_tags = requests.get("%srepos/voxpupuli/modulesync_config/tags" \
                                        % api_url)
            if msync_tags.status_code == requests.codes.ok:
                releases = msync_tags.json()
                latest_release = self._compare_semver(releases)
                return latest_release
            else:
                return "Something happened, boss. Got a %s " % \
                    str(msync_tags.status_code)
        except Exception as e:
            logger.exception('Caught exception in !msync:' + str(e))
            return "Unable to fetch latest msync version."

    def _get_single_version(self,*args,**kwargs):
        # For the love of God, check for length!
        logger.debug(kwargs)
        if 'module' not in kwargs:
            try:
                module = args[2]
            except IndexError:
                logger.error('Not enough arguments supplied to _get_single_version()')
                return "Not enough arguments!"
        else: 
            module = kwargs['module']
        msync_ver = requests.get(raw_url + module + '/master/.msync.yml')
        if msync_ver.status_code == requests.codes.ok:
            msync_ver = msync_ver.text
            msync_ver = re.search('\d+\.\d+\.\d+', msync_ver)
            return msync_ver.group(0)
        else:
            logger.debug('Got a bad return code from module %s: %s' % (module,msync_ver.status_code))
            return '0.0.0'

    def _gist(self,text):
        # input is a list. we want one module per line
        timestamp = date.today()
        header = '# Report generated by TheVoxFox on %s' % timestamp.strftime("%A, %d %B %Y")
        text.insert(0,header) 
        text = '\n'.join(text)
        body = {'descrption':'Voxpupuli modulesync report',
                'files':{
                    'report.txt':{
                        'content': text
                    }
                }
                }
        r = requests.post('https://api.github.com/gists', json.dumps(body))
        logger.debug('_gist response code: %s' % r.status_code)
        r = r.json()
        logger.debug(r)
        if 'html_url' in r:
            return r['html_url']
        else:
            return "Unable to generate a gist at this time..."
