class Namespace:
    def __init__(self,alias, URL):
        self.alias = alias
        self.URL = URL

class Variable:
    def __init__(self,subject, alias, predicate, optional, concatenate):
        self.subject = subject
        self.alias = alias
        self.predicate = predicate
        self.optional = optional
        self.concatenate = concatenate

class Predicate:
    def __init__(self,namespace,name):
        self.namespace = namespace
        self.name = name

class Entity:
    def __init__(self,alias, predicate):
        self.alias = alias
        self.predicate = predicate

class EntityQueryBuilder:
    def __init__ (self,namespaces,parameters,entity):
        self.namespaces = namespaces
        self.parameters = parameters
        self.entity = entity
        self._separator = ";;"

    def getQuery(self,limit=None,offset=None):
        return self._getQuery(self.namespaces,self.parameters,self.entity,offset,limit)

    def _getQuery(self,namespaces,parameters,entity,offset,limit):
        query = []

        # Add namespaces
        # i.e. PREFIX dbo: <http://dbpedia.org/ontology/>
        for namespace in namespaces:
            query.append("PREFIX %s: <%s>" 
            % (namespace.alias , namespace.URL ))

        # Start the select
        query.append("SELECT DISTINCT")

        # Select the required and optional parameters
        # i.e. when needing concatenating: (group_concat(distinct ?name; separator = ",") as ?names)
        # i.e. otherwise: ?names
        for parameter in parameters:
            if parameter.concatenate:
                query.append(
                    '(GROUP_CONCAT(DISTINCT ?%s; separator = "%s") as ?%s)'
                    % (parameter.alias,self._separator,parameter.alias))
            else:
                query.append(
                    '?%s'
                    % (parameter.alias))
        
        # Start the 'where' clause
        query.append("WHERE{")

        # Select the class name
        # i.e. ?person a dbo:Person .
        query.append('?%s a %s:%s .'
                    % (entity.alias,
                        entity.predicate.namespace.alias,
                        entity.predicate.name))
        
        # Graph Pattern for matching parameters
        # i.e. for required - ?person foaf:isPrimaryTopicOf ?t
        # i.e. for optional - OPTIONAL {?person foaf:name ?name . }
        for parameter in parameters:
            if parameter.optional:
                query.append("OPTIONAL {?%s %s:%s ?%s .}"
                            % (parameter.subject.alias,
                                parameter.predicate.namespace.alias,
                                parameter.predicate.name,
                                parameter.alias))
                
            else:
                query.append("?%s %s:%s ?%s ."
                            % (parameter.subject.alias,
                                parameter.predicate.namespace.alias,
                                parameter.predicate.name,
                                parameter.alias))

        # Only returns the results in which there is at least one of the specified optional parameters
        # i.e. FILTER (bound(?alias) || bound(?birthName))
        if any(parameter.optional for parameter in parameters):
            # Start the 'filter' function
            query.append('FILTER(')

            query.append('bound(?%s)'
                        % (parameters[0].alias))
            for parameter in parameters:
                if parameter.optional:
                    query.append('||bound(?%s)'
                                % (parameter.alias))

            # Close the 'filter' function
            query.append(')')

        # Close WHERE clause
        query.append('}')
        
        if limit:
            query.append("LIMIT %s"%(limit))

        if offset:
            query.append("OFFSET %s"%(offset))

        return "\n".join(query) 