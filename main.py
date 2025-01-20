from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time
import requests
from bs4 import BeautifulSoup
import csv

# Function to get movie details from the movie page
def get_movie_details(movie_url):
    response = requests.get(movie_url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve {movie_url}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find('h1', {'data-testid': 'hero__pageTitle'})
    title = title_tag.find('span', {'class': 'hero__primary-text'}).text.strip()
    print("Title:", title)
    year_tag = soup.find('a', href=lambda href: href and 'releaseinfo' in href)
    year = year_tag.text.strip() if year_tag else "N/A"
    rating = soup.find('span', class_='sc-d541859f-1 imUuxf').text.strip() if soup.find('span', class_='sc-d541859f-1 imUuxf') else "N/A"
    genres = [genre.text.strip() for genre in soup.find_all('span', class_='sc-16ede3c-2 iUeAdT')]
    genres = ", ".join(genres) if genres else "N/A"
    
    return {
        'Title': title,
        'Year': year,
        'Rating': rating,
        'Genres': genres,
        'URL': movie_url
    }

driver_path = r'C:\Users\manas\Downloads\edgedriver_win64\msedgedriver.exe'  # Update with the correct path

service = Service(driver_path)
options = Options()

driver = webdriver.Edge(service=service, options=options)

driver.get('https://www.imdb.com/list/ls063676189/')

time.sleep(5)

movie_links = []

for page_num in range(1, 21):
    page_url = f'https://www.imdb.com/list/ls063676189/?page={page_num}'
    
    driver.get(page_url)
    
    time.sleep(5)
    
    links = driver.find_elements(By.XPATH, '//a[contains(@href, "/title/")]')
    
    for link in links:
        movie_links.append(link.get_attribute('href'))

    print(f"Page {page_num} processed. Total links found: {len(movie_links)}")

driver.quit()

movie_data = []

for movie_url in movie_links:
    print(f"Scraping details for: {movie_url}")
    movie_details = get_movie_details(movie_url)
    
    if movie_details:
        movie_data.append(movie_details)

# Define CSV file name
csv_file = 'podcast_movies.csv'

# Write the movie details to a CSV file
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Title', 'Year', 'Rating', 'Genres', 'URL'])
    
    # Write the header
    writer.writeheader()
    
    # Write the movie data
    writer.writerows(movie_data)

print(f"Movie details saved to {csv_file}")
