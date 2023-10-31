import pymongo


from settings import MONGO_PORT, MONGO_USER, MONGO_PASS

client = pymongo.MongoClient(
    host=f"mongodb://localhost:{MONGO_PORT}",
    username=MONGO_USER,
    password=MONGO_PASS
)

mydb: pymongo.mongo_client.database.Database = client.testdata
mycoll: pymongo.collection.Collection = mydb.dataset
