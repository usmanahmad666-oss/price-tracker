import requests
from bs4 import BeautifulSoup

def get_product_details(url):
    # Set custom headers to mimic a real browser and prevent blocking
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    try:
        # Send an HTTP GET request to the target URL
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None, None
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract product title (defaulting to 'h1' tag)
        title = soup.find("h1")
        title_text = title.get_text().strip() if title else "Unknown Product"
        
        # Extract product price using common class selectors
        price_tag = soup.find(class_=["price", "a-price", "current-price", "price_color"])
        
        if price_tag:
            price_str = price_tag.get_text().replace("$", "").replace("£", "").replace(",", "").strip()
            # Clean string and convert to float value
            price = float(''.join(c for c in price_str if c.isdigit() or c == '.'))
        else:
            price = 0.0

        return title_text, price

    except Exception as e:
        print(f"Error fetching product: {e}")
        return None, None

# Test script execution locally
if __name__ == "__main__":
    test_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    title, price = get_product_details(test_url)
    print(f"Product Name: {title}")
    print(f"Product Price: £{price}")