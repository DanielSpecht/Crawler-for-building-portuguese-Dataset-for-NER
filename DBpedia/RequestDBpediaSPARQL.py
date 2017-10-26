import requests

FORMATS = {'json':'application/sparql-results+json','csv':'text/csv'}

class RequestDBpediaSPARQL:
    def __init__(self,
                 endpoint,
                 CXMLRedirForHrefs="",
                 defaultGraphURI="",
                 format="",
                 CXMLRedirForSubjs="",
                 timeout="30000",
                 debug="on",):

                 self.endpoint = endpoint
                 self.CXMLRedirForHrefs = CXMLRedirForHrefs
                 self.defaultGraphURI = defaultGraphURI
                 self.format = format
                 self.CXMLRedirForSubjs = CXMLRedirForSubjs
                 self.timeout = timeout
                 self.debug = debug

    def requestQuery(self, query):
        params = {'query': query,
                  'default-graph-uri': self.defaultGraphURI,
                  'format': self.format,
                  'CXML_redir_for_subjs': self.CXMLRedirForSubjs,
                  'CXML_redir_for_hrefs': self.CXMLRedirForHrefs,
                  'timeout': self.timeout,
                  'debug': self.debug}

        request = requests.get(self.endpoint, params=params)
        return request.text


