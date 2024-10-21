
# 🚀 Google Map Scraper

This Python script helps you scrape **Google Maps** search results for local businesses (like cafes, restaurants, hospitals, etc.) in any specific location. It ensures unique results and saves the scraped data into a structured JSON file for further use. 🎯

## 🔧 Installation

To get started, you'll need to install the required dependencies from the `requirements.txt` file. Follow the steps below:

### 1. Clone the Repository 🛠️

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/shivraj-prajapati/google-map-scraper.git
```

Navigate to the project directory:

```bash
cd google-map-scraper
```

### 2. Install Dependencies 📦

Install the necessary packages by running:

```bash
pip install -r requirements.txt
```

## 🚀 Usage

Once installed, you can run the script with your desired parameters to scrape data.

### Parameters:

- `page`: Number of result pages to scrape (e.g., `60` for scraping up to 6 pages).
- `category`: The type of businesses you're searching for (e.g., `cafe`, `restaurant`, `medical`).
- `location`: The city or area you want to search in (e.g., `jamnagar`).

### Running the Script 🖥️

Navigate to the project folder and run the script using the following command:

```bash
python app.py
```

### Example Command 📝

To search for cafes in **Jamnagar** and scrape up to 6 pages of results:

```bash
python app.py --page 60 --category cafe --location jamnagar
```

The script will save the scraped data into a JSON file named after the `category` and `location` (e.g., `cafe_jamnagar.json`).

## 📂 Output

The scraped data will be saved in a `.json` file with the following structure:

```json
[
  {
    "name": "XYZ Cafe",
    "contact": "9876543210",
    "address": "123 Street, Jamnagar",
    "status": "Open now",
    "additional_info": "Cozy ambiance, Free Wi-Fi",
    "website_url": "http://xyzcafe.com",
    "direction_url": "https://maps.google.com/..."
  },
  ...
]
