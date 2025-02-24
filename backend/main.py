from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware to allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["nyc_apartments"]
collection = db["listings"]


@app.get("/")
def home():
    return {"message": "NYC Apartment Listings API is running"}


@app.get("/listings")
def get_listings(price_max: int = None, location: str = None):
    query = {}
    if price_max:
        query["price"] = {"$lte": price_max}
    if location:
        query["location"] = {"$regex": location, "$options": "i"}

    listings = list(collection.find(query, {"_id": 0}))
    return {"listings": listings}
