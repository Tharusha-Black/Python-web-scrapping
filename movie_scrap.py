import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape movie details
def scrape_movie_details(movie_url):
    # Send request to movie details page
    response = requests.get(movie_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract movie title from the <title> tag
    title = soup.title.text.strip().split('|')[0].strip()

    # Extract movie info section
    movie_info_section = soup.find('section', class_='media-info')

    # Extract synopsis
    synopsis = movie_info_section.find('div', class_='synopsis-wrap').find('rt-text').text.strip()

    # Extract other movie details from <dl> tags
    details_dl = movie_info_section.find('dl')
    details = {}
    for dt_dd_pair in details_dl.find_all(['dt', 'dd']):
        if dt_dd_pair.name == 'dt':
            key = dt_dd_pair.text.strip()
        elif dt_dd_pair.name == 'dd':
            value = dt_dd_pair.text.strip()
            details[key] = value

    tomato_meter_score = soup.find('rt-button', slot='criticsScore').find('rt-text').text.strip()
    audience_score = soup.find('rt-button', slot='audienceScore').find('rt-text').text.strip()

    # Return a dictionary with the extracted information
    movie_data = {
        'Title': title,
        'Director': details.get('Director', ''),
        'Screenwriter': details.get('Screenwriter', ''),
        'Distributor': details.get('Distributor', ''),
        'Production Co': details.get('Production Co', ''),
        'Rating': details.get('Rating', ''),
        'Genre': details.get('Genre', ''),
        'Original Language': details.get('Original Language', ''),
        'Release Date (Theaters)': details.get('Release Date (Theaters)', ''),
        'Box Office (Gross USA)': details.get('Box Office (Gross USA)', ''),
        'Sound Mix': details.get('Sound Mix', ''),
        'Aspect Ratio': details.get('Aspect Ratio', ''),
        'Tomato Meter Score': tomato_meter_score,
        'Audience Score': audience_score,
    }
    return movie_data

# Main function
def main():
    # URL of the main page
    url = 'https://www.rottentomatoes.com/browse/movies_in_theaters/sort:top_box_office'
    # Send request to the main page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all movie tiles
    movie_tiles = soup.find_all('div', class_='js-tile-link')

    # List to store movie data
    movie_data_list = []

    # Iterate over each movie tile
    for tile in movie_tiles:
        # Extract the URL of the movie details page
        movie_url = 'https://www.rottentomatoes.com' + tile.find('a')['href']
        print(tile.find('rt-img')['alt'] + " Retrieved Successfully")
        # Scrape details from the movie details page
        movie_data = scrape_movie_details(movie_url)
        # Append the extracted data to the list
        movie_data_list.append(movie_data)

    # Create a Pandas DataFrame from the list of movie data
    df = pd.DataFrame(movie_data_list)
    df.to_csv('scraped_movie_data.csv', index=False)
    # Print the DataFrame
    print(df)

if __name__ == "__main__":
    main()
