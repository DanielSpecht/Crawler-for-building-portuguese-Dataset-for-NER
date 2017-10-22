from EntityQueryBuilder import *

# - Namespaces
dbo = Namespace("dbo", "http://dbpedia.org/ontology/")
dbp = Namespace("dbp", "http://dbpedia.org/property/")
foaf = Namespace("foaf", "http://xmlns.com/foaf/0.1/")
rdfs = Namespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")

namespaces = [dbo, dbp, foaf, rdfs]

# - Entity class
personEntity = Entity( predicate = Predicate(namespace=dbo, name="person"), alias="Person")

# - Entity attributes

# - Required attributes
isPrimaryTopicOf = Variable(subject=personEntity,
                            alias="isPrimaryTopicOf",
                            predicate = Predicate(namespace=foaf,name="isPrimaryTopicOf"),
                            optional=False,
                            concatenate=False)

# - Optional propertiess
label = Variable(subject=personEntity,
                 alias="label",
                 predicate=Predicate(namespace=rdfs, name="label"),
                 optional=True,
                 concatenate=True)

name = Variable(subject=personEntity,
                alias="name",
                predicate=Predicate(namespace=foaf, name="name"),
                optional=True,
                concatenate=True)

alias = Variable(subject=personEntity,
                 alias="alias",
                 predicate=Predicate(namespace=dbo, name="alias"),
                 optional=True,
                 concatenate=True)

birthName = Variable(subject=personEntity,
                     alias="birthName",
                     predicate=Predicate(namespace=dbo, name="birthName"),
                     optional=True,
                     concatenate=True)

pseudonym = Variable(subject=personEntity,
                     alias="pseudonym",
                     predicate=Predicate(namespace=dbo, name="pseudonym"),
                     optional=True,
                     concatenate=True)

attributes = [isPrimaryTopicOf, label, name, alias, birthName, pseudonym]

builder = EntityQueryBuilder(namespaces,attributes,personEntity)

print builder.getQuery()