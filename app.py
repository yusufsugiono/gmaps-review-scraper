# Import library
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

begin = time.time();
attempts = 120
scroll_counter = 1
final_dataset = [];

driver = webdriver.Chrome()

# Membuka maps objek wisata sedudo
url = 'https://www.google.com/maps/place/Air+Terjun+Sedudo/@-7.7814262,111.7576068,17z/data=!3m1!4b1!4m6!3m5!1s0x2e79adf9c70ffff9:0xe17436693e56eab7!8m2!3d-7.7814262!4d111.7576068!16s%2Fg%2F11b_2y2c5y'
driver.get(url)

# Melakukan klik element "Ulasan Lainnya"
# element = driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[59]/div/button/span')
element = driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[57]/div/button/span')
driver.execute_script("arguments[0].click();", element)


ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

# Get scroll height.
last_height = driver.execute_script("return arguments[0].scrollHeight", WebDriverWait(driver, 5,ignored_exceptions=ignored_exceptions)\
                        .until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'))))

while True:
    print("Scrolling...", scroll_counter)

    # Scroll down to the bottom.
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', WebDriverWait(driver, 5,ignored_exceptions=ignored_exceptions)\
                        .until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'))))

    # Wait to load the page.
    time.sleep(2)

    # Calculate new scroll height and compare with last scroll height.
    new_height = driver.execute_script("return arguments[0].scrollHeight", WebDriverWait(driver, 5,ignored_exceptions=ignored_exceptions)\
                        .until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'))))

    if new_height == last_height:
        if attempts >= 0:
            print("Trying again..", attempts)
            time.sleep(10)
            new_height = driver.execute_script("return arguments[0].scrollHeight", WebDriverWait(driver, 5,ignored_exceptions=ignored_exceptions)\
                        .until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'))))
            attempts = attempts - 1
        else:
            break
    else:
        attempts = 120
        scroll_counter = scroll_counter + 1
    last_height = new_height


# Click button to load full text review
read_more_buttons = driver.find_elements(By.CLASS_NAME, 'w8nwRe.kyuRq')
for x in range(0,len(read_more_buttons)):
    if read_more_buttons[x].is_displayed():
        read_more_buttons[x].click()


# Extracting review data
response = BeautifulSoup(driver.page_source, 'html.parser')
review_card = response.find_all('div', class_='jftiEf')
print("Total reviews :", len(review_card))

for review in review_card:
    # review_name = review['aria-label']
    review_id = review['data-review-id']
    review_text = review.find('span', class_='wiI7pd').text
    final_dataset.append([review_id, review_text])


# Save to CSV file
with open("final_dataset.csv", 'w', encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['review_id', 'review_text'])
    csvwriter.writerows(final_dataset) 

end = time.time()

print(f"Total runtime of the program is {end - begin} seconds")

time.sleep(10)

