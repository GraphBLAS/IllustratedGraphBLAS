import os, sys
import subprocess
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin, urlparse
from time import sleep

# Images used in Chapter0/Scene4.py
# Format: (matrix_name, matrix_image_index, graph_image_index)
REQUIRED_IMAGES = {
    'pct20stif': [1, 2],       # Structural Analysis
    'rw5151': [1, 5],          # Statistics and Mathematics
    'lpl1': [2, 4],            # Resource Optimization
    'poli_large': [1, 5],      # Economic Planning
    'conf5_0-4x4-10': [1, 5],  # Theoretical Quantum Chemistry
}

def main(main_page_url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    base_dir = 'scraped_images'
    os.makedirs(base_dir, exist_ok=True)
    driver.get(main_page_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    thumbnails = soup.find_all('a', href=True)

    for thumbnail in thumbnails:
        img_tag = thumbnail.find('img')
        if img_tag:
            target_link = urljoin(main_page_url, thumbnail['href'])
            path_element = urlparse(target_link).path.split('/')[-1]

            # Skip matrices not in our required list
            if path_element not in REQUIRED_IMAGES:
                continue

            required_indices = REQUIRED_IMAGES[path_element]
            target_dir = os.path.join(base_dir, path_element)
            os.makedirs(target_dir, exist_ok=True)

            print(f"Downloading {path_element}...")

            # Navigate to target page and scrape images
            driver.get(target_link)
            sleep(2)
            target_soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Scrape and download only the required images
            images = target_soup.find_all('img')
            for idx, img in enumerate(images):
                if idx not in required_indices:
                    continue

                img_url = urljoin(target_link, img['src'])
                img_filename = f'image_{idx}.jpg'
                img_path = os.path.join(target_dir, img_filename)

                if not os.path.exists(img_path):
                    img_data = requests.get(img_url).content
                    with open(img_path, 'wb') as f:
                        f.write(img_data)
                    print(f"  Downloaded {img_filename}")

    driver.quit()

    # Invert images using Chapter0/invert.sh
    script_dir = os.path.dirname(os.path.abspath(__file__))
    invert_script = os.path.join(script_dir, 'Chapter0', 'invert.sh')
    print("Inverting images...")
    subprocess.run(['bash', invert_script], cwd=script_dir, check=True)
    print("Done.")


if __name__ == '__main__':
    main(sys.argv[1])
