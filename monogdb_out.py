import pymongo

# Establish a connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Access the database and collection
db = client["swimdatabase"]
collection = db["entries"]

# Find all documents in the collection
results = collection.find()

# Loop through the results and print each document
for result in results:
    print(result)
