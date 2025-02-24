import requests
from bs4 import BeautifulSoup
import pymongo
import time

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["nyc_apartments"]
collection = db["listings"]

def scrape_apartments():
    url = "https://newyork.craigslist.org/search/apa"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract apartment listings
    listings = []
    # Find all listings
    for listing in soup.find_all("li", class_="cl-static-search-result"):  
        title_elem = listing.find("div", class_="title")
        price_elem = listing.find("div", class_="price")
        location_elem = listing.find("div", class_="location")
        link_elem = listing.find("a", href=True)

        if title_elem and link_elem:
            title = title_elem.text.strip()
            link = link_elem["href"]
            price = price_elem.text.strip() if price_elem else "N/A"
            location = location_elem.text.strip() if location_elem else "Unknown"

            # Only add the listings with prices
            listings.append({"title": title, "price": price, "location": location, "url": link})

    if listings:  
        collection.delete_many({})  # Clear old data
        collection.insert_many(listings)
        print(f"Scraped {len(listings)} listings!")
    else:
        print("No listings found.")

if __name__ == "__main__":
    time.sleep(2)  # Prevents rapid requests to the server
    scrape_apartments()
