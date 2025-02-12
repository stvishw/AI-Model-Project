import os
import librosa
import numpy as np
import soundfile as sf
from flask import Flask, request, jsonify
from pydub import AudioSegment
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# MongoDB Atlas Connection
MONGO_URI = "mongodb+srv://<user>:<password>@audio-project.faluj.mongodb.net/?retryWrites=true&w=majority&appName=audio-project"
client = MongoClient(MONGO_URI)
db = client["fingerprint_db"]
fingerprint_collection = db["fingerprint_data"]

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)

    # Convert MP3 to WAV if needed
    if filename.endswith(".mp3"):
        wav_filename = filename.replace(".mp3", ".wav")
        audio = AudioSegment.from_mp3(filename)
        audio.export(wav_filename, format="wav")
        filename = wav_filename  # Use the converted file

    try:
        # Extract fingerprint
        y, sr = librosa.load(filename)
        fingerprint = librosa.feature.mfcc(y=y, sr=sr).tolist()

        # Store fingerprint in MongoDB
        fingerprint_id = fingerprint_collection.insert_one({"fingerprint": fingerprint}).inserted_id

        return jsonify({"message": "Fingerprint stored successfully", "id": str(fingerprint_id)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/match", methods=["POST"])
def match_fingerprint():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)

    # Convert MP3 to WAV if needed
    if filename.endswith(".mp3"):
        wav_filename = filename.replace(".mp3", ".wav")
        audio = AudioSegment.from_mp3(filename)
        audio.export(wav_filename, format="wav")
        filename = wav_filename  # Use the converted file

    try:
        # Extract fingerprint
        y, sr = librosa.load(filename)
        new_fingerprint = librosa.feature.mfcc(y=y, sr=sr).tolist()

        # Fetch the latest stored fingerprint
        stored_data = fingerprint_collection.find_one({}, sort=[("_id", -1)])

        if stored_data is None or "fingerprint" not in stored_data:
            return jsonify({"error": "No fingerprint data found in the database"}), 404

        stored_fingerprint = stored_data["fingerprint"]

        # Compare fingerprints (Basic Example)
        similarity = np.corrcoef(np.array(new_fingerprint).flatten(), np.array(stored_fingerprint).flatten())[0, 1]

        return jsonify({"message": "Matching completed", "similarity": float(similarity)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)

