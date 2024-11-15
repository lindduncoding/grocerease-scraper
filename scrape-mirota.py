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

def scrape_category(category_id, max_pages=4):
    """Scrape products from a single category, including image links, limiting to a specific number of pages."""
    base_url = f"https://www.mirotakampus.com/id/Products/{category_id}"
    page = 1
    products = []

    while page <= max_pages:  # Limit to the first 'max_pages'
        url = f"{base_url}?page={page}"
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        # Extract category name from the page title
        if page == 1:  # Only need to do this once per category
            category_name = driver.title.split("|")[0].strip()

        # Find product elements
        product_elements = driver.find_elements(By.CSS_SELECTOR, "article")
        if not product_elements:
            break  # Exit if no products are found

        # Extract product data, including image links
        for product in product_elements:
            try:
                name = product.find_element(By.CSS_SELECTOR, "a.tittle:not(.landscape)").text
                price = product.find_element(By.CSS_SELECTOR, ".price").text
                image_link = product.find_element(By.CSS_SELECTOR, ".img-wrap img").get_attribute("src")
                products.append({"name": name, "price": price, "image_link": image_link})
            except Exception as e:
                print(f"Error scraping product: {e}")

        page += 1

    return category_name, products


def save_to_json(category_name, products):
    """Save scraped products to a JSON file named after the category."""
    file_name = f"{category_name.replace(' ', '_')}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4, ensure_ascii=False)
    print(f"Saved {len(products)} products to {file_name}")


# Main scraping loop for categories 45 to 60
for category_id in range(45, 61):
    print(f"Scraping category {category_id}...")
    try:
        category_name, products = scrape_category(category_id)
        save_to_json(category_name, products)
    except Exception as e:
        print(f"Error scraping category {category_id}: {e}")

# Quit WebDriver
driver.quit()

# # Function to scrape one page of products
# def scrape_products():
#     products = []
#     product_elements = driver.find_elements(By.CSS_SELECTOR, 'div.product') 

#     for product_element in product_elements:

#         image_element = product_element.find_element(By.CSS_SELECTOR, 'img.img-responsive')
#         image_url = image_element.get_attribute('src')
#         title_element = product_element.find_element(By.CSS_SELECTOR, 'a.tittle:not(.landscape)')
#         price_element = product_element.find_element(By.CSS_SELECTOR, 'div.price') 

#         image = image_url.strip() if image_url else 'No Image'
#         title = title_element.text.strip() if title_element else 'No Title'
#         price = price_element.text.strip() if price_element else 'No Price'

#         products.append({
#             'image_url': image,
#             'title': title,
#             'price': price
#         })

#     return products

# try:
#     # Open the URL
#     base_url = 'https://www.mirotakampus.com/id/Products/45'
#     driver.get(base_url)
#     all_products = []

#     # Scrape data from each page
#     while True:
#         time.sleep(2)  # Adjust sleep time as necessary

#         # Scrape products on the current page
#         products = scrape_products()
#         all_products.extend(products)

#         # Check if a "next" link exists
#         try:
#             next_button = driver.find_element(By.CSS_SELECTOR, 'a[rel="next"]')  # Selector for the next button
#             next_page_href = next_button.get_attribute('href')

#             if next_page_href:
#                 # Navigate to the next page
#                 next_page_url = urljoin(base_url, next_page_href)
#                 driver.get(next_page_url)
#                 time.sleep(2)  # Wait for the next page to load
#             else:
#                 break  # No next page, exit the loop
#         except Exception:
#             print("No more pages found.")
#             break

#     # Output results to JSON
#     print(json.dumps(all_products, indent=4))
#     with open('mirota_products.json', 'w') as f:
#         json.dump(all_products, f, indent=4)

# except Exception as e:
#     print(f"An error occurred: {e}")

# finally:
#     driver.quit()