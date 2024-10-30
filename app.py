import os
import streamlit as st
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId  # Import ObjectId directly
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection details
MONGO_URI = os.getenv("MONGODB_CONNECTION_STRING")
DATABASE_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")


# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Streamlit app title
st.title("MongoDB Today's Created Objects Counter")

# Get today's date range
today_start = datetime.combine(datetime.today(), datetime.min.time())
today_end = datetime.combine(datetime.today(), datetime.max.time())

# Create query to count documents created today
query = {
    "_id": {
        "$gte": ObjectId.from_datetime(today_start),
        "$lt": ObjectId.from_datetime(today_end)
    }
}

pipeline = [
    {
        "$group": {
            "_id": { "$dateToString": { "format": "%Y-%m-%d", "date": "$createdAt" } },
            "count": { "$sum": 1 }
        }
    },
    { "$sort": { "_id": 1 } }  # Sort by date
]

# Optionally add a button to refresh the count
if st.button("Todays Count"):
    try:
        today_count = collection.count_documents(query)
        total_count = list(collection.aggregate(pipeline))

        st.success(f"Today's created agents count: **{today_count}**")
        st.success(f"Total's created agents count: **{total_count[0]['count']}**")

    except Exception as e:
        st.error(f"An error occurred: {e}")
