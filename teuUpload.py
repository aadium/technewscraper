import json
from pymongo import MongoClient, UpdateOne
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()

# Configuration
json_file_path = 'teu.json'
mongo_uri = os.getenv('MONGODB_URI')
database_name = 'tech-news-db'
collection_name = 'techeu'

# Read JSON file
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# Prepare bulk write operations 
operations = []
for item in data:
    # Assuming each item has a unique 'url' field
    operations.append(
        UpdateOne({'url': item['url']}, {'$set': item}, upsert=True)
    )

# Execute bulk write
if operations:
    result = collection.bulk_write(operations)
    print(f'Bulk write result: {result.bulk_api_result}')
else:
    print('No operations to perform.')

# Close the connection
client.close()