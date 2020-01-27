import pymongo
import pprint

## Function that inserts a new restaurant into the db using different args
def insert_restaurant(building, coords, rua, zipcode, localidade, gastronomia, grades, nome, id):
    db.rest.insert_one({"address": {"building": building, "coord": coords, "rua": rua, "zipcode": zipcode}, "localidade": localidade, "gastronomia": gastronomia, "grades": grades, "nome": nome, "restaurant_id": id})

## Function that inserts directly a new doc
def insert_restaurant_doc(doc):
    db.rest.insert_one(doc)


## Function that updates field field of the restaurant identified by id
def edit_restaurant_single_field(id, field, value):
    db.test.update_one({'restaurant_id': id}, {'field': value})

## Function that replaces every field of the restaurant identified by id
def edit_restaurant_all_fields(id, doc):
    db.test.update_one({'restaurant_id': id}, doc)


## Function that queries the db for every document
def query(args=None):
    if args == None:
        return db.rest.find()


## Count localidades
def count_localidades():
    return len(db.rest.distinct('localidade'))


## Count restaurants by location
def count_rest_by_loca():
    # We want to convert the query:
    # db.rest.aggregate( [ {$group : {_id : "$localidade", count: {$sum: 1} }}])
    # to Python

    query = [ {"$group" : { "_id" : "$localidade", "count": {"$sum": 1} }}]
    return db.rest.aggregate(query)


## Count restaurants by Location by Gastronomia
def count_by_lg():
    query = [ {"$group" : { "_id" : {"localidade": "$localidade", "gastronomia" : "$gastronomia"}, "count": {"$sum": 1} }}]
    return db.rest.aggregate(query)


## Get Rest With Name Closer to
def get_rest_name(name):
    ## We want to convert the query:
    # db.rest.find( { "nome" : { $regex : "^Wil.*"}  } , { "restaurant_id" : 1, "nome" : 1, "localidade" : 1, "gastronomia" : 1, "_id" : 0}).pretty()
    return db.rest.find( { "nome" : { "$regex" : "^"+name+".*"}})


## Driver code    

client = pymongo.MongoClient("localhost", 27017)
db = client.cbd

# for item in query():
#     pprint.pprint(item)

db.rest.create_index("localidade")
db.rest.create_index("gastronomia")
db.rest.create_index("nome")

print(count_localidades())
for t in count_rest_by_loca():
    print((t['_id'], t['count']))

for t in count_by_lg():
    print((t['_id']['localidade'], t['_id']['gastronomia'], t['count']))

for t in get_rest_name("Wil"):
    print(t['nome'])


