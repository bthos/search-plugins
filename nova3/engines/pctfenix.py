#VERSION: 1.1
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
                
    class HTMLParser2(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == 'div':
                Dict = dict(attrs)
                torrent_num = Dict["onclick"]
                torrent_num = torrent_num[torrent_num.find("(")+1:torrent_num.find(")")]
                pctfenix.modCap(self, torrent_num)

    class HTMLParser3(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == 'a':
                Dict = dict(attrs)
                if ".torrent" in Dict["href"]:
                    pctfenix.montar_torrent(self, "https:"+Dict["href"])

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
        encoded_args = urllib.parse.urlencode(what).encode('ascii')
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

        prettyPrinter(item)
        pctfenix.count = pctfenix.count + 1

    def modCap(self, id):
        s = {'id': id }
        html = pctfenix.do_post(pctfenix, pctfenix.url+'/controllers/show.chapters.php', s)
        parser = pctfenix.HTMLParser3()
        parser.feed(str(html))


    def loadDD(self, CNAME, CID, O):
        if O == "0":
            CIDR = "1469"
        elif O == "1":
            CIDR = "767"
        else:
            CIDR = "775"

        #CNAME = CNAME.replace(" ", "+")    
        s = {'_cname': CNAME, '_cid': CID ,'_cidr': CIDR ,'_o':O}
        html = pctfenix.do_post(pctfenix, pctfenix.url+'/controllers/load.chapters.type.php', s)
        parser = pctfenix.HTMLParser2()
        parser.feed(str(html))

    
    def tratar_series(self, html_virgen):
        #Get CNAME variable
        texto = "CNAME = "
        idx = html_virgen.find(texto)
        
        html = html_virgen[idx:]
        if html == "":
            return
        html = html[len(texto)+2:]
        CNAME = html[:html.find(",")-2]
        #Get CID variable
        texto = "CID = "
        idx = html_virgen.find(texto)
        
        html = html_virgen[idx:]
        if html == "":
            return
        html = html[len(texto)+2:]
        CID = html[:html.find(",")-2] 
        
        html2 = html_virgen
        while True:
            #Get O variable
            texto = "\" onClick=\"loadDD("
            idx = html2.find(texto)
            
            html2 = html2[idx:]
            if html2 == "":
                return
            html2 = html2[len(texto):]
            O = html2[:html2.find(");\"")]
            
            pctfenix.loadDD(self, CNAME, CID, O)
        
    def get_torrent_core(self, link):
        if link not in pctfenix.list: 
            pctfenix.list.append(link) 
        else:
            return
        html_virgen = pctfenix.retrieve_url(self, pctfenix.url + link[1:])
        html_virgen = str(html_virgen)
        texto = "class=\"ctn-download-torrent\"><a href=\""
        idx = html_virgen.find(texto)
        
        html = html_virgen[idx:]
        if len(html)>1:
            html = html[len(texto):]
            
            html = "https:" + html[:html.find("\"")]
            pctfenix.montar_torrent(self, html)
        else:
            pctfenix.tratar_series(self, html_virgen)
        
    def search(self, what, cat='all'):
        what = what.replace("%20", " ")
        what = {'s': what}
        html = self.do_post(self.url+'/controllers/search-mini.php', what)
        parser = pctfenix.HTMLParser1()
        parser.feed(str(html))
                        
                            
        
if __name__ == "__main__":
    m = pctfenix()
    m.search('star wars')
