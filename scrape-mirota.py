from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json

# Set up Chrome options
options = Options()
options.headless = True  # Run headless to not show the browser window
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Path to your ChromeDriver
chrome_driver_path = '/home/fred/chromedriver-linux64/chromedriver'  # Update this to your chromedriver path

# Set up the driver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Function to scrape one page of products
def scrape_products():
    products = []
    product_elements = driver.find_elements(By.CSS_SELECTOR, 'div.product') 

    for product_element in product_elements:

        image_element = product_element.find_element(By.CSS_SELECTOR, 'img.img-responsive')
        image_url = image_element.get_attribute('src')
        title_element = product_element.find_element(By.CSS_SELECTOR, 'a.tittle:not(.landscape)')
        price_element = product_element.find_element(By.CSS_SELECTOR, 'div.price') 

        image = image_url.strip() if image_url else 'No Image'
        title = title_element.text.strip() if title_element else 'No Title'
        price = price_element.text.strip() if price_element else 'No Price'

        products.append({
            'image_url': image,
            'title': title,
            'price': price
        })

    return products

try:
    # Open the URL
    base_url = 'https://www.mirotakampus.com/id/Products/45'
    driver.get(base_url)
    all_products = []

    # Scrape data from each page
    while True:
        time.sleep(2)  # Adjust sleep time as necessary

        # Scrape products on the current page
        products = scrape_products()
        all_products.extend(products)

        # Check if a "next" link exists
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a[rel="next"]')  # Selector for the next button
            next_page_href = next_button.get_attribute('href')

            if next_page_href:
                # Navigate to the next page
                next_page_url = urljoin(base_url, next_page_href)
                driver.get(next_page_url)
                time.sleep(2)  # Wait for the next page to load
            else:
                break  # No next page, exit the loop
        except Exception:
            print("No more pages found.")
            break

    # Output results to JSON
    print(json.dumps(all_products, indent=4))
    with open('mirota_products.json', 'w') as f:
        json.dump(all_products, f, indent=4)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()