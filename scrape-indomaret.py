from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options
options = Options()
options.headless = True  # Run headless
options.add_argument("--no-sandbox")  # Overcome limited resource problems
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

# Path to your ChromeDriver
chrome_driver_path = '/home/fred/chromedriver-linux64/chromedriver'  # Update this to your chromedriver path

# Set up the driver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    url = 'https://www.klikindomaret.com/category/makanan-beku'  # Replace with your URL
    driver.get(url)
    
    # Let the page load
    time.sleep(5)  # Adjust sleep time as necessary for the page to load completely

    # Get all product titles
    title_elements = driver.find_elements(By.CSS_SELECTOR, 'div.produk.produk-level div.each-item div.title')
    product_titles = [title.text for title in title_elements]
    
    # Get all product prices
    price_elements = driver.find_elements(By.CSS_SELECTOR, 'div.produk.produk-level div.each-item span.normal.price-value')
    product_prices = [price.text for price in price_elements]

    # # Print the scraped titles and prices
    # for title, price in zip(product_titles, product_prices):
    #     print(f'Product Title: {title}, Product Price: {price}')

    # Combine titles and prices into a list of dictionaries
    products = [
        {"title": title, "price": price}
        for title, price in zip(product_titles, product_prices)
    ]

    # Convert the list of dictionaries to JSON format
    json_data = json.dumps(products, indent=4)
    print(json_data)  # Print or save json_data as needed

except Exception as e:
    print(f'An error occurred: {e}')
finally:
    driver.quit() 
