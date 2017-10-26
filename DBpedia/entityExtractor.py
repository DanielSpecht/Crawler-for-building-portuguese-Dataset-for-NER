from EntityQueryBuilder import *
from RequestDBpediaSPARQL import *
import os
import errno

# - Namespaces
dbo = Namespace("dbo", "http://dbpedia.org/ontology/")
dbp = Namespace("dbp", "http://dbpedia.org/property/")
foaf = Namespace("foaf", "http://xmlns.com/foaf/0.1/")
rdfs = Namespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")

namespaces = [dbo, dbp, foaf, rdfs]

# Entity classes
personEntity = Entity( predicate = Predicate(namespace=dbo, name="Person"), alias="Person")
placeEntity = Entity( predicate = Predicate(namespace=dbo, name="Place"), alias="Place")
organisationEntity = Entity( predicate = Predicate(namespace=dbo, name="Organisation"), alias="Organisation")

# Attributes

# Required attributes
isPrimaryTopicOf = Variable(subject=None,
                            alias="isPrimaryTopicOf",
                            predicate = Predicate(namespace=foaf,name="isPrimaryTopicOf"),
                            optional=False,
                            concatenate=False)

# Optional propertiess

# Thing properies

abbreviation = Variable(subject=None,
                 alias="abbreviation",
                 predicate=Predicate(namespace=dbo, name="abbreviation"),
                 optional=True,
                 concatenate=True)

alternativeName = Variable(subject=None,
                 alias="alternativeName",
                 predicate=Predicate(namespace=dbo, name="alternativeName"),
                 optional=True,
                 concatenate=True)

commonName = Variable(subject=None,
                 alias="commonName",
                 predicate=Predicate(namespace=dbo, name="commonName"),
                 optional=True,
                 concatenate=True)

familyName = Variable(subject=None,
                 alias="familyName",
                 predicate=Predicate(namespace=foaf, name="familyName"),
                 optional=True,
                 concatenate=True)

givenName = Variable(subject=None,
                 alias="givenName",
                 predicate=Predicate(namespace=foaf, name="givenName"),
                 optional=True,
                 concatenate=True)

nick = Variable(subject=None,
                 alias="nick",
                 predicate=Predicate(namespace=foaf, name="nick"),
                 optional=True,
                 concatenate=True)

surname = Variable(subject=None,
                 alias="surname",
                 predicate=Predicate(namespace=foaf, name="surname"),
                 optional=True,
                 concatenate=True)

formerName = Variable(subject=None,
                 alias="formerName",
                 predicate=Predicate(namespace=dbo, name="formerName"),
                 optional=True,
                 concatenate=True)

longName = Variable(subject=None,
                 alias="longName",
                 predicate=Predicate(namespace=dbo, name="longName"),
                 optional=True,
                 concatenate=True)

dboName = Variable(subject=None,
                 alias="dboName",
                 predicate=Predicate(namespace=dbo, name="name"),
                 optional=True,
                 concatenate=True)

originalName = Variable(subject=None,
                 alias="originalName",
                 predicate=Predicate(namespace=dbo, name="originalName"),
                 optional=True,
                 concatenate=True)

label = Variable(subject=None,
                 alias="label",
                 predicate=Predicate(namespace=rdfs, name="label"),
                 optional=True,
                 concatenate=True)

foafName = Variable(subject=None,
                alias="foafName",
                predicate=Predicate(namespace=foaf, name="name"),
                optional=True,
                concatenate=True)

alias = Variable(subject=None,
                 alias="alias",
                 predicate=Predicate(namespace=dbo, name="alias"),
                 optional=True,
                 concatenate=True)

# Person variables

birthName = Variable(subject=None,
                     alias="birthName",
                     predicate=Predicate(namespace=dbo, name="birthName"),
                     optional=True,
                     concatenate=True)

pseudonym = Variable(subject=None,
                     alias="pseudonym",
                     predicate=Predicate(namespace=dbo, name="pseudonym"),
                     optional=True,
                     concatenate=True)

# Organisation variables

historicalName = Variable(subject=None,
                     alias="historicalName",
                     predicate=Predicate(namespace=dbo, name="historicalName"),
                     optional=True,
                     concatenate=True)

requiredAttributes = [isPrimaryTopicOf]
thingAttributes = [abbreviation,alternativeName,commonName,familyName,givenName,nick,surname,formerName,longName,dboName,originalName,label,foafName,alias]
commonAttributes = requiredAttributes + thingAttributes

personAttributes = [birthName,pseudonym] + commonAttributes
placeAttributes = [historicalName] + commonAttributes
organisationAttributes = commonAttributes

# Just checking
# for i in range(len(personAttributes)):
#     personAttributes[i].subject = personEntity
# print "\n\n"
# print EntityQueryBuilder(namespaces, personAttributes, personEntity).getQuery()

# for i in range(len(placeAttributes)):
#     placeAttributes[i].subject = placeEntity
# print "\n\n"
# print EntityQueryBuilder(namespaces, placeAttributes, placeEntity).getQuery()

# for i in range(len(organisationAttributes)):
#     organisationAttributes[i].subject = organisationEntity
# print "\n\n"
# print EntityQueryBuilder(namespaces, organisationAttributes, organisationEntity).getQuery()

def saveResultInFile(lines,batch,entity,folder):
    # i.e. documents/person_1.csv
    fileName = "%s%s_%s.csv"%(folder,entity.alias,batch)

    # Make path if not exist
    if not os.path.exists(os.path.dirname(fileName)):
        os.makedirs(os.path.dirname(fileName))

    # TODO - Change to a csv file writer
    file = open(fileName,"w")
    for line in lines:
        file.writelines(line+"\n")
    file.close()

def main():
    attributesOfEntities = [personAttributes,placeAttributes,organisationAttributes]
    entities = [personEntity,placeEntity,organisationEntity]
    
    for entity, attributes in zip(entities, attributesOfEntities):
        
        # Associate
        for i in range(len(attributes)):
            attributes[i].subject = entity

        # Query generator
        queryBuilder = EntityQueryBuilder(namespaces, attributes, entity)

        # Query executor
        DBpediaQueryRequest = RequestDBpediaSPARQL(endpoint='http://pt.dbpedia.org/sparql',format=FORMATS["csv"])

        folder = "%s/"%(entity.alias)
        hasResults = True
        batchSize = 10
        iteration = 0
        while hasResults:
            # Get results
            # print queryBuilder.getQuery()
            result = DBpediaQueryRequest.requestQuery(query = queryBuilder.getQuery(limit = batchSize,offset=iteration*batchSize))
            lines = result.encode("utf-8").splitlines()

            saveResultInFile(lines,iteration+1,entity,folder)

            # Stop check
            if len(lines) < batchSize-1:
                hasResults = False

            iteration += 1
            print result
            print "\n Batch: %s -- N results: %s \n"%(iteration,len(lines))

if __name__ == "__main__":
    main()