#VERSION: 1.01
#AUTHORS: Jose Lorenzo (josee.loren@gmail.com)

from helpers import download_file, headers
from novaprinter import prettyPrinter
import re
import json
import urllib.error
import urllib.parse
import urllib.request
try:
    #python3
    from html.parser import HTMLParser
except ImportError:
    #python2
    from HTMLParser import HTMLParser

class pctfenix(object):
    url = 'https://pctfenix.com/'
    name = 'PCTFenix'
    size = ""
    count = 1
    list = [] 
    
    class HTMLParser1(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == 'a':
                Dict = dict(attrs)
                pctfenix.get_torrent_core(self, Dict["href"])

    def retrieve_url(self, url):
        req = urllib.request.Request(url, headers=headers)
        try:
            response = urllib.request.urlopen(req)
            dat = response.read()
            response.close()
            return dat
        except urllib.error.URLError as errno:
            response.close()
            return ""
        return ""

    def do_post(self, full_url, what):
        query_args = {'s': what}
        encoded_args = urllib.parse.urlencode(query_args).encode('ascii')
        req = urllib.request.Request(full_url, data=encoded_args, headers=headers)
        req2 = urllib.request.urlopen(req)
        with req2 as response:
            the_page = response.read()
            req2.close()
            return the_page
        req2.close()
            
    def montar_torrent(self, link):
        name = link.split("/")[-1].split(".")[0]
        
        item = {}
        item['seeds'] = '-1'
        item['leech'] = '-1'
        item['name'] = name
        item['size'] = '-1'
        item['link'] = link
        item['engine_url'] = pctfenix.url
        item['desc_link'] = link

        print(item)
        prettyPrinter(item)
        pctfenix.count = pctfenix.count + 1
        
    def get_torrent_core(self, link):
        if link not in pctfenix.list: 
            pctfenix.list.append(link) 
        else:
            return
        html_virgen = pctfenix.retrieve_url(self, pctfenix.url + link[1:])
        html_virgen = str(html_virgen)
        texto = "id=\"btn-download-torrent\" data-ut=\""
        idx = html_virgen.find(texto)
        
        html = html_virgen[idx:]
        
        html = html[len(texto):]
        html = "https:" + html[:html.find("\"")]
        pctfenix.montar_torrent(self,html)
        
    def search(self, what, cat='all'):
        what = what.replace("%20", " ")
        html = self.do_post(self.url+'/controllers/search-mini.php', what)
        parser = pctfenix.HTMLParser1()
        parser.feed(str(html))
                        
                            
        
if __name__ == "__main__":
    m = pctfenix()
    m.search('greed')
