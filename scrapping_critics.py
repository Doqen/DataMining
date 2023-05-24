from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import time

driver = webdriver.Chrome()

# List to hold the scraped paragraphs
paragraphs = []

# Open the main page
driver.get('https://www.imdb.com/title/tt6710474/externalreviews/')

# Find clickable elements by class name
clickable_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ipc-metadata-list-item__icon-link')))

for i in range(min(10, len(clickable_elements))):  # 10 or less, depending on how many such elements exist
    # Get the current window handle
    main_window = driver.current_window_handle

    # Use javascript to click the element
    driver.execute_script("arguments[0].click();", clickable_elements[i])

    # Switch to the new window
    new_window = [window for window in driver.window_handles if window != main_window][0]
    driver.switch_to.window(new_window)
    
    # Extract the paragraph elements if they exist. If they do not exist, skip the page.
    try:
        p_elements = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'p')))
        
        for p in p_elements:
            paragraphs.append(p.text)

    except TimeoutException:
        print("No <p> tags found in this page. Moving to the next page...")
    
    # Close the new tab and switch back to the main tab
    driver.close()
    driver.switch_to.window(main_window)

    # Wait for the page to load again
    time.sleep(5)

    # Redefine clickable elements after going back
    clickable_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ipc-metadata-list-item__icon-link')))

driver.quit()

# Write the paragraphs to a csv file
with open('paragraphs.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for p in paragraphs:
        writer.writerow([p])
