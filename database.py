from pymongo import MongoClient

# Replace with your actual MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://user>:<password>@audio-project.faluj.mongodb.net/?retryWrites=true&w=majority&appName=audio-project"

try:
    # Connect to MongoDB Atlas
    client = MongoClient(MONGO_URI)
    db = client["fingerprint_db"]  # Database name
    fingerprint_collection = db["fingerprint_data"]  # Collection name

    # Insert a test document to ensure the collection is created
    if fingerprint_collection.count_documents({}) == 0:
        fingerprint_collection.insert_one({"message": "Collection created successfully!"})

    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print(f"❌ MongoDB Connection Failed: {e}")



