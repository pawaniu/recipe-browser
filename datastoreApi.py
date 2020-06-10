from google.cloud import datastore
from google.cloud import client

# Create, populate and persist an entity with keyID=1234
from google.cloud.datastore import Client

client = Client.from_service_account_json('pk-dev-service.json')


def create_record(recipe):
    key = client.key('Recipe', recipe['name'])
    entity = datastore.Entity(key=key)
    entity.update({
        'name' : recipe['name'],
        'url' : recipe['url'],
        'description': recipe['description']
    })
    client.put(entity)
    result = client.get(key)
    print(result)
    return result


def read_record():
    query = client.query(kind='Recipe')
    results = list(query.fetch())
    print ([recipe.to_dict() for recipe in results])
    return [recipe.to_dict() for recipe in results]


