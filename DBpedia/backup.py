
offset = 0
url = 'http://dbpedia.org/sparql'

# --- Params for the endpoint

# decoded using https://meyerweb.com/eric/tools/dencoder/

# ?default-graph-uri=http%3A%2F%2Fdbpedia.org
default_graph_uri = "http://dbpedia.org"
# &format=application%2Fsparql-results%2Bjson
formats = {'json':'application/sparql-results+json','csv':''}
# &CXML_redir_for_subjs=121
CXML_redir_for_subjs = 121
# &CXML_redir_for_hrefs=
CXML_redir_for_hrefs = ""
# &timeout=30000
timeout = 30000
# &debug=on
debug_options = {"on":"on","off":"off"}
debug = "on"
# &run=+Run+Query+
run= " Run Query "


# --- QueryBuilder
preferedLang = "pt"

# --- Test

query = 'select distinct ?Concept where {[] a ?Concept} LIMIT 100'

params = {'query':query,'default-graph-uri':default_graph_uri,'format':formats['json'],'CXML_redir_for_subjs':CXML_redir_for_subjs,'CXML_redir_for_hrefs':CXML_redir_for_hrefs,'timeout':timeout,'debug':debug_options["on"],'run':run}

r = requests.get(url, params=params)
print(r.url)
print(r.text)


