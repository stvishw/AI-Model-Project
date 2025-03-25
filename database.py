from pymongo import MongoClient

# Replace with your password MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://user>:<password>@audio-project.faluj.mongodb.net/?retryWrites=true&w=majority&appName=audio-project"

try:
    # Connect to MongoDB Atlas
    client = MongoClient(MONGO_URI)
    db = client["fingerprint_db"]  # Database name
    fingerprint_collection = db["fingerprint_data"]  # Collection name

    # Collection is created
    if fingerprint_collection.count_documents({}) == 0:
        fingerprint_collection.insert_one({"message": "Collection created successfully!"})

    print("mongoDB Connected Successfully!")
except Exception as e:
    print(f"mongoDB Connection Failed: {e}")



