import pymongo
from pymongo import MongoClient
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Configuration
mongo_uri = os.getenv('MONGODB_URI')
database_name = 'tech-news-db'
collection_name = 'theverge'

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# Find duplicates based on 'title'
pipeline = [
    {
        "$group": {
            "_id": {"title": "$title"},
            "count": {"$sum": 1},
            "docs": {"$push": "$_id"}
        }
    },
    {
        "$match": {
            "count": {"$gt": 1}
        }
    }
]

duplicates = list(collection.aggregate(pipeline))

# Prepare bulk delete operations
operations = []
for doc in duplicates:
    # Keep the first document and delete the rest
    ids_to_delete = doc["docs"][1:]
    for _id in ids_to_delete:
        operations.append(pymongo.DeleteOne({"_id": _id}))

# Execute bulk delete
if operations:
    result = collection.bulk_write(operations)
    print(f'Deleted {result.deleted_count} duplicate documents.')
else:
    print('No duplicates found.')

# Close the connection
client.close()
