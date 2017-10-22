import requests

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

payload = {'query':query,'default-graph-uri':default_graph_uri,'format':formats['json'],'CXML_redir_for_subjs':CXML_redir_for_subjs,'CXML_redir_for_hrefs':CXML_redir_for_hrefs,'timeout':timeout,'debug':debug_options["on"],'run':run}

r = requests.get(url, params=payload)
print(r.url)
print(r.text)


# --- Namespaces
dbo = {"alias":"dbo", "URL":"http://dbpedia.org/ontology/"}
dbp = {"alias":"dbp", "URL":"http://dbpedia.org/property/"}
foaf = {"alias":"foaf", "URL":"http://xmlns.com/foaf/0.1/"}
rdfs = {"alias":"foaf", "URL":"http://www.w3.org/2000/01/rdf-schema#"}

namespaces = [dbo, dbp, foaf, rdfs]

# - Parameters
def makeParameter(subject, alias, predicate, namespace, optional):
    return {"subject": subject, "predicate": {"namespace": namespace, "name": predicate}, "alias": alias, "optional": optional}

# - Entity class
personEntity = {"alias": "Person", "namespace": dbo, "type": "Person"}

# - Entity properties
properties = []

# - Required properties
isPrimaryTopicOf = makeParameter(subject=personEntity,
                                 alias="isPrimaryTopicOf",
                                 predicate="isPrimaryTopicOf",
                                 namespace=foaf,
                                 optional=False)

properties = [isPrimaryTopicOf]


  # ?person foaf:isPrimaryTopicOf ?t
  # OPTIONAL {?person rdfs:label ?label . }
  # OPTIONAL {?person foaf:name ?name . }
  # OPTIONAL {?person dbo:alias ?alias .}
  # OPTIONAL {?person dbo:birthName ?birthName .}
  # OPTIONAL {?person dbo:pseudonym ?pseudonym .}



SEPARATOR = "@$@"

def makeNamedEntityExtractionQuery(namespaces,parameters,entityType):
    query = []

    # Add namespaces
    # i.e. PREFIX dbo: <http://dbpedia.org/ontology/>
    for namespace in namespaces:
        query.append("PREFIX %s: <%s>" 
        % (namespace["alias"] , namespace["URL"] ))

    # Start the select
    query.append("SELECT DISTINCT")

    # Select the required and optional parameters
    # i.e. when needing concatenating: (group_concat(distinct ?name; separator = ",") as ?names)
    # i.e. otherwise: ?names
    for parameter in requiredParameters+optionalParameters:
        if parameter["concatenate"]:
            query.append(
                '(GROUP_CONCAT(DISTINCT ?%s; separator = "%s") as ?%s)'
                % (parameter["alias"],SEPARATOR,parameter["alias"]))
        else:
            query.append(
                '?%s'
                % (parameter["alias"]))

    
    # Start the 'where' clause
    query.append("WHERE{")

    # Select the class name
    # i.e. ?person a dbo:Person .
    query.append('?%s a %s:%s .'
                 % (entityType["alias"],
                    entityType["namespace"]["alias"],
                    entityType["type"]))
    
    # Graph Pattern for matching parameters
    # i.e. for required - ?person foaf:isPrimaryTopicOf ?t
    # i.e. for optional - OPTIONAL {?person foaf:name ?name . }
    for parameter in parameters:
        if parameter["optional"]:
          query.append("OPTIONAL {?%s %s:%s ?%s}"
                       % (parameter["subject"]["alias"],
                          parameter["predicate"]["namespace"]["alias"],
                          parameter["predicate"]["name"],
                          parameter["alias"]))
            
        else:
          query.append("?%s %s:%s ?%s"
                       % (parameter["subject"]["name"],
                          parameter["predicate"]["namespace"]["alias"],
                          parameter["predicate"]["name"],
                          parameter["alias"]))

    # Start the 'filter' function
    query.append('FILTER(')

    # Only returns the results in which there is at least one of the specified optional parameters
    # i.e. FILTER (regex(?alias, "[[:blank:]]") && regex(?pseudonym, "[[:blank:]]"))
    if parameters:
        query.append('regex(?%s, "[[:blank:]]"' 
                    % (parameters[0]["alias"] ) );
        for parameter in parameters:
            query.append('&& regex(?%s, "[[:blank:]]"' 
                        % (parameter["alias"] ) );

    # Close the 'filter' function
    query.append(')')


    # Close WHERE clause
    query.append('}')


    return string.join(query) 
