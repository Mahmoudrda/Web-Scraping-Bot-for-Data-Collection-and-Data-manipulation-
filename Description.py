"""
This Python script utilizes the Selenium library to automate web scraping
of job listings from the Wuzzuf job search website (https://wuzzuf.net/jobs/egypt).
The script searches for specific job titles, scrapes relevant job data,
and combines the results into a single CSV file for further analysis.

Function Definition (search_and_scrape):

The search_and_scrape function is defined to search
for a given job title on the Wuzzuf website and scrape job data for the search results.
It takes a single argument search_term, which represents the job title to search for.
Within the function:
A Chrome WebDriver is initialized, and the Wuzzuf website is opened.
The search bar is located, and the provided search_term is entered.
Job data from the current page is scraped using Selenium's WebDriver methods.
A loop is implemented to navigate through multiple pages of search results,
scraping job data from each page until either ten pages have been scraped or there are no more pages to scrape.
Once all data is collected, the WebDriver is closed,
and the scraped job data is returned as a Pandas DataFrame.
Search and Scrape Process:

The script calls the search_and_scrape function twice,
once for the "analyst" job title and once for the "customer service" job title.
Each call returns a DataFrame containing job data for the respective search term.
Combining DataFrames:

After scraping job data for both search terms,
the script concatenates the two DataFrames into one using the pd.concat function from the Pandas library.
The combined DataFrame contains job listings for both "analyst" and "customer service" positions.
Saving to CSV:

Finally, the combined DataFrame is saved to a CSV file named "combined_job_data.csv"
using the to_csv method provided by Pandas. The index column is excluded from the CSV file.
"""