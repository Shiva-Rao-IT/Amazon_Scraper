# 🛒 Amazon Product Scraper

**Amazon Scraper** is a full-stack web application that allows users to search and extract real-time product data from Amazon, including title, price, rating, and image. It presents the results in a user-friendly interface and supports storage for historical price tracking and analysis.

---

## 🚀 Features

- Product search interface with clean UI
- Scrapes real-time data: title, price, rating, availability, image
- Stores product results in MongoDB for future reference
- RESTful API built with Flask for backend operations
- Fully responsive frontend built with HTML, CSS, Bootstrap, and Jinja2
- Easy-to-use interface for non-technical users

---

## 🛠️ Technologies Used

- **Frontend:** HTML5, CSS3, Bootstrap, Jinja2 (Flask Templates)
- **Backend:** Python, Flask
- **Web Scraping:** BeautifulSoup, Requests
- **Database:** MongoDB
- **Templating Engine:** Jinja2
- **Server:** Flask development server or any WSGI server (e.g., Gunicorn)

---

## 🧪 How It Works

1. User enters a product keyword in the search box.
2. The server sends an HTTP request to Amazon and parses the HTML.
3. Relevant product data is extracted using BeautifulSoup.
4. The results are saved to MongoDB and displayed on the frontend.
5. Users can view current and stored search results.

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/amazon-scraper.git
cd amazon-scraper
```
2. Create and activate a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Add your MongoDB connection string
Edit the Flask app file (e.g., app.py) and replace the placeholder with your actual MongoDB connection URI:

```python
client = pymongo.MongoClient("your_mongodb_connection_string")
```
5. Run the application
```bash
python app.py
```

⚠️ Legal Disclaimer
This project is intended for educational purposes only. Web scraping Amazon or any third-party website may violate their terms of service. Please use responsibly.

🧑‍💻 Author
Shiva Yadav
BSC Student – University of Delhi

📄 License
This project is licensed under the MIT License. See the LICENSE file for more details.
