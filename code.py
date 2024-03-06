##used libraries and module
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import matplotlib.pyplot as plt
## Initiates a Chrome WebDriver session and Navigates the WebDriver to the specified URL.
def scrape_and_search(search_input):
    driver = webdriver.Chrome()
    url = 'https://wuzzuf.net/jobs/egypt'
    driver.get(url)

    ## Finds the search bar element on the webpage by its class name.
    search = driver.find_element(By.NAME, "q")
    search.send_keys(search_input)
    search.send_keys(Keys.RETURN)
    ## Sets an implicit wait time of 15 seconds to allow the page to load before scraping.
    driver.implicitly_wait(15)

    ## function: Finds job titles, data posted, job locations, and job
    ## links on the current page and stores them in a DataFrame using Pandas.
    def scrape_page():
        titles = driver.find_elements(By.CSS_SELECTOR, 'h2.css-m604qf')
        job_title = []
        for title in titles:
            job_title.append(title.text)
        df = pd.DataFrame(job_title, columns=['title'])
        times_and_locations = driver.find_elements(By.CLASS_NAME, 'css-d7j1kk')
        data_posted = []
        job_location = []
        for time in times_and_locations:
            data_posted.append(time.text.split('\n')[1])
        for location in times_and_locations:
            job_location.append(location.text.split('\n')[0])
        df['data posted'] = data_posted
        df['job location'] = job_location
        anchor_elements = driver.find_elements(By.XPATH, '//h2[@class="css-m604qf"]/a')
        links = []
        for element in anchor_elements:
            link = element.get_attribute('href')
            links.append(link)
        df['job link'] = links
        return df

    df = scrape_page()
    page_counter = 0

    ## function: Finds the next page button, clicks it if it exists,
    ## and breaks the loop if the button is not found or if the page counter exceeds 10.
    def next_page():
        next_page_buttons = driver.find_elements(By.CSS_SELECTOR, 'button.css-zye1os.ezfki8j0')
        for button in next_page_buttons:
            svg_path = button.find_element(By.TAG_NAME, 'path')
            svg_path_data = svg_path.get_attribute("d")
            if "M9.213" in svg_path_data:
                button.click()
                break  # Break the loop after clicking the button

    ## loop: Continuously scrapes data from each page
    ## until either 10 pages have been scraped or there are no more pages to scrape.
    next_page()
    while True:
        new_df = scrape_page()
        sleep(15)
        df = pd.concat([df, new_df], ignore_index=True)
        sleep(15)
        next_page()
        page_counter += 1
        if page_counter >= 10:
            break
    return df
analyst_df=scrape_and_search('analyst')
customer_service_df=scrape_and_search('customer service representative')
combined_df=pd.concat([analyst_df,customer_service_df],ignore_index=True)
combined_df['new_location']=combined_df['job location'].str.split('-').str[1]
location_counts=combined_df['new_location'].value_counts()
plt.figure(figsize=(14,8))
location_counts.plot(kind='bar',color='skyblue')
plt.xlabel('Location')
plt.ylabel('Frequency')
plt.title('Frequency of Locations')
plt.xticks(rotation=60, ha='right',fontsize=8)
plt.show()
combined_df.to_csv(r'C:\Users\pc\Downloads\search_data.csv',index=False)
