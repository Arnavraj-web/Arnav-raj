import requests
from bs4 import BeautifulSoup
import json

DATA_FILE = "database.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def scrape_price_by_url(url):
    if "amazon." in url:
        return scrape_amazon_price(url)
    elif "flipkart." in url:
        return scrape_flipkart_price(url)
    elif "meesho." in url:
        return scrape_meesho_price(url)
    else:
        return None, None

def scrape_amazon_price(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        title = soup.find(id='productTitle').get_text().strip()
        price = soup.find('span', {'class': 'a-price-whole'}).get_text().replace(',', '')
        return title, int(price)
    except:
        return None, None

def scrape_flipkart_price(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        title = soup.find('span', {'class': 'B_NuCI'}).get_text()
        price = soup.find('div', {'class': '_30jeq3 _16Jk6d'}).get_text().replace('₹', '').replace(',', '')
        return title.strip(), int(price)
    except:
        return None, None

def scrape_meesho_price(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        title = soup.find('h1').get_text()
        price = soup.find('span', {'class': 'pdp-discounted-price'}).get_text().replace('₹', '').replace(',', '')
        return title.strip(), int(price)
    except:
        return None, None

def add_product(user_id, url):
    data = load_data()
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = []

    title, price = scrape_price_by_url(url)
    if not title:
        return False, "❌ Unsupported or invalid product link."

    data[user_id].append({
        "url": url,
        "title": title,
        "last_price": price
    })

    save_data(data)
    return True, f"✅ Now tracking: {title}\nCurrent Price: ₹{price}"

def check_prices(bot):
    data = load_data()
    for user_id, items in data.items():
        for item in items:
            title, current_price = scrape_price_by_url(item['url'])
            if current_price and current_price < item['last_price']:
                msg = f"🔥 PRICE DROP ALERT!\n{title}\nOld Price: ₹{item['last_price']} → New Price: ₹{current_price}\n🔗 {item['url']}"
                bot.send_message(chat_id=user_id, text=msg)
                item['last_price'] = current_price
    save_data(data)
