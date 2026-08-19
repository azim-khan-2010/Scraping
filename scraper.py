import requests
from bs4 import BeautifulSoup
import csv
import os

URL = "https://books.toscrape.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)

if response.status_code != 200:
    print("Failed to access the website.")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

products = []

for book in soup.select("article.product_pod"):
    name = book.select_one("h3 a")["title"]
    price = book.select_one(".price_color").get_text(strip=True)

    rating_element = book.select_one(".star-rating")
    rating = rating_element.get("class")[1]

    products.append({
        "Name": name,
        "Price": price,
        "Rating": rating
    })

os.makedirs("data", exist_ok=True)

with open("data/scraped_data.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=["Name", "Price", "Rating"]
    )

    writer.writeheader()
    writer.writerows(products)

print("Scraping completed successfully!")
print(f"{len(products)} products collected.")
print("Data saved to data/scraped_data.csv")