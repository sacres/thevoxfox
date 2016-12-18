import random
import re
import logging

import requests

from Legobot.Message import Message,Metadata
from Legobot.Lego import Lego

logger = logging.getLogger(__name__)

class BingImageSearch(Lego):
    def __init__(self, baseplate, lock):
        super().__init__(baseplate, lock)
        self.user_agent = "Mozilla/4.0 (compatible; MSIE 7.0; " \
                          "Windows NT 5.1; Trident/4.0; FDM; " \
                          ".NET CLR 2.0.50727; " \
                          "InfoPath.2; .NET CLR 1.1.4322)"

    def listening_for(self, message):
        return message['text'].split()[0] == '!img'

    def handle(self, message):
        try:
            target = message['metadata']['source_channel']
            opts = {'target':target}
        except IndexError:
            logger.error('Could not identify message source in message: {0!s}'.format(str(message)))
        query = ' '.join(message['text'].split()[1:])
        query = query.replace(' ', '%20')
        req_url = self._make_url(query)
        response = requests.get(req_url)
        urls = []
        url_regex = '"https?://[^"]*\.(jpg|jpeg|png|gif|gifv)"'
        for url in re.finditer(url_regex, response.text):
            urls += [url.group(0).strip('"')]
        if len(urls) == 0:
            url = 'Nothing found :('
        else:
            url = random.choice(urls) # nosec

        metadata = Metadata(source=self).__dict__
        metadata['opts'] = opts
        message = Message(text=str(url), metadata=metadata).__dict__
        self.baseplate.tell(message)

    def _make_url(self, query):
        req_url = 'http://www.bing.com/images/search'
        req_url += '?q=' + query
        req_url += '&safesearch=on'
        return req_url

    def get_name(self):
        return 'img'

    def get_help(self):
        help_text = "Search Bing for a random image. " \
                    "Safesearch is enabled, but you have been warned. " \
                    "Usage: !img <search string>"
        return help_text
