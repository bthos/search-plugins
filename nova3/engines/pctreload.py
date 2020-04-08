#VERSION: 1.00
#AUTHORS: Jose Lorenzo (josee.loren@gmail.com)

from helpers import download_file, retrieve_url, headers
from novaprinter import prettyPrinter
import re
import json
import urllib.error
import urllib.parse
import urllib.request

class pctreload(object):
    url = 'https://pctreload.com'
    name = 'PCTReload'

    def do_post(self, full_url, what):
        query_args = {'s': what, 'pg': self.pg}
        encoded_args = urllib.parse.urlencode(query_args).encode('ascii')
        req = urllib.request.Request(full_url, data=encoded_args, headers=headers)
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
            self.pg = self.pg + 1
            return the_page
            
    def get_torrent(self, m):
        name = m.split("/")[4].split('.')[0]
        link = self.url+"/descargar-torrent/"+name
        
        item = {}
        item['seeds'] = '-1'
        item['leech'] = '-1'
        item['name'] = name
        item['size'] = self.size
        item['link'] = link
        item['engine_url'] = self.url
        item['desc_link'] = link

        prettyPrinter(item)
    
    def search(self, what, cat='all'):
        self.pg = 1
            
        while self.pg > 0:
            json_data = self.do_post(self.url+'/get/result/', what)
            torrents = json.loads(json_data)['data']['torrents']
            
            for k, v in torrents.items():
                if v == None:
                    return
                for k2, v2 in v.items():
                    for k3, v3 in v2.items():
                        if k3 == 'torrentSize':
                            self.size = v3
                        if k3 == 'imagen':
                            self.get_torrent(v3)
                            
            self.pg = self.pg + 1