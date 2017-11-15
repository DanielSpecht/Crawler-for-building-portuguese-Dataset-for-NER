# -*- coding: utf-8 -*-
import requests
import wikipedia
#endpoint = https://pt.wikipedia.org/w/api.php
# ?action=query
# &prop=revisions
# &rvsection=0
# &titles=Luiz_In%C3%A1cio_Lula_da_Silva
# &rvprop=content
# &format=xmlfm

FORMATS = {'json':'application/sparql-results+json','csv':'text/csv'}
 

class RequestWikimediaAPI:
    def __init__(self,
                 endpoint="https://pt.wikipedia.org/w/api.php",
                 action="query",
                 prop="revisions",
                 rvsection=0,                 
                 rvprop="content",
                 format="json"):

        self.endpoint=endpoint
        self.action=action
        self.prop=prop
        self.rvsection=rvsection
        self.rvprop=rvprop
        self.format=format

    def requestPage(self, titles):
        params = {"titles": titles,
                  "action": self.action,
                  "prop": self.prop,
                  "rvsection": self.rvsection,
                  "rvprop": self.rvprop,
                  "format": self.format}

        request = requests.get(self.endpoint, params=params)
        print request.url
        return request.text

#a = RequestWikimediaAPI()
#print a.requestPage("Luiz_Inácio_Lula_da_Silva")

wikipedia.set_lang("pt")
lula = wikipedia.page("Luiz_Inácio_Lula_da_Silva")
print lula.sections
print lula.content
print lula.links
print lula.section(lula.sections[0])