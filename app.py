from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017")  # Connect to your MongoDB instance
db = client['DATA_SCRAPPER']  # Use the database you created
collection = db['PRODUCTS']   # Use the collection you created

# Function to extract Product Title
def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        return title.text.strip()
    except AttributeError:
        return ""

def get_price(soup):
    try:
        # Try priceblock_ourprice
        price = soup.find("span", attrs={"id": "priceblock_ourprice"})
        if price and "$" in price.text:
            return price.text.strip()

        # Try deal price
        price = soup.find("span", attrs={"id": "priceblock_dealprice"})
        if price and "$" in price.text:
            return price.text.strip()

        # Try a-price-whole and fraction
        whole = soup.find("span", class_="a-price-whole")
        fraction = soup.find("span", class_="a-price-fraction")
        if whole and fraction:
            return f"${whole.text.strip()}.{fraction.text.strip()}"

        # Try a-offscreen
        price = soup.find("span", class_="a-offscreen")
        if price and "$" in price.text:
            return price.text.strip()
    except Exception as e:
        print("Price extraction error:", e)

    return "Price Not Available"



# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""
    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()
    except AttributeError:
        review_count = ""
    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        return available.find("span").string.strip()
    except AttributeError:
        return "Not Available"
    
# Function to extract Product Image URL
def get_image_url(soup):
    try:
        image = soup.find("img", attrs={"id": "landingImage"})
        return image['src'] if image else "Image Not Available"
    except (AttributeError, TypeError):
        return "Image Not Available"

@app.route("/", methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        search_term = request.form['search_term']
        HEADERS = {
            'User-Agent': '',
            'Accept-Language': 'en-US, en;q=0.5'
        }
        URL = f"https://www.amazon.com/s?k={search_term.replace(' ', '+')}&ref=nb_sb_noss"

        # HTTP Request
        webpage = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})

        links_list = ["https://www.amazon.com" + link.get('href') for link in links]
        
        d = {"title": [], "price": [], "rating": [], "reviews": [], "availability": [], "image_url": []}

        for link in links_list:
            new_webpage = requests.get(link, headers=HEADERS)
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")
            
            # Extract product information
            title = get_title(new_soup)
            price = get_price(new_soup)
            rating = get_rating(new_soup)
            reviews = get_review_count(new_soup)
            availability = get_availability(new_soup)
            image_url = get_image_url(new_soup)

            # Create a document to insert into MongoDB
            product_data = {
                "title": title,
                "price": price,
                "rating": rating,
                "reviews": reviews,
                "availability": availability,
                "image_url": image_url
            }

            # Insert the document into the MongoDB collection
            collection.insert_one(product_data)

            # Add to dictionary for DataFrame
            d['title'].append(title)
            d['price'].append(price)
            d['rating'].append(rating)
            d['reviews'].append(reviews)
            d['availability'].append(availability)
            d['image_url'].append(image_url)

        # Convert dictionary to DataFrame
        amazon_df = pd.DataFrame.from_dict(d)
        amazon_df['title'].replace('', np.nan, inplace=True)
        amazon_df = amazon_df.dropna(subset=['title'])

        reviews = amazon_df.to_dict(orient='records')
        return render_template('result.html', reviews=reviews)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
